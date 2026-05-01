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

    # Konfigurasi Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--mute-audio")
    
    # Penyamaran agar tidak terdeteksi sebagai Bot
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Inisialisasi Driver dengan ChromeDriverManager untuk mengatasi masalah versi 147
    print("Menginisialisasi WebDriver...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Menghapus flag 'webdriver' di browser agar lebih 'stealth'
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    try:
        random.shuffle(video_links) # Acak urutan video
        
        for index, link in enumerate(video_links):
            print(f"[{index+1}/{len(video_links)}] Membuka: {link}")
            driver.get(link)
            
            try:
                # Tunggu elemen video tersedia
                wait = WebDriverWait(driver, 30)
                video_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
                
                # Simulasi interaksi manusia: scroll sedikit
                driver.execute_script("window.scrollTo(0, random.randint(200, 500));")
                time.sleep(2)

                # Paksa play video
                driver.execute_script("arguments[0].play();", video_element)
                print("Video berhasil diputar (Force Play).")

                # Pantau durasi nonton (70-95 detik)
                target_duration = random.randint(70, 95)
                start_time = time.time()
                
                while time.time() - start_time < target_duration:
                    curr_time = driver.execute_script("return arguments[0].currentTime;", video_element)
                    is_ended = driver.execute_script("return arguments[0].ended;", video_element)
                    
                    if is_ended:
                        print("Video sudah mencapai akhir.")
                        break
                    
                    if int(curr_time) % 30 == 0 and int(curr_time) > 0:
                        print(f"Laporan: Sedang menonton detik ke-{int(curr_time)}...")
                    
                    time.sleep(5)
                
                print(f"Selesai menonton video ini selama {int(time.time() - start_time)} detik.")

            except Exception as e:
                print(f"Gagal memutar video ini: {e}")
            
            # Jeda antar video agar natural
            break_time = random.randint(10, 20)
            print(f"Istirahat sejenak {break_time} detik...")
            time.sleep(break_time)
            
    except Exception as e:
        print(f"Terjadi kesalahan sistem: {e}")
    finally:
        print("Bot selesai. Menutup browser.")
        driver.quit()

if __name__ == "__main__":
    run_bot()
