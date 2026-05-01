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
    print(text, flush=True)

def run_bot():
    video_links = [
        "https://www.febspot.com/video/3189338", "https://www.febspot.com/video/3189741",
        "https://www.febspot.com/video/3189743", "https://www.febspot.com/video/3189744",
        "https://www.febspot.com/video/3189747", "https://www.febspot.com/video/3189748",
        "https://www.febspot.com/video/3189750", "https://www.febspot.com/video/3189751",
        "https://www.febspot.com/video/3189753", "https://www.febspot.com/video/3189754",
        "https://www.febspot.com/video/3189846", "https://www.febspot.com/video/3189848",
        "https://www.febspot.com/video/3189849", "https://www.febspot.com/video/3189851",
        "https://www.febspot.com/video/3189857", "https://www.febspot.com/video/3189858",
        "https://www.febspot.com/video/3189860", "https://www.febspot.com/video/3189861",
        "https://www.febspot.com/video/3189863", "https://www.febspot.com/video/3189864"
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

    print_log(">>> Memulai inisialisasi browser...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Hilangkan jejak bot
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        random.shuffle(video_links)
        
        for index, link in enumerate(video_links):
            print_log(f"\n[{index+1}/{len(video_links)}] Membuka: {link}")
            driver.get(link)
            time.sleep(5)
            
            try:
                wait = WebDriverWait(driver, 25)
                video_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
                
                # Klik play fisik
                actions = ActionChains(driver)
                actions.move_to_element(video_element).click().perform()
                print_log("Klik Play berhasil dilakukan.")

                # Ambil durasi
                duration = driver.execute_script("return arguments[0].duration;", video_element)
                
                if duration and duration > 0:
                    print_log(f"Video terdeteksi. Durasi: {int(duration)} detik.")
                    start_time = time.time()
                    
                    while True:
                        current = driver.execute_script("return arguments[0].currentTime;", video_element)
                        ended = driver.execute_script("return arguments[0].ended;", video_element)
                        
                        if ended or current >= (duration - 1):
                            print_log("Konfirmasi: Video Selesai ditonton.")
                            break
                            
                        # Safety timeout jika macet
                        if (time.time() - start_time) > (duration + 20):
                            print_log("Timeout: Pindah ke video berikutnya.")
                            break
                            
                        if int(current) % 15 == 0 and int(current) > 0:
                            print_log(f"Sedang menonton... Detik ke-{int(current)}")
                            
                        time.sleep(5)
                else:
                    print_log("Gagal ambil durasi, nonton standar 30 detik...")
                    time.sleep(30)

            except Exception as e:
                print_log(f"Error: Video tidak ditemukan atau gagal muat.")
            
            print_log("Jeda istirahat 7 detik...")
            time.sleep(7)

    except Exception as e:
        print_log(f"FATAL ERROR: {e}")
    finally:
        print_log("\nSemua proses selesai. Menutup browser.")
        driver.quit()

if __name__ == "__main__":
    run_bot()
