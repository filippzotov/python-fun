import requests
import json
from bs4 import BeautifulSoup

ajax = "https://scrapingclub.com/exercise/ajaxdetail_cookie/"


header = {
    "Host": "scrapingclub.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://scrapingclub.com/exercise/detail_cookie/",
    "x-requested-with": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Cookie": "_ga_BD9ZHFE1XX=GS1.1.1692104504.5.1.1692106677.0.0.0; _ga=GA1.1.722116230.1691694853; csrftoken=fZlxzYrFAqxvJa7SfBgAO6FB9dtndq0l; token=ZZ9H6NDEGD",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers",
}

response = requests.get("https://scrapingclub.com/exercise/detail_cookie/")
soup = BeautifulSoup(response.text, "lxml")
# print(dir(response))
token = response.cookies["token"]
header[
    "Cookie"
] = f"_ga_BD9ZHFE1XX=GS1.1.1692104504.5.1.1692106677.0.0.0; _ga=GA1.1.722116230.1691694853; csrftoken=fZlxzYrFAqxvJa7SfBgAO6FB9dtndq0l; token={token}"

req = requests.get(ajax + f"?token={token}", cookies=response.cookies)
src = req.text
print(src)
card_info = json.loads(src)
card = {
    "name": card_info["title"],
    "price": card_info["price"],
    "description": card_info["description"],
}

print(card)
