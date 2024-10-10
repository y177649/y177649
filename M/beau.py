from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Chromeのオプション設定
options = Options()
# options.add_argument('--headless')  # 必要であればコメントアウトして、ブラウザを表示
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

# 手動でインストールしたChromeDriverのパスを指定
driver_path = "C:/chromedriver.exe"
driver = webdriver.Chrome(service=Service(driver_path), options=options)

# メルカリの検索結果ページURL
url = 'https://www.mercari.com/jp/search/?keyword=Barbour&category=men_jacket_blouson'
driver.get(url)

# ページカウントとアイテムカウント用変数
page = 1
item_num = 0
item_urls = []

while True:
    print(f"Getting the page {page} ...")
    time.sleep(3)  # ページが完全に読み込まれるのを待機

    # 商品一覧を取得
    items = driver.find_elements(By.CLASS_NAME, "item-cell")

    for item in items:
        item_num += 1
        try:
            # 商品ページのURLを取得
            item_url = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            print(f"item{item_num} url: {item_url}")
            item_urls.append(item_url)
        except Exception as e:
            print(f"Error retrieving item URL: {e}")

    # 次のページへ進む処理（クリック方式）
    page += 1
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "li[class*='pager-next'] a")
        next_button.click()  # 次ページボタンをクリック
        print("Moving to the next page...")
    except Exception as e:
        print(f"Error moving to the next page: {e}")
        print("Last page!")
        break

# WebDriverを閉じる
driver.quit()

# 取得したURLをCSVファイルに保存
import pandas as pd

df = pd.DataFrame(item_urls, columns=['商品URL'])
df.to_csv('barbour_product_urls.csv', index=False, encoding='utf-8-sig')

print("データが 'barbour_product_urls.csv' に保存されました。")
