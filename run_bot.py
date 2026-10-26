import os
import requests
from playwright.sync_api import sync_playwright

TELEGRAM_TOKEN = "8954438858:AAGAZ2ctmYL0kLl-SWLramgK14viM_2OK28"
TELEGRAM_CHAT_ID = "6636133008"

def send_telegram_msg(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"[!] Gagal kirim Telegram: {e}")

def simpan_laporan(filename, isi):
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(isi + "\n")
    except Exception as e:
        print(f"[!] Gagal menyimpan laporan: {e}")

def jalankan_bot():
    if not os.path.exists("state.json"):
        print("[!] File state.json tidak ditemukan. Jalankan save_session.py dulu!")
        return

    with sync_playwright() as p:
        user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Microsoft", "Edge", "User Data Bot")
        
        print("[+] Membuka Shopee via Edge...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            channel="msedge",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        
        print("[+] Membuka Halaman Voucher Saya...")
        page.goto("https://shopee.co.id/user/voucher")
        page.wait_for_timeout(7000)

        if "login" not in page.url:
            # Mengambil seluruh isi teks dari elemen utama halaman
            body_text = page.inner_text("body")
            lines = [line.strip() for line in body_text.split("\n") if line.strip()]
            
            # Filter baris yang berisi kata kunci promo/voucher
            vouchers_found = []
            for item in lines:
                item_lower = item.lower()
                if any(k in item_lower for k in ["diskon", "ongkir", "cashback", "makanan", "food", "gratis"]):
                    if len(item) < 60 and item not in vouchers_found:
                        vouchers_found.append(item)
            
            # Ambil maksimal 5 baris voucher unik
            top_vouchers = vouchers_found[:5]
            detail_str = "\n".join([f"• {v}" for v in top_vouchers]) if top_vouchers else "• Sesi Aktif (Voucher terverifikasi di UI)"

            msg = (
                f"🎉 *Shopee Food & Voucher Success*\n"
                f"👤 *Account:* marselusdian044\n"
                f"🎫 *Status:* Sesi Valid & Berhasil Diumpan\n\n"
                f"📌 *Detail Promo & Voucher Terdeteksi:*\n{detail_str}"
            )
            
            print(f"[✓] {msg}")
            send_telegram_msg(msg)
            simpan_laporan("valid_food.txt", f"marselusdian044 | Status: Berhasil | \n{detail_str}")
        else:
            msg = "⚠️ *Shopee Check Failed*\nStatus: Sesi habis, silakan login ulang via save_session.py"
            print(f"[✗] {msg}")
            send_telegram_msg(msg)

        context.close()

if __name__ == "__main__":
    jalankan_bot()