import random
from unidecode import unidecode
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from news_model import *
from seleniumbase import Driver
from selenium.webdriver.common.keys import Keys
import time


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


def get_init_driver() -> WebDriver:
    driver = Driver(uc=True)
    time.sleep(0.5)
    driver.maximize_window()
    time.sleep(0.5)
    return driver


def go_to_home_page(driver_loc: WebDriver):
    yt_url = "https://chatgpt.com/"
    driver_loc.get(yt_url)
    # print("\n\nWaiting for captcha to be solved...\n\n")
    # a = input()


def click_sign_in(driver_loc: WebDriver):
    x_path = "/html/body/div[1]/div[1]/div[2]/div[1]/div/div/button[1]"
    wait_for_element(driver_loc, x_path, 10)
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)


def insert_email(driver_loc: WebDriver):
    with open("../../secrets/chatgpt.pwd", "r", encoding="utf-8") as f:
        lines = f.readlines()
    usr = lines[0] if "\n" in lines[0] else lines[0] + "\n"
    x_path = "/html/body/div/div/main/section/div[2]/div[1]/input"  # email input
    wait_for_element(driver_loc, x_path, 10)
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(usr)
    time.sleep(2)


def insert_password(driver_loc: WebDriver):
    with open("../../secrets/chatgpt.pwd", "r", encoding="utf-8") as f:
        lines = f.readlines()
    pwd = lines[1] if "\n" in lines[1] else lines[1] + "\n"
    x_path = "/html/body/div[1]/main/section/div/div/div/form/div[1]/div/div[2]/div/input"  # pwd input
    wait_for_element(driver_loc, x_path, 10)
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(pwd)
    time.sleep(5)

    x_path = "/html/body/div[4]/div/div/div/div[2]/div/div[2]/button"
    x_path = "/html/body/div[5]/div/div/div/div[1]/button"


def set_input_text_and_go(driver_loc: WebDriver, input_text: str):
    if "\n" not in input_text:
        input_text += "\n"
    x_path = "/html/body/div[1]/div[1]/div[2]/main/div[1]/div[2]/div[1]/div/form/div/div[2]/div/div/div[2]/textarea"
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(input_text.replace("\n",""))
    time.sleep(random.uniform(1, 3))
    x_path = "/html/body/div[1]/div[1]/div[2]/main/div[1]/div[2]/div[1]/div/form/div/div[2]/div/div/button"
    driver_loc.find_element(by=By.XPATH, value=x_path).click()
    time.sleep(5)

    # for c in input_text:
    #     driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(c)
    #     driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(Keys.ARROW_RIGHT)
    #     time.sleep(random.uniform(0.001, 0.005))


def get_x_start(driver_loc: WebDriver):
    x_start_l = [
        "/html/body/div[1]/div[1]/div[2]/main",
        "/html/body/div[1]/div[1]/div/main"
    ]
    for x_start in x_start_l:
        driver_loc.find_element(By.XPATH, x_start)
        return x_start

def get_all_parsed_text(driver_loc: WebDriver):
    old_text = ".."
    while True:
        x_path = f"{get_x_start(driver_loc)}/div[1]/div[1]/div/div/div/div/div[3]/div/div/div[2]/div/div[1]/div/div/div"
        wait_for_element(driver_loc, x_path, 120)
        new_text = driver_loc.find_element(By.XPATH, x_path).get_attribute("innerText")
        if len(new_text) > len(old_text):
            old_text = new_text
        else:
            return old_text
def get_all_description_text(driver_loc: WebDriver):
    old_text = ".."
    while True:
        x_path = f"{get_x_start(driver_loc)}/div[1]/div[1]/div/div/div/div/div[5]/div/div/div[2]/div/div[1]/div/div/div"
        wait_for_element(driver_loc, x_path, 120)
        new_text = driver_loc.find_element(By.XPATH, x_path).get_attribute("innerText")
        if len(new_text) > len(old_text):
            old_text = new_text
        else:
            return old_text
def get_all_tags_text(driver_loc: WebDriver):
    old_text = ".."
    while True:
        x_path = f"{get_x_start(driver_loc)}/div[1]/div[1]/div/div/div/div/div[7]/div/div/div[2]/div/div[1]/div/div/div"
        wait_for_element(driver_loc, x_path, 120)
        new_text = driver_loc.find_element(By.XPATH, x_path).get_attribute("innerText")
        if len(new_text) > len(old_text):
            old_text = new_text
        else:
            return old_text
def get_all_title_text(driver_loc: WebDriver):
    old_text = ".."
    while True:
        x_path = f"{get_x_start(driver_loc)}/div[1]/div[1]/div/div/div/div/div[9]/div/div/div[2]/div/div[1]/div/div/div"
        wait_for_element(driver_loc, x_path, 120)
        new_text = driver_loc.find_element(By.XPATH, x_path).get_attribute("innerText")
        if len(new_text) > len(old_text):
            old_text = new_text
        else:
            return old_text


def get_chatgpt_input() -> list[str]:
    with open("data/urls/input_for_chatgpt.txt", "r", encoding="utf-8") as f:
        return f.readlines()


def parse_text_with_polish_special_char(in_str: str):
    in_str_c = in_str.replace('\r','').replace('\n','')
    return unidecode(in_str_c)

def __parse_tags(tags: str):
    if "," in tags and "#" not in tags:
        return tags

    if "\n" in tags:
        tags = tags.replace('\n',',')
    if "," not in tags:
        tags = tags.replace(' ',',')
    if "#" in tags:
        tags = tags.replace('#','')
    return tags

def limit_words(in_text: str):
    limit = 100
    list_txt = in_text.split(" ")
    res_txt = ""
    counter = 0
    for a in list_txt:
        if counter >= limit:
            return res_txt
        counter += 1
        res_txt += a + " "
    return res_txt


def main():
    model = load_obj()
    [parse_text, description_text, tags_text, title_text] = get_chatgpt_input()
    parse_text = parse_text_with_polish_special_char(parse_text+model.article_text[:3000])
    description_text = parse_text_with_polish_special_char(description_text)
    tags_text = parse_text_with_polish_special_char(tags_text)
    title_text = parse_text_with_polish_special_char(title_text)

    driver = get_init_driver()
    go_to_home_page(driver)
    click_sign_in(driver)
    insert_email(driver)
    insert_password(driver)

    set_input_text_and_go(driver, parse_text)
    time.sleep(10)
    model.parsed_text = get_all_parsed_text(driver)
    model.parsed_text = limit_words(model.parsed_text)
    save_obj(model)
    time.sleep(1)

    set_input_text_and_go(driver, description_text)
    time.sleep(5)
    model.description_text = get_all_description_text(driver)
    save_obj(model)
    time.sleep(1)

    set_input_text_and_go(driver, tags_text)
    time.sleep(5)
    model.tags_text = get_all_tags_text(driver)
    model.tags_text = __parse_tags(model.tags_text)
    save_obj(model)
    time.sleep(1)

    set_input_text_and_go(driver, title_text)
    time.sleep(3)
    model.title_text = get_all_title_text(driver)
    save_obj(model)

    driver.close()


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
