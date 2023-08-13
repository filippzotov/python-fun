import requests
from bs4 import BeautifulSoup
import json

url = "https://scrapingclub.com/exercise/detail_json/"

req = requests.get(url)
src = req.text

with open("text.txt", "w", encoding="utf-8") as f:
    f.write(src)
soup = BeautifulSoup(src, "lxml")
card_info = soup.find(class_="p-6")
print(card_info.text)

card = {
    "name": card_info.find(class_="card-title").text,
    "price": card_info.find(class_="my-4 card-price").text,
    "description": card_info.find(class_="my-4 card-price").text,
}

print(card)
