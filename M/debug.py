from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

driver_path = "C:/chromedriver.exe"
driver = webdriver.Chrome(service=Service(driver_path), options=options)

# メルカリの検索ページを開く
url = 'https://jp.mercari.com/search'
driver.get(url)
wait = WebDriverWait(driver, 10)

# ステップ1: 「絞り込み」ボタンをクリック
try:
    filter_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='絞り込み']")))
    filter_button.click()
    time.sleep(1)  # ページが反応するのを待つ
except Exception as e:
    print(f"Error clicking filter button: {e}")

# ステップ2: 「カテゴリー」メニューを開く
try:
    category_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@data-testid='category_id']//button[@id='accordion_button']")))
    category_button.click()
    time.sleep(1)  # ページが反応するのを待つ
except Exception as e:
    print(f"Error clicking category accordion button: {e}")

# ステップ3: 「ファッション」を選択
try:
    select_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select__da4764db")))
    select = Select(select_element)
    select.select_by_visible_text("ファッション")
    time.sleep(1)  # ページが反応するのを待つ
except Exception as e:
    print(f"Error selecting 'ファッション': {e}")

# ステップ4: 「メンズ」を選択
try:
    men_option = wait.until(EC.presence_of_element_located((By.XPATH, "//option[text()='メンズ']")))
    men_option.click()
    time.sleep(1)  # ページが反応するのを待つ
except Exception as e:
    print(f"Error selecting 'メンズ': {e}")

# ステップ5: 「ジャケット・アウター」を選択
try:
    jacket_outer_option = wait.until(EC.presence_of_element_located((By.XPATH, "//option[text()='ジャケット・アウター']")))
    jacket_outer_option.click()
    time.sleep(1)  # ページが反応するのを待つ
except Exception as e:
    print(f"Error selecting 'ジャケット・アウター': {e}")

# ステップ4: 「検索する」ボタンをクリック
try:
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='検索する']")))
    search_button.click()
    time.sleep(3)  # 結果ページの読み込みを待つ
except Exception as e:
    print(f"Error clicking search button: {e}")

# 検索結果のアイテムを取得
items = driver.find_elements(By.CLASS_NAME, "sc-bcd1c877-2.cvAXgx")

print(f"Found {len(items)} items with the class 'sc-bcd1c877-2 cvAXgx'.")

item_urls = []
item_num = 0
for item in items:
    item_num += 1
    try:
        item_url = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        print(f"item{item_num} url: {item_url}")
        item_urls.append(item_url)
    except Exception as e:
        print(f"Error retrieving item URL: {e}")

# デバッグ用のコード：ブラウザを開いたままにする
try:
    print("メルカリのサイトが開かれています。デバッグが終了したら手動でブラウザを閉じてください。")
    while True:
        time.sleep(10)  # 10秒ごとにループを繰り返す
except KeyboardInterrupt:
    print("デバッグモードを終了しました。")
finally:
    driver.quit()
    print("ブラウザを閉じました。")

# 取得したURLをCSVファイルに保存
df = pd.DataFrame(item_urls, columns=['商品URL'])
df.to_csv('barbour_product_urls.csv', index=False, encoding='utf-8-sig')

print("データが 'barbour_product_urls.csv' に保存されました。")
