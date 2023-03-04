import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import sys


def import_mm(ads_id):
    # ads_id = "XXX"
    open_url = "http://local.adspower.net:50325/api/v1/browser/start?user_id=" + ads_id
    close_url = "http://local.adspower.net:50325/api/v1/browser/stop?user_id=" + ads_id

    resp = requests.get(open_url).json()
    if resp["code"] != 0:
        print(resp["msg"])
        print("please check ads_id")
        sys.exit()

    chrome_driver = resp["data"]["webdriver"]
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
    driver = webdriver.Chrome(chrome_driver, options=chrome_options)
    print(driver.title)

    try:
        driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")

        current_window = driver.current_window_handle
        all_windows = driver.window_handles
        for window in all_windows:
            if window != current_window:
                driver.switch_to.window(window)
                driver.close()
        driver.switch_to.window(current_window)

        time.sleep(3)

    except Exception as ex:
        print(f'{ex} in profile {ads_id}')

    finally:
        driver.quit()
        requests.get(close_url)


import_mm('j5bt4qs')
