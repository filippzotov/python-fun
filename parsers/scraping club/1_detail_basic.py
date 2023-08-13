import requests
from bs4 import BeautifulSoup


url = "https://scrapingclub.com/exercise/detail_basic/"

req = requests.get(url)
src = req.text
soup = BeautifulSoup(src, "lxml")
card_info = soup.find(class_="p-6")

card = {
    "name": card_info.find(class_="card-title").text,
    "price": card_info.find(class_="my-4 card-price").text,
    "description": card_info.find(class_="my-4 card-price").text,
}

print(card)
