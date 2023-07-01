import requests
from bs4 import BeautifulSoup
import pandas as pd
import random


def get_info_from_page(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, "html.parser")
    manga = soup.find_all("a", {"class": "fs14"})
    score = soup.find_all("span", {"class": "on"})
    info = soup.find_all("div", {"class": "information"})
    d = {
        "name": [],
        "rating": [],
        "volumes": [],
        "date": [],
        "url": [],
    }
    for i, rating, information in zip(manga, score, info):
        d["name"].append(i.text)
        d["rating"].append(rating.text)
        information = information.text.strip().split("\n")
        d["volumes"].append(information[0])
        d["date"].append(information[1].strip())
        d["url"].append(i["href"])
    return d


def get_top_manga():
    url = "https://myanimelist.net/topmanga.php"
    limit = 0
    for limit in range(0, 250, 50):
        if limit != 0:
            new_titles = get_info_from_page(url + f"?limit={limit}")
            for key in d:
                d[key].extend(new_titles[key])
        else:
            d = get_info_from_page(url)

    s = pd.DataFrame(d)
    return s


def create_manga_file(file_name, manga_table):
    manga_table.to_csv(file_name)


def get_data_from_file(file_name):
    try:
        df = pd.read_csv(file_name, on_bad_lines="skip")
    except FileNotFoundError:
        df = get_top_manga()
        create_manga_file(file_name, df)
    return df


def generate_random_manga(manga_table):
    i = random.randint(0, 249)
    manga = manga_table.loc[i]
    return f'{manga["name"]} rating: {manga["rating"]} volumes: {manga["volumes"]} link: {manga["url"]}'


if __name__ == "__main__":
    manga_table = get_data_from_file("top_manga.csv")
    while True:
        print("Get random manga? y/n")
        if input() == "y":
            print(generate_random_manga(manga_table))
        else:
            break
