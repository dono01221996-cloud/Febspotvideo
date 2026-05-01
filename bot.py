import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

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

    print("Menginisialisasi Browser...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        random.shuffle(video_links)
        
        for index, link in enumerate(video_links):
            print(f"\n[{index+1}/{len(video_links)}] Membuka: {link}")
            driver.get(link)
            
            try:
                # Tunggu player video muncul
                wait = WebDriverWait(driver, 30)
                video_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
                
                # Klik untuk memutar
                ActionChains(driver).move_to_element(video_element).click().perform()
                time.sleep(3)

                # Ambil durasi video dari metadata player
                total_duration = driver.execute_script("return arguments[0].duration;", video_element)
                
                if total_duration and total_duration > 0:
                    print(f"Deteksi durasi: {int(total_duration)} detik.")
                    
                    # Pantau video sampai selesai
                    start_watch = time.time()
                    while True:
                        current_time = driver.execute_script("return arguments[0].currentTime;", video_element)
                        is_ended = driver.execute_script("return arguments[0].ended;", video_element)
                        
                        # Jika video berakhir atau waktu tonton sudah melebihi durasi video
                        if is_ended or current_time >= (total_duration - 1):
                            print("Selesai: Video telah diputar sampai akhir.")
                            break
                        
                        # Keamanan: Jika macet lebih dari durasi asli + 30 detik, paksa stop
                        if (time.time() - start_watch) > (total_duration + 30):
                            print("Timeout: Video macet atau terlalu lama, pindah...")
                            break

                        time.sleep(2)
                else:
                    print("Gagal mendeteksi durasi, menonton manual 30 detik...")
                    time.sleep(30)

            except Exception as e:
                print(f"Skip video ini karena error.")
            
            # Jeda antar video (Singkat saja karena videonya pendek)
            time.sleep(random.randint(5, 10))

    finally:
        print("\nSemua link diproses.")
        driver.quit()

if __name__ == "__main__":
    run_bot()
