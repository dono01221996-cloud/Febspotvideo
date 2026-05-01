import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    options = uc.ChromeOptions()
    options.add_argument('--headless') # Tetap headless untuk GitHub
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--mute-audio')
    
    # Menyamarkan identitas browser
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    print("Memulai Browser Stealth...")
    driver = uc.Chrome(options=options)

    try:
        # Acak daftar video agar tidak berpola sama setiap kali jalan
        random.shuffle(video_links)
        
        for index, link in enumerate(video_links):
            print(f"[{index+1}/{len(video_links)}] Menuju: {link}")
            driver.get(link)
            
            try:
                # Tunggu video muncul
                wait = WebDriverWait(driver, 25)
                video_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
                
                # Scroll sedikit agar terlihat seperti manusia membaca halaman
                driver.execute_script("window.scrollTo(0, 300);")
                time.sleep(2)

                # Paksa play
                driver.execute_script("arguments[0].play();", video_element)
                print("Video diputar.")

                # Monitoring durasi
                start_time = time.time()
                # Tonton selama 70-90 detik (acak)
                watch_duration = random.randint(70, 90) 
                
                while time.time() - start_time < watch_duration:
                    is_ended = driver.execute_script("return arguments[0].ended;", video_element)
                    curr_time = driver.execute_script("return arguments[0].currentTime;", video_element)
                    
                    if is_ended:
                        print("Video selesai sebelum durasi target.")
                        break
                        
                    if int(curr_time) % 20 == 0 and int(curr_time) > 0:
                        print(f"Status: Menonton detik ke-{int(curr_time)}...")
                    
                    time.sleep(5)

            except Exception as e:
                print(f"Gagal memuat video ini, lanjut ke berikutnya...")
            
            # Jeda antar video (PENTING agar IP tidak langsung diblokir)
            jeda = random.randint(15, 30)
            print(f"Jeda istirahat {jeda} detik...")
            time.sleep(jeda)
            
    except Exception as e:
        print(f"Error Fatal: {e}")
    finally:
        print("Bot selesai bertugas.")
        driver.quit()

if __name__ == "__main__":
    run_bot()
