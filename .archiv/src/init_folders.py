import os
import shutil


def init_folders():
    print(f"init_folders")
    data_files = '../data_files'
    folders = [
        'audio',
        'gifs',
        'important_files',
        'movies',
        'screen_shots',
        'logs'
    ]
    for folder in folders:
        sciezka_folderu = os.path.join(data_files, folder)
        if os.path.exists(sciezka_folderu):
            shutil.rmtree(sciezka_folderu)
        os.makedirs(os.path.join(data_files, folder))

if __name__ == "__main__":
    init_folders()