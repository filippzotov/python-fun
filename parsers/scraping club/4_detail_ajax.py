import requests
import json

url = "https://scrapingclub.com/exercise/detail_ajax/"
ajax = "https://scrapingclub.com/exercise/ajaxdetail/"

req = requests.get(ajax)
src = req.text
card_info = json.loads(src)
card = {
    "name": card_info["title"],
    "price": card_info["price"],
    "description": card_info["description"],
}

print(card)
