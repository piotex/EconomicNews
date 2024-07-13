import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from news_model import *
from selenium.webdriver.common.by import By
import time


def get_init_driver() -> WebDriver:
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    time.sleep(0.5)
    driver.maximize_window()
    return driver


def wait_for_element(driver: WebDriver, x_path: str, max_wait_time_s: float):
    max_wait_time_s *= 100
    for time_s in range(1, int(max_wait_time_s), 1):
        try:
            driver.find_element(By.XPATH, x_path)
            return 0
        except:
            pass
        time.sleep(1 / 100)
    return 1


def close_advertisement(driver: WebDriver):
    x_path_list = [
        "/html/body/div[1]/div[7]",
        "/html/body/div[1]/div[2]",
        "/html/body/div[1]/header",
        "/html/body/div[1]/div[3]/aside[1]",
        "/html/body/div[1]/div[4]/aside[1]",
        "/html/body/div[1]/div[3]/main/article/section/div[1]",
        "/html/body/div[1]/div[4]/main/article/section/section[2]",
        "/html/body/div[1]/div[3]/main/article/section/section[2]",
    ]

    for x_path in x_path_list:
        try:
            element = driver.find_element(By.XPATH, x_path)
            driver.execute_script(f"arguments[0].setAttribute('style', 'display: none')", element)
            time.sleep(0.5)
        except:
            pass


def open_news_full_width(driver: WebDriver):
    x_path_list = [
        "/html/body/div[1]/div[3]/main",
        "/html/body/div[1]/div[4]/main",
    ]
    for x_path in x_path_list:
        try:
            element = driver.find_element(By.XPATH, x_path)
            driver.execute_script(f"arguments[0].setAttribute('style', 'width: 100%')", element)
            time.sleep(0.5)
        except:
            pass


def close_break_message(driver: WebDriver):
    x_path = "/html/body/div[1]/div[7]"
    wait_for_element(driver, x_path, 10)
    try:
        driver.find_element(By.XPATH, x_path).click()
    except:
        pass


def close_cookies(driver: WebDriver):
    for i in range(1, 15):
        x_path = f"/html/body/div[{i}]/div[2]/div/div/div[2]/div/div/button"
        try:
            driver.find_element(By.XPATH, x_path).click()
            return 0
        except:
            pass


def find_xpath_idx(driver: WebDriver):
    for i in range(1, 15, 1):
        x_path = f"/html/body/div[1]/div[{i}]/main/article/header"
        try:
            driver.find_element(By.XPATH, x_path)
            return i
        except:
            pass
    raise Exception("=== Can't find idx ===")


def make_screenshots(driver: WebDriver):
    css_updates = "'padding: 15px;font-size: 30px;'"
    idx = find_xpath_idx(driver)

    x_paths = [
        f"/html/body/div[1]/div[{idx}]/main/article/header",
        f"/html/body/div[1]/div[{idx}]/main/article/section/p[1]",
        f"/html/body/div[1]/div[{idx}]/main/article/section/p[2]",
        f"/html/body/div[1]/div[{idx}]/main/article/section/p[3]",
        f"/html/body/div[1]/div[{idx}]/main/article/section/p[4]",
        f"/html/body/div[1]/div[{idx}]/main/article/section/p[5]",
        f"/html/body/div[1]/div[{idx}]/main/article/section/p[6]",
        f"/html/body/div[1]/div[{idx}]/main/article/section/p[7]",
        # f"/html/body/div[1]/div[{idx}]/main/article/section",
    ]
    for i, x_path in enumerate(x_paths):
        screenshot_path = f"data/images/screenshots/screenshot-{i + 1}.png"
        try:
            element = driver.find_element(By.XPATH, x_path)
            driver.execute_script(f"arguments[0].setAttribute('style', {css_updates})", element)
            driver.find_element(By.XPATH, x_path).screenshot(screenshot_path)
        except:
            pass


def main():
    model = load_obj()
    driver = get_init_driver()
    driver.get(model.url)
    time.sleep(1)
    close_cookies(driver)
    close_break_message(driver)
    close_advertisement(driver)
    open_news_full_width(driver)
    make_screenshots(driver)


if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    total_s = end_time - start_time
    total_m = int(total_s / 60)
    total_s = int(total_s - total_m * 60)
    print(f"")
    print(f"#####################################")
    print(f"Total time: {total_m}m {total_s}s")
    print(f"#####################################")
