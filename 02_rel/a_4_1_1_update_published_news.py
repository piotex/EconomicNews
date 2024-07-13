import time
import news_model

obj_list_path = "../data/obj_list.json"


def main():
    pathh = "data/urls/processed_news.txt"
    tmp_obj = news_model.load_obj()
    with open(pathh, "r") as f:
        data = f.readlines()

    data = [x.replace("\n", "").replace("\r", "") for x in data]
    data.append(tmp_obj.url)
    data = [x+"\n" for x in data]

    with open(pathh, "w") as f:
        f.writelines(data)

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
