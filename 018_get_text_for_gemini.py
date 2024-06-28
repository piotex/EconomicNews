from news_model import *


def main():
    obj_list = load_obj_list()

    txt = """
Streść poniższy artykuł, tak, żeby dobrze się tego słuchało na TikTok.
Chcę, żebyś wybrał najciekawsze wątki z całego materiału i podsumował je w angażujący sposób do 5 zdań maksymalnie.
Unikaj zbędnych przymiotników.
Przedstaw poniższe informacje w rzetelny, obiektywny i angażujący widza TikToka sposób. 
    """

    with open(f"data/text_for_gemini/{obj_list[0].idx}.txt", "w", encoding="utf-8") as f:
        f.write(txt+obj_list[0].article_text)

    print("""
Czekam na twoją akcje...
Skopiuj tekst z data/text_for_gemini
Uruchom polecenie w gemini
Zapisz w tym samym pliku rezultat wygenerowany przez gemini
Po zapisaniu wciśnij ENTER w konsoli
""")
    a = input()

    with open(f"data/text_for_gemini/{obj_list[0].idx}.txt", "r", encoding="utf-8") as f:
        obj_list[0].article_text = f.read()

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
