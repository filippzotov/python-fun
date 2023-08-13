import requests
from bs4 import BeautifulSoup

base_url = "https://scrapingclub.com/exercise/list_basic/"
url = "https://scrapingclub.com/exercise/list_basic/"
i = 1
all_cards = []
while True:
    req = requests.get(url)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    card_info = soup.find_all(class_="w-full rounded border")
    for card in card_info:
        all_cards.append(
            {
                "name": card.find("h4").text,
                "price": card.find("h5").text,
            }
        )
    if not soup.find(class_="page next"):
        break
    i += 1
    url = base_url + f"?page={i}"

print(all_cards)
