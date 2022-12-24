import sched, time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.keys import Keys

import setting


def get_driver():
    chrome_service = service.Service(executable_path=setting.CHROME_DRIVER_PATH) 
    options = webdriver.ChromeOptions()
    options.add_argument(f'service={chrome_service}')
    options.add_extension(setting.LINE_EXTENSION_PATH)      # LINE拡張機能を追加。
    driver = webdriver.Chrome(options=options)

    return driver


def login(driver):
    page_url = "chrome-extension://ophjlpahpchlmihnnnihgmmeilfjmjjc/index.html"
    driver.get(page_url)
    time.sleep(2)

    driver.find_element_by_css_selector(".MdBtn03D01.mdBtn03S._layer_left").click()
    driver.find_element_by_id("line_login_email").send_keys(setting.USER_ID)
    driver.find_element_by_id("line_login_pwd").send_keys(setting.USER_PASSWORD)
    driver.find_element_by_id("login_btn").click()

    time.sleep(15)


def send_message(driver, user_name):
    # ユーザ検索
    driver.find_element_by_id("search_input").clear()
    driver.find_element_by_id("search_input").send_keys(user_name)
    time.sleep(0.5)
    driver.find_element_by_css_selector(".MdColorMark").click()

    # メッセージ送信
    for message in setting.MESSAGE_TEXT_LIST:
        driver.find_element_by_id("_chat_room_input").send_keys(message)
        driver.find_element_by_id("_chat_room_input").send_keys(Keys.ENTER)
    time.sleep(0.5)


def send_messages(driver):
    for user_name in setting.DESTINATION_USERNAME_LIST:
        send_message(driver, user_name)


if __name__ == "__main__":
    driver = get_driver()
    login(driver)

    driver.find_element_by_css_selector(".mdLFT07Friends").click()
    time.sleep(1)


    # 指定した時間まで待機。
    now = datetime.now()
    diff = setting.SEND_TIME - now
    
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(diff.seconds, 1, send_messages, (driver, ))
    scheduler.run()
