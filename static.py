# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = "https://www.rakuya.com.tw/rent/rent_search?search=city&city=4&zipcode=320&upd=1&page={}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.rakuya.com.tw/"
}

def main():
    houses = []
    total_pages = 37  # 根據實際頁數設定
    
    for page in range(1, total_pages + 1):
        url = base_url.format(page)
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # 檢查 HTTP 錯誤
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 提取資料
            for item in soup.select("div.obj-info"):
                title = item.select_one("div.obj-title a").text.strip() if item.select_one("div.obj-title a") else "N/A"
                address = item.select_one("p.obj-address").text.strip() if item.select_one("p.obj-address") else "N/A"
                price = item.select_one("li.obj-price span").text.strip().replace(",", "") if item.select_one("li.obj-price span") else "N/A"
                houses.append({"title": title, "price": price, "address": address})
            
            print(f"第 {page} 頁抓取成功，累計 {len(houses)} 筆資料")
            time.sleep(2)  # 降低請求頻率
        
        except Exception as e:
            print(f"第 {page} 頁抓取失敗：{str(e)}")
            continue
    
    # 輸出 CSV
    with open("static.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "address"])
        writer.writeheader()
        writer.writerows(houses)
    
    print(f"所有資料已保存至 static.csv，總計 {len(houses)} 筆")

if __name__ == "__main__":
    main()