import dataclasses
import json
import re
from models.model_news import NewsModel
from yt_manager_2_0 import *


def get_val_from_attributes_list(key: str, attrs_list) -> str:
    res_list = [sub_list for sub_list in attrs_list if sub_list and sub_list[0] == key]
    res_elem = res_list[0][1]
    return res_elem


def get_comment_count(driver_in):
    for j in range(1, 4, 1):
        try:
            x_path = f"/html/body/div[1]/div[{j}]/main/section[2]/header/h3"
            kom_text = driver_in.find_element(by=By.XPATH, value=x_path).text
            pattern = r'Komentarze \((\d+)\)'
            match = re.search(pattern, kom_text)
            res = int(match.group(1))
            return res
        except Exception as exx:
            pass
    raise Exception("==== comment_count info not found ====")


def get_quick_desc(driver_in):
    kom_text = ""
    for j in range(4, 0, -1):
        try:
            x_path = f"/html/body/div[1]/div[{j}]/main/article/section/p[1]/span"
            kom_text += driver_in.find_element(by=By.XPATH, value=x_path).text
            kom_text += "\n"

            x_path = f"/html/body/div[1]/div[{j}]/main/article/section/p[2]"
            kom_text += driver_in.find_element(by=By.XPATH, value=x_path).text
            kom_text += "\n"

            x_path = f"/html/body/div[1]/div[{j}]/main/article/section/p[3]"
            kom_text += driver_in.find_element(by=By.XPATH, value=x_path).text
            kom_text += "\n"

            x_path = f"/html/body/div[1]/div[{j}]/main/article/section/p[4]"
            kom_text += driver_in.find_element(by=By.XPATH, value=x_path).text
            kom_text += "\n"

        except Exception as exx:
            pass

    if kom_text != "":
        return kom_text

    raise Exception("==== Quick info not found ====")


def get_comments_count(start_elem_in: int):
    print(f"get_comments_count")
    path_news_list = "../data_files/important_files/news_list.json"

    with open(path_news_list, "r") as json_file:
        data_from_json = json.load(json_file)
    my_class_objects = [NewsModel(**item) for item in data_from_json]

    driver = get_init_driver()
    time.sleep(1)
    accept_cookies_bankier(driver)
    time.sleep(1)

    # path_to_usr_pwd = "../data_files/screen_dimensions.txt"
    # with open(path_to_usr_pwd, "r") as file:
    #     res = file.readlines()
    #     width = int(res[0].strip())
    #     height = int(res[1].strip())
    # driver.set_window_size(width, height)
    # driver.set_window_position(0, 0)

    i = 0
    for elem in my_class_objects:
        if i < start_elem_in:
            i += 1
            continue

        try:
            print(f"get_comments_count: {i} z {len(my_class_objects)}")
            i += 1
            driver.get(elem.url)
            time.sleep(1)
            scroll_to_xxx(driver, 600)

            elem.quick_info = get_quick_desc(driver)
            elem.comments_number = get_comment_count(driver)

            # img_path = f"../data_files/screen_shots/{elem.id}.png"
            # driver.save_screenshot(img_path)
            # elem.screen_path = img_path
        except Exception as exxx:
            print("=== error ===")
            print(exxx)
            print(elem)
            print("=== error ===")
            pass

    news_dict_list = [dataclasses.asdict(news) for news in my_class_objects]
    with open(path_news_list, "w") as json_file:
        json.dump(news_dict_list, json_file, indent=4)


if __name__ == "__main__":
    start_elem = 0
    get_comments_count(start_elem)
