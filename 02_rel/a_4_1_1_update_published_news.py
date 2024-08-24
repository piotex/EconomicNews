import time
from news_model import *

obj_list_path = "../data/obj_list.json"


def main():
    processed_news_path = "data/urls/processed_news.txt"
    news_model_list = load_obj_list()
    for news_model in news_model_list:
        with open(processed_news_path, "r") as f:
            processed_news = f.readlines()

        processed_news = [x.replace("\n", "").replace("\r", "") for x in processed_news]
        processed_news.append(news_model.url)
        processed_news = [x+"\n" for x in processed_news]

        with open(processed_news_path, "w") as f:
            f.writelines(processed_news)



    # path = r"C:\Users\pkubon\kn\0-git-repos\hosted-files\.git"
    # commit_msg = "jenkins: update published news"
    # try:
    #     repo = Repo(path)
    #     repo.git.add(update=True)
    #     repo.index.commit(commit_msg)
    #     origin = repo.remote(name='origin')
    #     origin.push()
    # except:
    #     pass


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
