from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Chromeのオプション設定
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

# 手動でインストールしたChromeDriverのパスを指定
driver_path = "C:/chromedriver.exe"
driver = webdriver.Chrome(service=Service(driver_path), options=options)

# メルカリの検索ページを開く
url = 'https://jp.mercari.com/search'
driver.get(url)

# 無限ループでブラウザを開いたままにしておく
try:
    print("メルカリのサイトが開かれました。デバッグが終了したら手動でブラウザを閉じてください。")
    while True:
        time.sleep(10)  # 10秒ごとにループを繰り返す
except KeyboardInterrupt:
    print("デバッグモードを終了しました。")
finally:
    driver.quit()
    print("ブラウザを閉じました。")
