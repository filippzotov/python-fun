url = "https://scrapingclub.com/exercise/list_infinite_scroll/"


import requests
from bs4 import BeautifulSoup

base_url = "https://scrapingclub.com/exercise/list_infinite_scroll/"
url = "https://scrapingclub.com/exercise/list_infinite_scroll/"
i = 1
all_cards = []
while True:
    req = requests.get(url)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    flag = False
    card_info = soup.find_all(class_="w-full rounded border post")
    for card in card_info:
        new_card = {
            "name": card.find("h4").text,
            "price": card.find("h5").text,
            "image": card.find(class_="card-img-top img-fluid")["src"],
        }
        if new_card in all_cards:
            flag = True
        all_cards.append(new_card)
    if flag:
        break
    i += 1
    url = base_url + f"?page={i}"
print(all_cards)
