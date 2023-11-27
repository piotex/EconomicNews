import logging
import time
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def wait_until_elem_is_visible(driver_loc: WebDriver, x_path: str, time_out_int_sec: int = 60) -> None:
    i = 0
    while True:
        try:
            driver_loc.find_element(By.XPATH, x_path)
            return 0
        except Exception as eeee:
            time.sleep(0.1)
            i += 1
            if i > 10 * time_out_int_sec:
                raise Exception(f"==== Waiting for element longer that {time_out_int_sec}s ====")
            pass


def accept_cookies_bankier(driver_loc: WebDriver) -> None:
    yt_url = "https://www.bankier.pl/"
    driver_loc.get(yt_url)
    time.sleep(10)
    for i in [2, 4]:
        x_path = f"/html/body/div[{i}]/div[2]/div/div/div[2]/div/div/button"
        try:
            wait_until_elem_is_visible(driver_loc, x_path, 30)
            driver_loc.find_element(By.XPATH, x_path).click()
            break
        except Exception as eeee:
            pass
        driver_loc.find_element(By.XPATH, x_path).click()

def accept_cookies_youtube(driver_loc: WebDriver) -> None:
    yt_url = "https://youtube.com"
    x_path = "//*[@id=\"content\"]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]"
    driver_loc.get(yt_url)
    driver_loc.find_element(By.XPATH, x_path).click()


def scroll_to_bottom(driver: WebDriver):
    for i in range(1, 10, 1):
        driver.execute_script(f"window.scrollTo(0, {i * 1000})")
        time.sleep(0.5)

def scroll_to_xxx(driver: WebDriver, xxx: int):
    driver.execute_script(f"window.scrollTo(0, {xxx})")


def get_init_driver() -> WebDriver:
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    time.sleep(0.5)

    # driver.maximize_window()
    driver.set_window_position(0,0)

    x = 500
    y = 820 + 1000

    driver.set_window_size(x, y)
    return driver


def login(driver_loc: WebDriver, usr: str, pwd: str) -> None:
    logging.debug('login() - start')

    x_path = "/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[3]/div[2]/ytd-button-renderer/yt-button-shape/a/yt-touch-feedback-shape/div/div[2]"
    driver_loc.find_element(By.XPATH, x_path).click()
    logging.debug('login() - clicked SIGN IN')

    x_path = "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input"
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(usr)
    logging.debug('login() - inserted user name')

    x_path = "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button/span"
    driver_loc.find_element(By.XPATH, x_path).click()
    logging.debug('login() - clicked NEXT')
    time.sleep(5)

    x_path = "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(pwd)
    logging.debug('login() - inserted password')

    x_path = "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button/span"
    driver_loc.find_element(By.XPATH, x_path).click()
    logging.debug('login() - clicked NEXT')

    time.sleep(5)


def send_video(driver_loc: WebDriver, file_path, title, description, tags):
    logging.debug('send_video() - start')

    driver_loc.get("https://studio.youtube.com/")
    logging.debug('send_video() - gone to YouTube studio')

    x_path = "/html/body/ytcp-app/ytcp-entity-page/div/ytcp-header/header/div/ytcp-button/div"
    wait_until_elem_is_visible(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    logging.debug('send_video() - Clicked Create')

    x_path = "/html/body/ytcp-app/ytcp-entity-page/div/ytcp-header/header/div/ytcp-text-menu/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[1]/ytcp-ve/tp-yt-paper-item-body/div/div/div/yt-formatted-string"
    wait_until_elem_is_visible(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    logging.debug('send_video() - Clicked Send Video')

    button = driver_loc.find_element(By.XPATH, "//input[@type='file']")
    button.send_keys(file_path)
    logging.debug('send_video() - Sent file')


    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[1]/ytcp-video-title/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div"
    wait_until_elem_is_visible(driver_loc, x_path, 200)
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(Keys.CONTROL, 'a')
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(Keys.BACKSPACE)
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(title)
    logging.debug('send_video() - Inserted Title')

    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[2]/ytcp-video-description/div/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div"
    wait_until_elem_is_visible(driver_loc, x_path, 100)
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(description)
    logging.debug('send_video() - Inserted Description')

# ##############################
#    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[4]/div[3]/div[1]/ytcp-video-metadata-playlists/ytcp-text-dropdown-trigger/ytcp-dropdown-trigger/div/div[3]/tp-yt-iron-icon"
#    wait_until_elem_is_visible(driver_loc, x_path, 100)
#    driver_loc.find_element(By.XPATH, x_path).click()
# ##############################

# ##############################
#    x_path_checkbox_1 = "/html/body/ytcp-playlist-dialog/tp-yt-paper-dialog/ytcp-checkbox-group/div/ul/tp-yt-iron-list/div/ytcp-ve[1]/li/label/ytcp-checkbox-lit/div"
#    wait_until_elem_is_visible(driver_loc, x_path, 100)
#    driver_loc.find_element(By.XPATH, x_path_checkbox_1).click()
#    # x_path_checkbox_2 = "/html/body/ytcp-playlist-dialog/tp-yt-paper-dialog/ytcp-checkbox-group/div/ul/tp-yt-iron-list/div/ytcp-ve[2]/li/label/ytcp-checkbox-lit/div"
#    # driver_loc.find_element(By.XPATH, x_path_checkbox_2).click()
#    x_path = "/html/body/ytcp-playlist-dialog/tp-yt-paper-dialog/div[2]/ytcp-button[2]/div"
#    driver_loc.find_element(By.XPATH, x_path).click()
#    logging.debug('send_video() - Chose Playlist')
# ##############################

    # xpath - for children #x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]/div[1]/div[1]"
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[1]/div[1]/div[1]"
    wait_until_elem_is_visible(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    logging.debug('send_video() - Click not for children')

# ##############################
#    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/div/ytcp-button/div"
#    wait_until_elem_is_visible(driver_loc, x_path, 100)
#    driver_loc.find_element(By.XPATH, x_path).click()
#    logging.debug('send_video() - Clicked SHOW MORE')
#    time.sleep(1)

#    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[5]/ytcp-form-input-container/div[1]/div/ytcp-free-text-chip-bar/ytcp-chip-bar/div/input"
#    wait_until_elem_is_visible(driver_loc, x_path, 100)
#    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(tags)
#    logging.debug('send_video() - Sent TAGS')

#    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[6]/div[3]/ytcp-form-language-input/ytcp-form-select/ytcp-select/ytcp-text-dropdown-trigger/ytcp-dropdown-trigger/div/div[3]/tp-yt-iron-icon"
#    wait_until_elem_is_visible(driver_loc, x_path, 100)
#    driver_loc.find_element(By.XPATH, x_path).click()
#    x_path = "/html/body/ytcp-text-menu/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[16]/ytcp-ve/tp-yt-paper-item-body/div/div/div/yt-formatted-string"  # angielski (Stany Zjednoczone)
#    x_path = "/html/body/ytcp-text-menu/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[170]/ytcp-ve/tp-yt-paper-item-body/div/div/div/yt-formatted-string"  # polski
#    wait_until_elem_is_visible(driver_loc, x_path, 100)
#    driver_loc.find_element(By.XPATH, x_path).click()
#    logging.debug('send_video() - Chose Language')

#    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[10]/div[3]/ytcp-form-select/ytcp-select/ytcp-text-dropdown-trigger/ytcp-dropdown-trigger/div/div[3]/tp-yt-iron-icon"
#    wait_until_elem_is_visible(driver_loc, x_path, 100)
#    driver_loc.find_element(By.XPATH, x_path).click()
#    x_path = "/html/body/ytcp-text-menu[2]/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[15]/ytcp-ve/tp-yt-paper-item-body/div/div/div/yt-formatted-string"  # zwierzeta
#    wait_until_elem_is_visible(driver_loc, x_path, 100)
#    driver_loc.find_element(By.XPATH, x_path).click()
#    logging.debug('send_video() - Chose Video Category')
# ##############################

    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div"
    wait_until_elem_is_visible(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    logging.debug('send_video() - Clicked NEXT')

    # napisy | subtitles

    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div"
    wait_until_elem_is_visible(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    logging.debug('send_video() - Clicked NEXT')

    # weryfikacja

    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div"
    wait_until_elem_is_visible(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    logging.debug('send_video() - Clicked NEXT')

    # widocznosc

    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[3]/div[1]/div[1]"  # publiczny
    wait_until_elem_is_visible(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    logging.debug('send_video() - Clicked NEXT')

    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[3]/div"
    wait_until_elem_is_visible(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    logging.debug('send_video() - Clicked PUBLISH')

    # x_path = "/html/body/ytcp-uploads-still-processing-dialog/ytcp-dialog/tp-yt-paper-dialog/div[3]/ytcp-button/div"
    x_path = "/html/body/ytcp-video-share-dialog/ytcp-dialog/tp-yt-paper-dialog/div[3]/ytcp-button/div"
    wait_until_elem_is_visible(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    logging.debug('send_video() - Clicked Close')
