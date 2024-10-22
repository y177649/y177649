from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# デバッグモードの設定
debug_mode = False  # Trueにすると手動でブラウザを閉じるモードになる

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
    time.sleep(1)
except Exception as e:
    print(f"Error clicking filter button: {e}")

# ステップ2: 「カテゴリー」メニューを開く
try:
    category_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@data-testid='category_id']//button[@id='accordion_button']")))
    category_button.click()
    time.sleep(1)
except Exception as e:
    print(f"Error clicking category accordion button: {e}")

# ステップ3: 「ファッション」を選択
try:
    select_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select__da4764db")))
    select = Select(select_element)
    select.select_by_visible_text("ファッション")
    time.sleep(1)
except Exception as e:
    print(f"Error selecting 'ファッション': {e}")

# ステップ4: 「メンズ」を選択
try:
    men_option = wait.until(EC.presence_of_element_located((By.XPATH, "//option[text()='メンズ']")))
    men_option.click()
    time.sleep(1)
except Exception as e:
    print(f"Error selecting 'メンズ': {e}")

# ステップ5: 「ジャケット・アウター」を選択
try:
    jacket_outer_option = wait.until(EC.presence_of_element_located((By.XPATH, "//option[text()='ジャケット・アウター']")))
    jacket_outer_option.click()
    time.sleep(1)
except Exception as e:
    print(f"Error selecting 'ジャケット・アウター': {e}")

# ステップ6: 販売状況の「絞り込み」ボタンをクリック（画像1の部分）
try:
    sales_status_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='販売状況']//button[@id='accordion_button']")))
    sales_status_button.click()
    time.sleep(1)
except Exception as e:
    print(f"Error clicking '販売状況' accordion button: {e}")

# ステップ7: 「売り切れのみ」のチェックボックスをクリック（画像2の部分）
try:
    sold_out_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='sold_out|trading']")))
    sold_out_checkbox.click()
    time.sleep(1)
except Exception as e:
    print(f"Error clicking '売り切れのみ' checkbox: {e}")

# ステップ8: 検索ボックスに「barbour」を入力
try:
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='検索キーワードを入力']")))
    search_box.send_keys("barbour bedale")
    time.sleep(1)
except Exception as e:
    print(f"Error entering text into search box: {e}")

# ステップ9: エンターキーを押して検索を実行
try:
    search_box.send_keys(Keys.ENTER)
    time.sleep(3)
except Exception as e:
    print(f"Error pressing Enter key: {e}")

# スクロール処理を追加 - ゆっくりスクロールして読み込みが完了するまで待つ
scroll_pause_time = 2  # スクロール後に待つ時間（秒）
increment_scroll = 1000  # 一回のスクロール量
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # ページを少しずつスクロール
    driver.execute_script(f"window.scrollBy(0, {increment_scroll});")

    # スクロール後、商品が読み込まれるまで待機
    time.sleep(scroll_pause_time)

    # 新しいページの高さを取得
    new_height = driver.execute_script("return document.body.scrollHeight")

    # ページの高さが変わらない場合、すべてのアイテムが読み込まれたと判断
    if new_height == last_height:
        break

    last_height = new_height

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

# デバッグモードでなければブラウザを自動で閉じる
if not debug_mode:
    driver.quit()
    print("ブラウザを閉じました。")
else:
    print("デバッグモード: 手動でブラウザを閉じてください。")
    try:
        # 手動で停止させるために無限ループを設定
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("デバッグモードを終了しました。")

# 取得したURLをCSVファイルに保存
df = pd.DataFrame(item_urls, columns=['商品URL'])
df.to_csv('barbour_product_urls.csv', index=False, encoding='utf-8-sig')

print("データが 'barbour_product_urls.csv' に保存されました。")
