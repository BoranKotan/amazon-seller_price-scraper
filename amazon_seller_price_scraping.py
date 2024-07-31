import pandas as pd
from bs4 import BeautifulSoup
import requests
import time  # Zamanlayıcı için ekledik

# Excel'de birinci sütuna eklediğiniz tüm amazon ürün urllerine giderek ürünün satıcısını ve ürünün satış fiyatını belirteceğiniz excel dosyasına yazar. 
# AMAZON FİYAT VE SATICI SCRAPER TOOL.



# Excel dosyasından URL'leri okuyun
excel_file = 'urller2.xlsx'  # Dosya adını burada belirtin
df = pd.read_excel(excel_file)

# URL'leri ilk sütundan bir listeye alın
urls = df.iloc[:, 0].tolist()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0"
}

# Verileri saklamak için boş bir liste oluşturun
data = []

# URL havuzundaki her bir URL için işlemleri yap
for url in urls:
    try:
        # Her işlemden önce 5 saniye bekle
        time.sleep(5)
        
        page = requests.get(url, headers=headers)
        soup1 = BeautifulSoup(page.content, "html.parser")
        soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

        price_element = soup2.find(class_='a-price-whole')
        if price_element:
            price_text = price_element.get_text().strip()
            price = int(price_text[:4])  # İlk 4 karakteri al ve int yap
        else:
            price = None

        seller_element = soup2.find(id='sellerProfileTriggerId')
        if seller_element:
            seller = seller_element.get_text().strip()
        else:
            seller = None

        data.append([url, seller, price])
    except Exception as e:
        print(f"Error processing {url}: {e}")

# Verileri bir DataFrame'e dönüştürün
df_output = pd.DataFrame(data, columns=['URL', 'Seller', 'Price'])

# DataFrame'i bir Excel dosyasına yazın
df_output.to_excel('ornek1.xlsx', index=False)

