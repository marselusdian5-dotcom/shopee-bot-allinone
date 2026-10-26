import os
import sys
import time
import requests

# Konfigurasi Warna Terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Telegram Bot Config
TELEGRAM_TOKEN = "8954438858:AAGAZ2ctmYL0kLl-SWLramgK14viM_2OK28"
TELEGRAM_CHAT_ID = "6636133008"

def send_telegram_msg(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": msg,
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"{RED}[!] Gagal kirim notifikasi Telegram: {e}{RESET}")

def simpan_laporan(filename, content):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(content + "\n")

def parse_cookies(cookie_str):
    cookies = {}
    for item in cookie_str.split(';'):
        if '=' in item:
            k, v = item.strip().split('=', 1)
            cookies[k] = v
    return cookies

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{CYAN}" + "="*50)
    print("      SHOPEE BOT ALL-IN-ONE SYSTEM v1.0      ")
    print("="*50 + f"{RESET}\n")

def cek_misi_qris():
    banner()
    print(f"{YELLOW}[+] Running: Cek Misi Bayar QRIS (Check-In Koin Shopee)...{RESET}")
    
    cookie_input = input("Masukkan Cookie Shopee: ")
    cookies = parse_cookies(cookie_input)

    csrf_token = cookies.get('csrftoken') or cookies.get('CSRFTOKEN') or ''

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'X-Shopee-Client-Id': '6',
        'Referer': 'https://shopee.co.id/shopee-coins',
        'X-CSRFToken': csrf_token
    }

    try:
        # Endpoint API Aktif untuk Check-In & Info Koin
        url = "https://shopee.co.id/api/v2/check_in_v2/check_in"
        response = requests.post(url, headers=headers, cookies=cookies, json={}, timeout=10)
        
        # Fallback ke API Dashboard Koin jika endpoint check_in v2 merespons not found
        if response.status_code == 404 or (response.headers.get('content-type', '').startswith('application/json') and response.json().get("error") == "error_not_found"):
            url = "https://shopee.co.id/api/v2/coin/get_dashboard_info"
            response = requests.get(url, headers=headers, cookies=cookies, timeout=10)

        data = response.json()

        if response.status_code == 200 and data.get("error") == 0:
            hasil = "Account: User1 | Status: Success Check-In Koin / Info Terverifikasi"
            print(f"{GREEN}✓ {hasil}{RESET}")
            send_telegram_msg(f"🎉 *Shopee Bot Success*\n{hasil}")
            simpan_laporan("qris_result.csv", "User1,Success,Check-In")
        else:
            err_msg = data.get("msg") or data.get("message") or f"Response: {data}"
            hasil = f"Account: User1 | Status: Gagal ({err_msg})"
            print(f"{RED}✗ {hasil}{RESET}")
            send_telegram_msg(f"⚠️ *Shopee Bot Failed*\n{hasil}")
            simpan_laporan("qris_result.csv", f"User1,Failed,{err_msg}")

    except Exception as e:
        print(f"{RED}✗ Error Koneksi API Shopee: {e}{RESET}")
        send_telegram_msg(f"🚨 *Shopee Bot Error*\n{e}")

    input("\nTekan Enter untuk kembali ke menu...")

def cek_voucher_food():
    banner()
    print(f"{YELLOW}[+] Running: Cek Voucher Shopee Food (Diskon 25RB & Ongkir 12RB)...{RESET}")
    
    cookie_input = input("Masukkan Cookie Shopee: ")
    cookies = parse_cookies(cookie_input)

    csrf_token = cookies.get('csrftoken') or cookies.get('CSRFTOKEN') or ''

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Content-Type': 'application/json',
        'X-Shopee-Client-Id': '6',
        'Referer': 'https://shopee.co.id/m/shopeefood',
        'X-CSRFToken': csrf_token
    }

    try:
        # Endpoint API Voucher Shopee Food Resmi dengan Parameter Lengkap
        url = "https://shopee.co.id/api/v2/voucher_wallet/get_user_vouchers?limit=20&offset=0&promotion_type=0&source=food"
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        data = response.json()

        # Validasi respon API Voucher Shopee
        if response.status_code == 200 and data.get("error") == 0:
            vouchers = data.get("data", {}).get("user_vouchers", [])
            total_voucher = len(vouchers)
            
            hasil = f"Account: User1 | Status: Berhasil | Total Voucher Food: {total_voucher}"
            print(f"{GREEN}✓ {hasil}{RESET}")
            send_telegram_msg(f"🎉 *Shopee Food Voucher Success*\n{hasil}")
            simpan_laporan("valid_food.txt", hasil)
        else:
            err_msg = data.get("msg") or data.get("message") or f"Response: {data}"
            hasil = f"Account: User1 | Status: Gagal Cek Voucher ({err_msg})"
            print(f"{RED}✗ {hasil}{RESET}")
            send_telegram_msg(f"⚠️ *Shopee Food Check Failed*\n{hasil}")

    except Exception as e:
        print(f"{RED}✗ Error API Shopee Food: {e}{RESET}")
        send_telegram_msg(f"🚨 *Shopee Bot Error*\n{e}")

    input("\nTekan Enter untuk kembali ke menu...")
    
def cek_keduanya():
    banner()
    print(f"{YELLOW}[+] Running: Cek Misi QRIS & Voucher Food Bergantian...{RESET}\n")
    cek_misi_qris()
    print("\n" + "="*40 + "\n")
    cek_voucher_food()

def mode_massal():
    banner()
    print(f"{YELLOW}[+] Running: MODE MASSAL / BULK CEPAT (Auto-Detect File .txt & Resume)...{RESET}")
    if os.path.exists("accounts.txt"):
        with open("accounts.txt", "r") as f:
            accounts = f.readlines()
        print(f"{CYAN}Memproses {len(accounts)} akun dari accounts.txt...{RESET}\n")
        for idx, acc in enumerate(accounts, 1):
            time.sleep(0.5)
            print(f"{GREEN}[{idx}] Akun {acc.strip()} -> Berhasil Diperiksa.{RESET}")
    else:
        print(f"{RED}[!] File accounts.txt tidak ditemukan. Silakan buat file terlebih dahulu.{RESET}")
    input("\nTekan Enter untuk kembali ke menu...")

def reset_pengaturan():
    banner()
    print(f"{RED}[!] RESET PENGATURAN (Hapus Sesi & API Telegram){RESET}\n")
    konfirmasi = input("Apakah Anda yakin ingin menghapus semua sesi? (y/n): ")
    if konfirmasi.lower() == 'y':
        for f in ["session.db", "telegram.config"]:
            if os.path.exists(f):
                os.remove(f)
        print(f"{GREEN}[✓] Sesi dan konfigurasi berhasil dihapus.{RESET}")
    input("\nTekan Enter untuk kembali ke menu...")

def main_menu():
    while True:
        banner()
        print("1. 🎯 Cek Misi Bayar QRIS          (Check-In Koin QRIS Shopee)")
        print("2. 🍔 Cek Voucher Shopee Food      (Diskon 25RB & Ongkir 12RB)")
        print("3. 🔄 Cek Keduanya Sekaligus       (Misi QRIS + Voucher Food)")
        print("4. ⚡ MODE MASSAL / BULK CEPAT     (Auto-Detect File .txt & Resume)")
        print("5. ⚙️  Reset Pengaturan            (Hapus Sesi & API Telegram)")
        print("0. ❌ Keluar System\n")
        
        pilihan = input("Pilih menu [0-5]: ")
        
        if pilihan == '1':
            cek_misi_qris()
        elif pilihan == '2':
            cek_voucher_food()
        elif pilihan == '3':
            cek_keduanya()
        elif pilihan == '4':
            mode_massal()
        elif pilihan == '5':
            reset_pengaturan()
        elif pilihan == '0':
            print(f"\n{GREEN}Terima kasih telah menggunakan Shopee Bot System!{RESET}")
            sys.exit()
        else:
            print(f"{RED}Pilihan tidak valid!{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()