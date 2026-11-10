import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



min_fiyat = 100000
max_fiyat = 160000
kontrol_araliği = 30

options = Options()
#options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.8103.39 Safari/537.36")

def veriyi_kaydet(urun_listesi):
    dosya_adi = "fiyat_takip.csv"
    tarih_saat = datetime.now().strftime("%Y-%m-%d %H: %M: %S:")
    
    with open(dosya_adi, "a", encoding="utf-8") as dosya:
        yazici = csv.writer(dosya)
        
        if dosya.tell() == 0: 
            yazici.writerow(["Tarih/Saat", "Ürün İsmi", "Fiyat", "Link"])

        for urun in urun_listesi:
            yazici.writerow([tarih_saat,urun["isim"], urun["fiyat"], urun["link"]])
            

driver = webdriver.Chrome(options=options)

try:
    
    while True:
        try:
            driver.get("https://www.amazon.com.tr")

            arama_kutusu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
            arama_kutusu.send_keys("iphone 17 pro max" + Keys.ENTER)

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-component-type='s-search-result']"))
            )

            urun_kartlari = driver.find_elements(By.CSS_SELECTOR, "div[data-component-type='s-search-result']")
            print(f"Toplam ürün sayısı: {len(urun_kartlari)}")
            urunler = []

            for kart in urun_kartlari:
                try:
                    urun_ismi = kart.find_element(By.CSS_SELECTOR, "h2 span").text  
                    fiyat_metin = kart.find_element(By.CLASS_NAME, "a-price-whole").text
                    sayisal_fiyat = float(fiyat_metin.replace(".", "").replace(",", "."))
                    link = kart.find_element(By.CLASS_NAME, "a-link-normal").get_attribute("href")
                    
                    if "17 pro max" in urun_ismi.lower() and min_fiyat <= sayisal_fiyat <= max_fiyat and "kılıf" not in urun_ismi.lower():
                        urunler.append({"isim": urun_ismi, "fiyat": sayisal_fiyat, "link": link})
                        print(f"uygun ürün bulundu: {urun_ismi[:40]}... - fiyat: {sayisal_fiyat} TL")
                except:
                    continue

            if urunler:
                en_ucuz = min(urunler, key=lambda x: x["fiyat"])
                print(f"En ucuz ürün: {en_ucuz['isim']} \nFiyat: {en_ucuz['fiyat']} TL")
                veriyi_kaydet(urunler)
                print("veriler 'fiyat_takip.csv' dosyasına kaydedildi")
            else:
                print("Ürün bulunamadı")
        except Exception as e:
            print(f"hata oluştu: {e}")
            
        print(f"{kontrol_araliği // 60} dakika sonra tekrar kontrol edilecek...")
        time.sleep(kontrol_araliği)
        
except KeyboardInterrupt:
    print("Program sonlandırıldı")  

finally:
    driver.quit()