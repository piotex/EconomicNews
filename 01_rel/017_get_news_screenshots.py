import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from news_model import *


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
        "/html/body/div[1]/div[3]/main/article/section/div[1]"
    ]

    for x_path in x_path_list:
        try:
            element = driver.find_element(By.XPATH, x_path)
            driver.execute_script(f"arguments[0].setAttribute('style', 'display: none')", element)
            time.sleep(0.5)
        except:
            pass


def close_break_message(driver: WebDriver):
    x_path = "/html/body/div[1]/div[7]"
    wait_for_element(driver, x_path, 30)


def close_cookies(driver: WebDriver):
    x_path = "/html/body/div[6]/div[2]/div/div/div[2]/div/div/button"
    x_path = "/html/body/div[6]/div[2]/div/div/div[2]/div/div/button"
    wait_for_element(driver, x_path, 10)
    driver.find_element(By.XPATH, x_path).click()


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


def main():
    obj_list = load_obj_list()
    driver = get_init_driver()
    for i in range(2):
        try:
            driver.get(obj_list[0].url)
            close_cookies(driver)
            close_break_message(driver)
            break
        except:
            pass
    m_obj = obj_list[0]
    m_obj.img_dir_path = f"../data/screen_shots"
    driver.get(m_obj.url)
    time.sleep(1)
    close_advertisement(driver)
    open_news_full_width(driver)
    screenshot_path = f"data\\screen_shots\\0-screen-{m_obj.idx}.png"
    screenshot = driver.save_screenshot(screenshot_path)
    if not screenshot:
        raise Exception("Didn't create snapshot")
    save_obj_list(obj_list)


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
