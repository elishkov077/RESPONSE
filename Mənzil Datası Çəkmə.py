import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://bina.az/baki/alqi-satqi/menziller?price_from=30000&price_to=80000&room_ids%5B%5D=2&room_ids%5B%5D=3'
head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}
liste = []

def web_scrapy(sehife):
    base_url = f"{url}&page={sehife}"
    response = requests.get(base_url,headers=head)
    if response.status_code == 200:
        html = BeautifulSoup(response.text,"html.parser")
        data = html.find_all("div",class_ = "items-i")
        for veri in data:
            erazi = veri.find("div",class_ = "location").text.strip()
            price = veri.find("span",class_ = "price-val").text.strip()
            replace = price.replace(" ","")
            qiymet = int(replace)
            qeydler = veri.find("ul",class_ = "name")
            otaqlar = qeydler("li")[0].text.strip()
            linkler = veri.find("a")["href"]
            link = f"https://bina.az{linkler}"
            liste.append((erazi,qiymet,otaqlar,link))
            print(erazi,qiymet,otaqlar,link)

for page in range(1,9):
    print("_" * 40)
    print(f"\nSehife : {page}")
    web_scrapy(page)   

df = pd.DataFrame(liste,columns=["ERAZI","QIYMET","OTAQ","LINK"])
df.to_excel("menzildata.xlsx",index=False)
print("Melumat Yuklenildi.....")
