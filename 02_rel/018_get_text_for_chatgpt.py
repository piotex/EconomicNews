import time

from news_model import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from news_model import *
from seleniumbase import Driver
from selenium.webdriver.common.keys import Keys


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


def go_to_gemini_and_wait_for_captcha_to_be_solved(driver_loc: WebDriver):
    yt_url = "https://chatgpt.com/"
    driver_loc.get(yt_url)
    # print("\n\nWaiting for captcha to be solved...\n\n")
    # a = input()


def accept_cookies_youtube(driver_loc: WebDriver) -> None:
    # x_path = "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button/span"  # accept
    # x_path = "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[1]/div/div/button"  # not accept
    # wait_for_element(driver_loc, x_path, 10)
    # driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)


def click_sign_in(driver_loc: WebDriver):
    x_path = "/html/body/div[1]/div[1]/div[2]/div[1]/div/div/button[1]"
    wait_for_element(driver_loc, x_path, 10)
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)


def insert_email(driver_loc: WebDriver):
    with open("../../secrets/chatgpt.pwd", "r", encoding="utf-8") as f:
        lines = f.readlines()
    usr = lines[0]
    x_path = "/html/body/div/div/main/section/div[2]/div[1]/input"  # email input
    wait_for_element(driver_loc, x_path, 10)
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(usr)
    time.sleep(2)


def insert_password(driver_loc: WebDriver):
    with open("../../secrets/chatgpt.pwd", "r", encoding="utf-8") as f:
        lines = f.readlines()
    pwd = lines[1]
    x_path = "/html/body/div[1]/main/section/div/div/div/form/div[1]/div/div[2]/div/input"  # pwd input
    wait_for_element(driver_loc, x_path, 10)
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(pwd)
    time.sleep(10)

    x_path = "/html/body/div[4]/div/div/div/div[2]/div/div[2]/button"
    x_path = "/html/body/div[5]/div/div/div/div[1]/button"


def click_new_chat_icon(driver_loc: WebDriver):
    # x_path = "/html/body/chat-app/main/side-navigation-v2/bard-sidenav-container/bard-sidenav/div/div/div[1]/div/expandable-button/button"  # new chat button
    # wait_for_element(driver_loc, x_path, 10)
    # try:
    #     driver_loc.find_element(By.XPATH, x_path).click()
    # except:
    #     pass
    time.sleep(1)

def slice_text(input_text:str):
    text_len = 50
    parts = [input_text[0:text_len-1]]
    i = 1
    while len(parts[-1]) == text_len-1:
        parts.append(input_text[i*text_len:(i+1)*text_len-1])
        i += 1
    return parts

# def make_input_bigger(driver_loc: WebDriver):
#     x_path = "/html/body/chat-app/main/side-navigation-v2/bard-sidenav-container/bard-sidenav-content/div/div/div[2]/chat-window/div[1]/div[2]/div[1]/input-area-v2/div/div"
#     wait_for_element(driver_loc, x_path, 10)
#     element = driver_loc.find_element(By.XPATH, x_path)
#     driver_loc.execute_script(f"arguments[0].setAttribute('style', 'height: 500px')", element)

def set_input_text_and_go(driver_loc: WebDriver, input_text: str):
    x_path = "/html/body/div[1]/div[1]/div[2]/main/div[1]/div[2]/div[1]/div/form/div/div[2]/div/div/div[2]/textarea"
    # driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(Keys.CONTROL, 'a')
    # driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(Keys.BACKSPACE)
    sliced = slice_text(input_text)
    # driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(input_text)
    for text in sliced:
        for c in text:
            driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(c)
            driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(Keys.ARROW_RIGHT)
            time.sleep(0.005)
        # driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(Keys.LEFT_SHIFT+Keys.ENTER)
    time.sleep(1)


def get_output_text(driver_loc: WebDriver):
    x_path = "/html/body/div[1]/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/div[3]/div/div/div[2]"
    wait_for_element(driver_loc, x_path, 10)
    result = driver_loc.find_element(By.XPATH, x_path).get_attribute("innerText")
    time.sleep(1)
    return result


def get_all_output_text(driver_loc: WebDriver):
    old_text = ".."
    while True:
        new_text = get_output_text(driver_loc)
        if len(new_text) > len(old_text):
            old_text = new_text
        else:
            return old_text


def main():
    txt = "Streść poniższy artykuł, tak, żeby dobrze się tego słuchało na TikTok. Chcę, żebyś wybrał najciekawsze wątki z całego materiału i podsumował je w angażujący sposób do 5 zdań maksymalnie. Unikaj zbędnych przymiotników. Przedstaw poniższe informacje w rzetelny, obiektywny i angażujący widza TikToka sposób."""
    obj_list = load_obj_list()
    model = obj_list[0]
    model.gemini_in_text = txt + model.article_text.replace("\n","").replace("\r","") + "\n"

    driver = get_init_driver()
    go_to_gemini_and_wait_for_captcha_to_be_solved(driver)
    click_sign_in(driver)
    insert_email(driver)
    insert_password(driver)
    # accept_cookies_youtube(driver)
    # click_new_chat_icon(driver)
    set_input_text_and_go(driver, model.gemini_in_text)
    time.sleep(10)
    model.gemini_out_text = get_all_output_text(driver)

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
