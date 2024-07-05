import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from unidecode import unidecode

from news_model import *
from seleniumbase import Driver
from selenium.webdriver.common.keys import Keys

obj_list_path = "../data/obj_list.json"


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
def accept_cookies_youtube(driver_loc: WebDriver) -> None:
    yt_url = "https://youtube.com"
    driver_loc.get(yt_url)
    x_path = "//*[@id=\"content\"]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]"
    wait_for_element(driver_loc,x_path,10)
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(10)

def insert_email(driver_loc: WebDriver):
    with open("../../secrets/youtube.pwd", "r", encoding="utf-8") as f:
        lines = f.readlines()
    usr = lines[0]
    x_path = "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input"         # email input
    wait_for_element(driver_loc,x_path,10)
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(usr)
    time.sleep(5)
def insert_password(driver_loc: WebDriver):
    with open("../../secrets/youtube.pwd", "r", encoding="utf-8") as f:
        lines = f.readlines()
    pwd = lines[1]
    x_path = "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"  # pwd input
    wait_for_element(driver_loc,x_path,10)
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(pwd)
    time.sleep(5)

def click_sign_in(driver_loc: WebDriver):
    x_path = "/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[3]/div[2]/ytd-button-renderer/yt-button-shape/a/yt-touch-feedback-shape/div/div[2]"
    wait_for_element(driver_loc,x_path,10)
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)

def click_proceed_after_login(driver_loc: WebDriver):
    x_path = "/html/body/div[1]/div[1]/div[2]/div/div/div[3]/div/div[2]/div/div/button/span"        # not now button for easier login
    wait_for_element(driver_loc,x_path,10)
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(3)

def go_to_youtube_studio(driver_loc: WebDriver):
    driver_loc.get("https://studio.youtube.com/")
    time.sleep(1)

def click_create_button(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-app/ytcp-entity-page/div/ytcp-header/header/div/ytcp-button"
    wait_for_element(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()

def click_send_file(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-app/ytcp-entity-page/div/ytcp-header/header/div/ytcp-text-menu/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[1]/ytcp-ve/tp-yt-paper-item-body/div/div/div/yt-formatted-string"
    # x_path = "/html/body/ytcp-app/ytcp-entity-page/div/ytcp-header/header/div/ytcp-text-menu/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[1]/ytcp-ve/tp-yt-paper-item-body/div/div/div/yt-formatted-string"
    # x_path = "/html/body/ytcp-app/ytcp-entity-page/div/ytcp-header/header/div/ytcp-text-menu/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[1]/ytcp-ve/tp-yt-iron-icon"
    wait_for_element(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
def send_file_from_disk(driver_loc: WebDriver):
    button = driver_loc.find_element(By.XPATH, "//input[@type='file']")
    file_path = "data/result.mp4"
    file_path = os.path.abspath(file_path)
    button.send_keys(file_path)
    time.sleep(10)
def insert_video_title(driver_loc: WebDriver, title: str):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[1]/ytcp-video-title/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div"
    wait_for_element(driver_loc, x_path, 200)
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(Keys.CONTROL, 'a')
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(Keys.BACKSPACE)
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(title)
def insert_video_description(driver_loc: WebDriver, description: str):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[2]/ytcp-video-description/div/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div"
    wait_for_element(driver_loc, x_path, 100)
    # driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(description)
    for c in description:
        driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(c)
        driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(Keys.ARROW_RIGHT)
        time.sleep(random.uniform(0.001, 0.005))
def select_playlist(driver_loc: WebDriver):
    playlist_idx = 1
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[4]/div[3]/div[1]/ytcp-video-metadata-playlists/ytcp-text-dropdown-trigger/ytcp-dropdown-trigger/div/div[3]/tp-yt-iron-icon"
    wait_for_element(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(0.5)
    x_path_checkbox_1 = f"/html/body/ytcp-playlist-dialog/tp-yt-paper-dialog/ytcp-checkbox-group/div/ul/tp-yt-iron-list/div/ytcp-ve[{playlist_idx}]/li/label/ytcp-checkbox-lit/div"
    wait_for_element(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path_checkbox_1).click()
    time.sleep(0.5)
    x_path = "/html/body/ytcp-playlist-dialog/tp-yt-paper-dialog/div[2]/ytcp-button[2]/div"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(0.5)

def select_not_for_kids(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[1]/div[1]/div[1]" # for kids
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]/div[1]/div[1]" # not for kids
    wait_for_element(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
def click_show_more(driver_loc: WebDriver):
    for i in range(1, 10, 1):
        driver_loc.execute_script(f"window.scrollTo(0, {i * 1000})")
        time.sleep(0.5)
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/div/ytcp-button/div"
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/div/ytcp-button/ytcp-button-shape/button"
    wait_for_element(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
    for i in range(1, 10, 1):
        driver_loc.execute_script(f"window.scrollTo(0, {i * 1000})")
        time.sleep(0.5)

def click_my_video_contain_paid_promotion(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[1]/ytcp-checkbox-lit/div/div[1]/div/div/div"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
def click_video_is_unedited_with_ai(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[2]/ytkp-altered-content-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]/div[1]"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
def click_automatic_chapters(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[3]/ytcp-form-checkbox/ytcp-checkbox-lit/div/div[1]/div/div/div"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
def click_allow_mentioned_places(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[4]/ytcp-checkbox-lit/div/div[1]/div/div/div"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
def click_automatic_concepts(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[5]/ytcp-form-checkbox/ytcp-checkbox-lit/div/div[1]/div/div/div"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
def set_tags(driver_loc: WebDriver, tags: str):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[5]/ytcp-form-input-container/div[1]/div/ytcp-free-text-chip-bar/ytcp-chip-bar/div/input"
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[6]/ytcp-form-input-container/div[1]/div/ytcp-free-text-chip-bar/ytcp-chip-bar/div/input"
    wait_for_element(driver_loc, x_path, 100)
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(tags)
def set_language(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[7]/div[3]/ytcp-form-language-input/ytcp-form-select/ytcp-select/ytcp-text-dropdown-trigger/ytcp-dropdown-trigger/div/div[3]/tp-yt-iron-icon"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
    x_path = "/html/body/ytcp-text-menu/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[170]/ytcp-ve/tp-yt-paper-item-body/div/div/div/yt-formatted-string"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
def click_not_published_in_usa_tv(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[7]/div[3]/ytcp-form-select/ytcp-select/ytcp-text-dropdown-trigger/ytcp-dropdown-trigger/div/div[3]/tp-yt-iron-icon"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
    x_path = "/html/body/ytcp-text-menu[2]/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[2]/ytcp-ve/tp-yt-paper-item-body/div/div/div/yt-formatted-string"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
def click_todays_date(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[8]/div[3]/div/ytcp-text-dropdown-trigger/ytcp-dropdown-trigger/div/div[3]/tp-yt-iron-icon"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
    x_path = "/html/body/ytcp-date-picker/tp-yt-paper-dialog/ytcp-scrollable-calendar/div/tp-yt-iron-list/div/div[2]/div[6]/span[5]" # 28-06-24
    x_path = "/html/body/ytcp-date-picker/tp-yt-paper-dialog/ytcp-scrollable-calendar/div/tp-yt-iron-list/div/div[3]/div[2]/span[4]" # 04-07-24
    x_path = "/html/body/ytcp-date-picker/tp-yt-paper-dialog/ytcp-scrollable-calendar/div/tp-yt-iron-list/div/div[3]/div[2]/span[5]" # 05-07-24
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
def set_film_location(driver_loc: WebDriver):
    txt = "Polska"
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[8]/div[3]/ytcp-form-location/ytcp-form-autocomplete/ytcp-dropdown-trigger/div/div[2]/input"
    driver_loc.find_element(by=By.XPATH, value=x_path).send_keys(txt)
    time.sleep(1)
    x_path = "/html/body/ytcp-text-menu[3]/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[3]/ytcp-ve/tp-yt-paper-item-body/div/div/div/yt-formatted-string"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
def click_standard_licence(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[9]/div[3]/ytcp-form-select/ytcp-select/ytcp-text-dropdown-trigger/ytcp-dropdown-trigger/div/div[3]/tp-yt-iron-icon"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
    x_path = "/html/body/ytcp-text-menu[4]/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[1]/ytcp-ve/tp-yt-paper-item-body/div/div/div/yt-formatted-string"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
def click_allow_to_insert_on_different_pages(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[9]/div[4]/ytcp-form-checkbox/ytcp-checkbox-lit/div/div[1]/div/div"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)

def click_publish_in_subscription_section(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[9]/div[4]/ytcp-checkbox-lit/div/div[1]/div/div"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
def click_allow_remix(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[10]/ytcp-video-metadata-remix-settings/tp-yt-paper-radio-group/tp-yt-paper-radio-button[1]/div[1]/div[1]"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
def click_set_category(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[11]/div[3]/ytcp-form-select/ytcp-select/ytcp-text-dropdown-trigger/ytcp-dropdown-trigger/div/div[3]/tp-yt-iron-icon"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
    for i in range(3,6,1):
        try:
            x_path = f"/html/body/ytcp-text-menu[{i}]/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[11]/ytcp-ve/tp-yt-paper-item-body/div/div/div/yt-formatted-string"
            driver_loc.find_element(By.XPATH, x_path).click()
            time.sleep(1)
        except:
            pass


def click_allow_comments(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[12]/div[3]/ytcp-comment-moderation-settings/div/tp-yt-paper-radio-button[1]/div[1]/div[1]"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
def click_show_likes(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[12]/div[5]/ytcp-form-checkbox/ytcp-checkbox-lit/div/div[1]/div/div/div"
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
def click_next_from_details_to_edit(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div"
    wait_for_element(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)

def login(driver_loc: WebDriver) -> None:
    click_sign_in(driver_loc)
    insert_email(driver_loc)
    insert_password(driver_loc)
    # click_proceed_after_login(driver_loc)

def click_add_subtitles(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-video-elements/div[2]/ytcp-button/div"
    wait_for_element(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(5)
def click_send_file_2(driver_loc: WebDriver):
    x_path = "/html/body/ytve-captions-editor-modal/ytcp-dialog/tp-yt-paper-dialog/div[2]/div/ytve-editor/div[1]/div/ytve-captions-editor-options-panel/div[2]/div/ul/li[1]/ytcp-ve/a/tp-yt-iron-icon"
    wait_for_element(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)

def click_next_2(driver_loc: WebDriver):
    x_path = "/html/body/ytve-captions-editor-upload-dialog/ytcp-dialog/tp-yt-paper-dialog/div[3]/div/ytcp-button[2]/div"
    wait_for_element(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
def subtitles_page_1(driver_loc: WebDriver):
    # TODO: dodać ekran końcowy
    pass
def subtitles_page_2(driver_loc: WebDriver):
    # TODO: dodać karty
    pass
def click_next_from_edit_to_verification(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div"
    wait_for_element(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
def click_next_from_verification_to_visibility(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div"
    wait_for_element(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)
def click_publish(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[3]/div[1]/div[1]"
    wait_for_element(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(1)

    x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[3]/div"
    wait_for_element(driver_loc, x_path, 100)
    driver_loc.find_element(By.XPATH, x_path).click()
    time.sleep(10)

def get_share_link(driver_loc: WebDriver):
    x_path = "/html/body/ytcp-video-share-dialog/ytcp-dialog/tp-yt-paper-dialog/div[2]/div/div/div/a"
    wait_for_element(driver_loc, x_path, 100)
    href = driver_loc.find_element(By.XPATH, x_path).get_attribute('href')
    return href
def parse_text_with_polish_special_char(in_str: str):
    # in_str_c = in_str.replace('\r','').replace('\n','')
    return unidecode(in_str)

# def subtitles_page(driver_loc: WebDriver):
#     # click_add_subtitles(driver_loc)
#     # click_send_file_2(driver_loc)
#     # click_next_2(driver_loc)
#     # TODO: dodać przesłanie pliku z napisami
#     click_next_from_subtitles_to_verification(driver_loc)
#     pass



def send_video(driver_loc: WebDriver):
    model = load_obj()

    go_to_youtube_studio(driver_loc)
    click_create_button(driver_loc)
    click_send_file(driver_loc)
    send_file_from_disk(driver_loc)
    insert_video_title(driver_loc, parse_text_with_polish_special_char(model.title_text[:100]))
    insert_video_description(driver_loc, parse_text_with_polish_special_char(model.description_text))       # TODO:  click playlist !!!
    select_not_for_kids(driver_loc)
    click_show_more(driver_loc)
    # # click_my_video_contain_paied_promotion(driver_loc)
    click_video_is_unedited_with_ai(driver_loc)
    # # click_automatic_chapters(driver_loc)
    # # click_allow_mentioned_places(driver_loc)
    # # click_automatic_concepts(driver_loc)
    set_tags(driver_loc,parse_text_with_polish_special_char(model.tags_text))
    set_language(driver_loc)
    click_not_published_in_usa_tv(driver_loc)
    click_todays_date(driver_loc)                           # TODO: poprawić wybór daty - teraz wybiera ostatni wiersz i 28.06.2024
    set_film_location(driver_loc)
    # # click_standard_licence(driver_loc)
    # # click_allow_to_insert_on_different_pages(driver_loc)
    # # click_publish_in_subscription_section(driver_loc)
    # # click_allow_remix(driver_loc)
    click_set_category(driver_loc)
    # click_allow_comments(driver_loc)
    # click_show_likes(driver_loc)

    click_next_from_details_to_edit(driver_loc)
    # add_subtitles(driver_loc)
    click_next_from_edit_to_verification(driver_loc)
    click_next_from_verification_to_visibility(driver_loc)
    click_publish(driver_loc)

    href = get_share_link(driver_loc)

    a = 9


    #
    # x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div"
    # wait_for_element(driver_loc, x_path, 100)
    # driver_loc.find_element(By.XPATH, x_path).click()
    # logging.debug('send_video() - Clicked NEXT')
    #
    # # weryfikacja
    #
    # x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div"
    # wait_for_element(driver_loc, x_path, 100)
    # driver_loc.find_element(By.XPATH, x_path).click()
    # logging.debug('send_video() - Clicked NEXT')
    #
    # # widocznosc
    #
    # x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[3]/div[1]/div[1]"  # publiczny
    # wait_for_element(driver_loc, x_path, 100)
    # driver_loc.find_element(By.XPATH, x_path).click()
    # logging.debug('send_video() - Clicked NEXT')
    #
    # time.sleep(30)
    #
    # x_path = "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[3]/div"
    # wait_for_element(driver_loc, x_path, 100)
    # driver_loc.find_element(By.XPATH, x_path).click()
    # logging.debug('send_video() - Clicked PUBLISH')
    #
    # # x_path = "/html/body/ytcp-uploads-still-processing-dialog/ytcp-dialog/tp-yt-paper-dialog/div[3]/ytcp-button/div"
    # x_path = "/html/body/ytcp-video-share-dialog/ytcp-dialog/tp-yt-paper-dialog/div[3]/ytcp-button/div"
    # wait_for_element(driver_loc, x_path, 100)
    # driver_loc.find_element(By.XPATH, x_path).click()
    # logging.debug('send_video() - Clicked Close')

def main():
    driver = get_init_driver()
    accept_cookies_youtube(driver)
    login(driver)
    send_video(driver)


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
