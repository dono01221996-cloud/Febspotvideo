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
        # Link dari daftar sebelumnya
        "https://www.febspot.com/video/3189338", "https://www.febspot.com/video/3189741",
        "https://www.febspot.com/video/3189743", "https://www.febspot.com/video/3189744",
        "https://www.febspot.com/video/3189747", "https://www.febspot.com/video/3189748",
        "https://www.febspot.com/video/3189750", "https://www.febspot.com/video/3189751",
        "https://www.febspot.com/video/3189753", "https://www.febspot.com/video/3189754",
        "https://www.febspot.com/video/3189846", "https://www.febspot.com/video/3189848",
        "https://www.febspot.com/video/3189849", "https://www.febspot.com/video/3189851",
        "https://www.febspot.com/video/3189857", "https://www.febspot.com/video/3189858",
        "https://www.febspot.com/video/3189860", "https://www.febspot.com/video/3189861",
        "https://www.febspot.com/video/3189863", "https://www.febspot.com/video/3189864",
        # Tambahan link baru
        "https://www.febspot.com/video/3181098", "https://www.febspot.com/video/3181099",
        "https://www.febspot.com/video/3181100", "https://www.febspot.com/video/3181101",
        "https://www.febspot.com/video/3181102", "https://www.febspot.com/video/3181103",
        "https://www.febspot.com/video/3181104", "https://www.febspot.com/video/3181106",
        "https://www.febspot.com/video/3181108", "https://www.febspot.com/video/3181109",
        "https://www.febspot.com/video/3181860", "https://www.febspot.com/video/3181861",
        "https://www.febspot.com/video/3181863", "https://www.febspot.com/video/3181865",
        "https://www.febspot.com/video/3181866", "https://www.febspot.com/video/3181867",
        "https://www.febspot.com/video/3181868", "https://www.febspot.com/video/3182071",
        "https://www.febspot.com/video/3182072", "https://www.febspot.com/video/3182073",
        "https://www.febspot.com/video/3182075", "https://www.febspot.com/video/3182076",
        "https://www.febspot.com/video/3182077", "https://www.febspot.com/video/3182079",
        "https://www.febspot.com/video/3182080", "https://www.febspot.com/video/3182081",
        "https://www.febspot.com/video/3182082", "https://www.febspot.com/video/3182083",
        "https://www.febspot.com/video/3182086", "https://www.febspot.com/video/3182087",
        "https://www.febspot.com/video/3182089", "https://www.febspot.com/video/3182091",
        "https://www.febspot.com/video/3182092", "https://www.febspot.com/video/3182093",
        "https://www.febspot.com/video/3183764", "https://www.febspot.com/video/3183766",
        "https://www.febspot.com/video/3185499", "https://www.febspot.com/video/3185507",
        "https://www.febspot.com/video/3185508", "https://www.febspot.com/video/3185510",
        "https://www.febspot.com/video/3185511", "https://www.febspot.com/video/3185512",
        "https://www.febspot.com/video/3189317", "https://www.febspot.com/video/3189318",
        "https://www.febspot.com/video/3189319", "https://www.febspot.com/video/3189320",
        "https://www.febspot.com/video/3189321", "https://www.febspot.com/video/3189328",
        "https://www.febspot.com/video/3189329", "https://www.febspot.com/video/3189330"
    ]

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Mengacak urutan agar tidak berpola
        random.shuffle(video_links)
        
        for index, link in enumerate(video_links):
            print(f"[{index+1}/{len(video_links)}] Membuka: {link}")
            driver.get(link)
            
            try:
                # 1. Tunggu elemen video muncul
                wait = WebDriverWait(driver, 20)
                video_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
                
                # 2. Force Play via JavaScript
                driver.execute_script("arguments[0].play();", video_element)
                print("Mencoba memutar video...")

                # 3. Pantau status video
                while True:
                    is_ended = driver.execute_script("return arguments[0].ended;", video_element)
                    is_paused = driver.execute_script("return arguments[0].paused;", video_element)
                    current_time = driver.execute_script("return arguments[0].currentTime;", video_element)

                    if is_ended:
                        print("Video selesai diputar.")
                        break
                    
                    if is_paused and current_time > 0:
                        driver.execute_script("arguments[0].play();", video_element)
                    
                    if int(current_time) % 30 == 0 and int(current_time) > 0:
                        print(f"Sedang menonton... Durasi: {int(current_time)} detik")
                    
                    time.sleep(5)

            except Exception as e:
                print(f"Gagal memutar video ini: {e}")
                continue
            
            # Jeda antar video
            time.sleep(random.randint(5, 10))
            
    except Exception as e:
        print(f"Kesalahan Fatal: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_bot()
