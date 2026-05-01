import time
import random
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def print_log(text):
    # Memaksa teks langsung keluar ke log GitHub Actions (Unbuffered)
    print(text, flush=True)
    sys.stdout.flush()

def run_bot():
    # Daftar link video baru (110 link)
    video_links = [
        "https://www.febspot.com/video/3189338", "https://www.febspot.com/video/3189741", "https://www.febspot.com/video/3189743",
        "https://www.febspot.com/video/3189744", "https://www.febspot.com/video/3189747", "https://www.febspot.com/video/3189748",
        "https://www.febspot.com/video/3189750", "https://www.febspot.com/video/3189751", "https://www.febspot.com/video/3189753",
        "https://www.febspot.com/video/3189754", "https://www.febspot.com/video/3189846", "https://www.febspot.com/video/3189848",
        "https://www.febspot.com/video/3189849", "https://www.febspot.com/video/3189851", "https://www.febspot.com/video/3189857",
        "https://www.febspot.com/video/3189858", "https://www.febspot.com/video/3189860", "https://www.febspot.com/video/3189861",
        "https://www.febspot.com/video/3189863", "https://www.febspot.com/video/3189864", "https://www.febspot.com/video/3183766",
        "https://www.febspot.com/video/3185499", "https://www.febspot.com/video/3185507", "https://www.febspot.com/video/3185508",
        "https://www.febspot.com/video/3185510", "https://www.febspot.com/video/3185511", "https://www.febspot.com/video/3185512",
        "https://www.febspot.com/video/3189317", "https://www.febspot.com/video/3189318", "https://www.febspot.com/video/3189319",
        "https://www.febspot.com/video/3189320", "https://www.febspot.com/video/3189321", "https://www.febspot.com/video/3189328",
        "https://www.febspot.com/video/3189329", "https://www.febspot.com/video/3189330", "https://www.febspot.com/video/3189331",
        "https://www.febspot.com/video/3189333", "https://www.febspot.com/video/3189334", "https://www.febspot.com/video/3189335",
        "https://www.febspot.com/video/3189336", "https://www.febspot.com/video/3181867", "https://www.febspot.com/video/3181868",
        "https://www.febspot.com/video/3182071", "https://www.febspot.com/video/3182072", "https://www.febspot.com/video/3182073",
        "https://www.febspot.com/video/3182075", "https://www.febspot.com/video/3182076", "https://www.febspot.com/video/3182077",
        "https://www.febspot.com/video/3182079", "https://www.febspot.com/video/3182080", "https://www.febspot.com/video/3182081",
        "https://www.febspot.com/video/3182082", "https://www.febspot.com/video/3182083", "https://www.febspot.com/video/3182086",
        "https://www.febspot.com/video/3182087", "https://www.febspot.com/video/3182089", "https://www.febspot.com/video/3182091",
        "https://www.febspot.com/video/3182092", "https://www.febspot.com/video/3182093", "https://www.febspot.com/video/3183764",
        "https://www.febspot.com/video/3171758", "https://www.febspot.com/video/3171759", "https://www.febspot.com/video/3171760",
        "https://www.febspot.com/video/3171761", "https://www.febspot.com/video/3171762", "https://www.febspot.com/video/3181098",
        "https://www.febspot.com/video/3181099", "https://www.febspot.com/video/3181100", "https://www.febspot.com/video/3181101",
        "https://www.febspot.com/video/3181102", "https://www.febspot.com/video/3181103", "https://www.febspot.com/video/3181104",
        "https://www.febspot.com/video/3181106", "https://www.febspot.com/video/3181108", "https://www.febspot.com/video/3181109",
        "https://www.febspot.com/video/3181860", "https://www.febspot.com/video/3181861", "https://www.febspot.com/video/3181863",
        "https://www.febspot.com/video/3181865", "https://www.febspot.com/video/3181866", "https://www.febspot.com/video/3141597",
        "https://www.febspot.com/video/3141598", "https://www.febspot.com/video/3141600", "https://www.febspot.com/video/3141605",
        "https://www.febspot.com/video/3141763", "https://www.febspot.com/video/3141777", "https://www.febspot.com/video/3141780",
        "https://www.febspot.com/video/3144339", "https://www.febspot.com/video/3144340", "https://www.febspot.com/video/3144342",
        "https://www.febspot.com/video/3144343", "https://www.febspot.com/video/3144347", "https://www.febspot.com/video/3144349",
        "https://www.febspot.com/video/3171613", "https://www.febspot.com/video/3171614", "https://www.febspot.com/video/3171617",
        "https://www.febspot.com/video/3171618", "https://www.febspot.com/video/3171620", "https://www.febspot.com/video/3171623",
        "https://www.febspot.com/video/3171624", "https://www.febspot.com/video/3137143", "https://www.febspot.com/video/3137150",
        "https://www.febspot.com/video/3137152", "https://www.febspot.com/video/3137158", "https://www.febspot.com/video/3137159",
        "https://www.febspot.com/video/3137164", "https://www.febspot.com/video/3141573", "https://www.febspot.com/video/3141576",
        "https://www.febspot.com/video/3141587", "https://www.febspot.com/video/3141592"
    ]

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    print_log(">>> Menyiapkan Browser...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Menghapus flag webdriver
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        # CEK IP BROWSER
        print_log(">>> Mengecek Alamat IP...")
        driver.get("https://api.ipify.org")
        ip_addr = driver.find_element(By.TAG_NAME, "body").text
        print_log(f">>> IP BROWSER: {ip_addr}")
        print_log("-" * 40)

        # Shuffle links agar tidak berpola
        random.shuffle(video_links)
        
        for index, link in enumerate(video_links):
            print_log(f"\n[{index+1}/{len(video_links)}] Membuka: {link}")
            driver.get(link)
            time.sleep(5) 
            
            try:
                wait = WebDriverWait(driver, 25)
                video_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
                
                # Klik play
                actions = ActionChains(driver)
                actions.move_to_element(video_element).click().perform()
                print_log("Berhasil klik Play.")

                # Ambil durasi video
                duration = driver.execute_script("return arguments[0].duration;", video_element)
                
                if duration and duration > 0:
                    print_log(f"Video dikesan. Durasi: {int(duration)} detik.")
                    start_watch = time.time()
                    
                    while True:
                        current = driver.execute_script("return arguments[0].currentTime;", video_element)
                        ended = driver.execute_script("return arguments[0].ended;", video_element)
                        
                        if ended or current >= (duration - 1):
                            print_log("Konfirmasi: Video selesai ditonton.")
                            break
                            
                        # Safety timeout
                        if (time.time() - start_watch) > (duration + 20):
                            print_log("Timeout: Melanjutkan ke video berikutnya.")
                            break
                            
                        if int(current) % 15 == 0 and int(current) > 0:
                            print_log(f"Status: Menonton detik ke-{int(current)}")
                            
                        time.sleep(5)
                else:
                    print_log("Gagal ambil durasi, tunggu 25 detik manual...")
                    time.sleep(25)

            except Exception:
                print_log("Peringatan: Gagal memuat video.")
            
            jeda = random.randint(4, 7)
            print_log(f"Istirahat {jeda} detik...")
            time.sleep(jeda)

    except Exception as e:
        print_log(f"KESALAHAN SISTEM: {e}")
    finally:
        print_log("\nProses selesai. Menutup browser.")
        driver.quit()

if __name__ == "__main__":
    run_bot()
