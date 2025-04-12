# -*- coding: utf-8 -*-
import requests
import csv
import time

# 1. 目標 API：使用 JSONPlaceholder 提供的 posts 端點 (提供 100 筆測試文章資料)
API_URL = "https://jsonplaceholder.typicode.com/posts"

def fetch_api_data():
    """
    向 API 發送 GET 請求並回傳 JSON 格式資料。
    """
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()  # 若 HTTP 回傳錯誤則拋出例外
        data = response.json()  # 將回傳內容轉成 JSON（Python 的 list/dict）
        print(f"成功取得 {len(data)} 筆 API 資料")
        return data
    except Exception as e:
        print(f"API 資料抓取失敗： {str(e)}")
        return []

def save_to_csv(data, filename="api.csv"):
    """
    將抓取到的資料存成 CSV 檔案，輸出欄位包括 userId, id, title, body。
    """
    fieldnames = ["userId", "id", "title", "body"]
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                writer.writerow({
                    "userId": item.get("userId", "N/A"),
                    "id": item.get("id", "N/A"),
                    "title": item.get("title", "N/A"),
                    "body": item.get("body", "N/A")
                })
        print(f"✅ 成功寫入 {filename}，共 {len(data)} 筆資料")
    except Exception as e:
        print(f"寫入 CSV 失敗：{str(e)}")

def main():
    # 抓取 API 資料
    data = fetch_api_data()
    
    # 模擬延遲，避免快速重複請求
    time.sleep(2)
    
    # 儲存資料至 CSV 檔案
    save_to_csv(data)

if __name__ == "__main__":
    main()
