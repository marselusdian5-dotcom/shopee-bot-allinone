import os
from playwright.sync_api import sync_playwright

def simpan_sesi():
    with sync_playwright() as p:
        # Menentukan lokasi penyimpanan profil Edge lokal
        user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Microsoft", "Edge", "User Data Bot")
        
        print("[+] Membuka Edge dengan Profil Pengguna...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            channel="msedge",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://shopee.co.id/buyer/login")

        print("[!] Silakan login di browser.")
        print("[!] Setelah berhasil masuk ke beranda, tekan ENTER di terminal...")
        input()

        # Simpan sesi login ke file state.json
        context.storage_state(path="state.json")
        print("[✓] Sesi login berhasil disimpan ke 'state.json'!")
        context.close()

if __name__ == "__main__":
    simpan_sesi()