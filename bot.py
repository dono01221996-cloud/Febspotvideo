import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
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
    chrome_options.add_argument("--mute-audio") # Matikan suara agar tidak berat di server
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        random.shuffle(video_links)
        
        for index, link in enumerate(video_links):
            print(f"[{index+1}/{len(video_links)}] Membuka: {link}")
            driver.get(link)
            
            try:
                # 1. Tunggu elemen video muncul
                wait = WebDriverWait(driver, 20)
                video_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
                
                # 2. Coba jalankan video via JavaScript (Force Play)
                driver.execute_script("arguments[0].play();", video_element)
                print("Mencoba memutar video...")

                # 3. Loop untuk memantau status video
                while True:
                    # Ambil status dari player video
                    is_ended = driver.execute_script("return arguments[0].ended;", video_element)
                    is_paused = driver.execute_script("return arguments[0].paused;", video_element)
                    current_time = driver.execute_script("return arguments[0].currentTime;", video_element)

                    if is_ended:
                        print("Video selesai diputar secara alami.")
                        break
                    
                    # Jika video terhenti (paused) tapi belum selesai, coba play lagi
                    if is_paused and current_time > 0:
                        driver.execute_script("arguments[0].play();", video_element)
                    
                    # Cetak durasi setiap 30 detik agar log GitHub Actions tidak kosong
                    if int(current_time) % 30 == 0 and int(current_time) > 0:
                        print(f"Sedang menonton... Durasi saat ini: {int(current_time)} detik")
                    
                    time.sleep(5) # Cek setiap 5 detik agar hemat CPU

            except Exception as e:
                print(f"Gagal memutar video ini: {e}")
                continue # Lanjut ke video berikutnya jika gagal
            
            # Beri jeda antar video agar tidak terlihat seperti bot kaku
            time.sleep(random.randint(5, 10))
            
    except Exception as e:
        print(f"Kesalahan Fatal: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()

