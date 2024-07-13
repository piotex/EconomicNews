import shutil
import requests
from bs4 import BeautifulSoup
import os
import time
from news_model import *
from pytube import YouTube

main_url = "https://www.bankier.pl"
obj_list_path = "../data/obj_list.json"
bankier_urls = []


# download resources from github ...


def init_folders():
    folders = [
        'data',
        'data/urls',
        'data/audios',
        'data/videos',
        'data/videos/background_videos',
        'data/images',
        'data/images/animated_bird',
        'data/images/screenshots',
    ]
    if os.path.exists(folders[2]):
        shutil.rmtree(folders[2])
    if os.path.exists(folders[7]):
        shutil.rmtree(folders[7])

    for folder in folders:
        if os.path.exists(folder):
            # shutil.rmtree(folder)
            pass
        else:
            os.makedirs(folder)


def init_files():
    save_obj_list([])


def download_file(url, dest):
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"File not accessible: {r.status_code} {r.url}")
    with open(dest, 'wb') as f:
        f.write(r.content)


def download_files_from_github_folder(url, dest):
    allowed_file_types = [".png", ".jgp", ".yml", ".yaml"]
    html_content = requests.get(url).content
    all_links = BeautifulSoup(html_content, 'html.parser').find_all('a')
    all_links = [a.get('href') for a in all_links if a.get('href') and url.split("/")[-1] in a.get('href')]

    res = []
    for href in all_links:
        file_is_ok = False
        for allowed_file_type in allowed_file_types:
            if allowed_file_type in href:
                file_is_ok = True
        if not file_is_ok:
            continue
        res.append("https://github.com" + href + "?raw=true")
    res = list(set(res))

    for url in res:
        file_name = url.split("/")[-1].split("?")[0]
        download_file(url, f"{dest}/{file_name}")


def download_files_from_github():
    url_dest_list = [
        ["https://github.com/piotex/hosted-files/raw/main/EconomicNews/urls/processed_news.txt","data/urls/processed_news.txt"],
        ["https://github.com/piotex/hosted-files/raw/main/EconomicNews/urls/input_for_chatgpt.txt","data/urls/input_for_chatgpt.txt"],
        ["https://github.com/piotex/hosted-files/raw/main/EconomicNews/urls/bankier_urls.txt","data/urls/bankier_urls.txt"],
        ["https://github.com/piotex/hosted-files/raw/main/EconomicNews/urls/youtube_background_urls.txt","data/urls/youtube_background_urls.txt"],
    ]
    for url_dest in url_dest_list:
        download_file(url_dest[0], url_dest[1])

    url_dest_list = [
        ["https://github.com/piotex/hosted-files/tree/main/EconomicNews/animated_bird", "data/images/animated_bird"],
    ]
    for url_dest in url_dest_list:
        download_files_from_github_folder(url_dest[0], url_dest[1])


def download_files_from_youtube():
    with open("data/urls/youtube_background_urls.txt", 'r', encoding="utf-8") as f:
        urls = f.readlines()
    urls = [u.strip().replace("\n", "") for u in urls]

    for url in urls:
        yt = YouTube(url)
        a1 = yt.streams
        a3 = a1.filter(file_extension="mp4")
        a4 = a3.filter(type="video")
        a5 = a4.order_by("resolution").desc()  # highest first
        a6 = a5.first().download(output_path="data/videos/background_videos")


def main():
    init_folders()
    init_files()
    # download_files_from_github()
    # download_files_from_youtube()


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
