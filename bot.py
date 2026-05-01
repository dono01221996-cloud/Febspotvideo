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
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--window-size=1280,720")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    print_log(">>> Menyiapkan Browser...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Bypass bot detection
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        # CEK IP
        driver.get("https://api.ipify.org")
        ip_saat_ini = driver.find_element(By.TAG_NAME, "body").text
        print_log(f">>> IP BROWSER: {ip_saat_ini}")

        random.shuffle(video_links)
        
        for index, link in enumerate(video_links):
            print_log(f"\n[{index+1}/{len(video_links)}] Membuka: {link}")
            driver.get(link)
            time.sleep(7)
            
            try:
                wait = WebDriverWait(driver, 25)
                video_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
                
                # Klik Play
                actions = ActionChains(driver)
                actions.move_to_element(video_element).click().perform()
                print_log("Berhasil klik tombol Play.")

                # Ambil durasi
                duration = driver.execute_script("return arguments[0].duration;", video_element)
                
                if duration and duration > 0:
                    print_log(f"Durasi video: {int(duration)} detik.")
                    
                    # Ambil screenshot di awal pemutaran
                    if index == 0 or index % 10 == 0:
                        driver.save_screenshot(f"screenshot_{index}.png")
                        print_log(f"Screenshot disimpan: screenshot_{index}.png")

                    start_watch = time.time()
                    while True:
                        current = driver.execute_script("return arguments[0].currentTime;", video_element)
                        ended = driver.execute_script("return arguments[0].ended;", video_element)
                        
                        if ended or current >= (duration - 1):
                            print_log("Selesai: Video habis.")
                            break
                        
                        if (time.time() - start_watch) > (duration + 15):
                            print_log("Timeout: Pindah ke video berikutnya.")
                            break
                            
                        if int(current) % 15 == 0 and int(current) > 0:
                            print_log(f"Nonton... detik ke-{int(current)}")
                            
                        time.sleep(5)
                else:
                    print_log("Gagal deteksi durasi, tunggu 20 detik...")
                    time.sleep(20)

            except Exception as e:
                print_log("Gagal memuat video ini.")
            
            time.sleep(random.randint(5, 8))

    except Exception as e:
        print_log(f"ERROR: {e}")
    finally:
        print_log("\nSelesai.")
        driver.quit()

if __name__ == "__main__":
    run_bot()
