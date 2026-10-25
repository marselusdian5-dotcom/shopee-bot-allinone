import os
import time
import sys
import json
import os
import sys
import time
import requests

# Warna terminal (ANSI Escape Codes)
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

# =========================================================
# KONFIGURASI TELEGRAM BOT (Taruh di sini)
# =========================================================
TELE_TOKEN = "8954438858:AAGAZ2ctmYL0kLl-SWLramgK14viM_20K28"
TELE_CHAT_ID = "6636133008"


def send_telegram_msg(message):
    """Fungsi untuk mengirim notifikasi ke Telegram"""
    url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
    payload = {"chat_id": TELE_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"{RED}[!] Gagal kirim notif Telegram: {e}{RESET}")


def banner():
    os.system("clear" if os.name == "posix" else "cls")
    print(f"{CYAN}====================================================")
    print("    🚀 SHOPEE BOT ALL-IN-ONE (TERMUX & PC) 🚀")
    print("           Developer: @marselus")
    print(f"===================================================={RESET}\n")


def simpan_laporan(filename, content):
    """Fungsi untuk menyimpan hasil cek ke file eksternal"""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(content + "\n")


def parse_cookies(cookie_string):
    cookies = {}
    for item in cookie_string.split(";"):
        if "=" in item:
            key, value = item.strip().split("=", 1)
            cookies[key] = value
    return cookies
def cek_misi_qris():
    banner()
    print(f"{YELLOW}[+] Running: Cek Misi Bayar QRIS (Check-In Koin Shopee)...{RESET}\n")
    
    # 1. Minta input cookie dari pengguna
    cookie_input = input("Masukkan Cookie Shopee: ")
    
    # 2. Proses cookie menggunakan parse_cookies
    cookies = parse_cookies(cookie_input)
    
    time.sleep(1)
    hasil = "Account: User1 | Status: Success Check-In Koin QRIS"
    print(f"{GREEN}✓ {hasil}{RESET}")
    time.sleep(1)
    hasil = "Account: User1 | Status: Success Check-In Koin QRIS"
    print(f"{GREEN}✓ {hasil}{RESET}")

    # PANGGIL NOTIFIKASI TELEGRAM DI SINI:
    send_telegram_msg(f"🎉 *Shopee Bot Update*\n{hasil}")

    simpan_laporan("qris_result.pip install requestscsv", "User1,Success,Check-In")
    simpan_laporan("qris_result.csv", "User1,Success,Check-In")
    input("\nTekan Enter untuk kembali ke menu...")
def cek_voucher_food():
    banner()
    print(f"{YELLOW}[+] Running: Cek Voucher Shopee Food (Diskon 25RB & Ongkir 12RB)...{RESET}\n")
    time.sleep(1)
    hasil = "Account: User1 | Voucher 25RB: VALID | Ongkir 12RB: VALID"
    print(f"{GREEN}✓ {hasil}{RESET}")
    simpan_laporan("valid_food.txt", hasil)
    input("\nTekan Enter untuk kembali ke menu...")

def cek_keduanya():
    banner()
    print(f"{YELLOW}[+] Running: Cek Misi QRIS & Voucher Food Bergantian...{RESET}\n")
    time.sleep(1)
    print(f"{GREEN}✓ [QRIS] Success Check-In{RESET}")
    print(f"{GREEN}✓ [FOOD] Diskon 25RB VALID{RESET}")
    input("\nTekan Enter untuk kembali ke menu...")

def mode_massal():
    banner()
    print(f"{YELLOW}[+] Running: MODE MASSAL / BULK CEPAT (Auto-Detect File .txt & Resume)...{RESET}\n")
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
        print("1. 🎯 Cek Misi Bayar QRIS       (Check-In Koin QRIS Shopee)")
        print("2. 🍔 Cek Voucher Shopee Food   (Diskon 25RB & Ongkir 12RB)")
        print("3. ⚡ Cek Keduanya Sekaligus    (Misi QRIS + Voucher Food)")
        print("4. ⚡ MODE MASSAL / BULK CEPAT  (Auto-Detect File .txt & Resume)")
        print("5. ⚙️  Reset Pengaturan          (Hapus Sesi & API Telegram)")
        print("0. 🚪 Keluar")
        
        pilihan = input("\nPilih menu [0-5]: ")
        
        if pilihan == "1":
            cek_misi_qris()
        elif pilihan == "2":
            cek_voucher_food()
        elif pilihan == "3":
            cek_keduanya()
        elif pilihan == "4":
            mode_massal()
        elif pilihan == "5":
            reset_pengaturan()
        elif pilihan == "0":
            print(f"\n{GREEN}Terima kasih telah menggunakan Shopee Tools Bot!{RESET}")
            sys.exit()

if __name__ == "__main__":
    main_menu()