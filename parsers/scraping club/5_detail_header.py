import requests
import json


url = "https://scrapingclub.com/exercise/detail_header/"
ajax = "https://scrapingclub.com/exercise/ajaxdetail_header/"
header = {
    "Host": "scrapingclub.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://scrapingclub.com/exercise/detail_header/",
    "x-requested-with": "XMLHttpRequest",
    "Alt-Used": "scrapingclub.com",
    "Connection": "keep-alive",
    "Cookie": "_ga_BD9ZHFE1XX=GS1.1.1692104504.5.1.1692104894.0.0.0; _ga=GA1.1.722116230.1691694853; csrftoken=fZlxzYrFAqxvJa7SfBgAO6FB9dtndq0l",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers",
}
req = requests.get(ajax, headers=header)
src = req.text
card_info = json.loads(src)
card = {
    "name": card_info["title"],
    "price": card_info["price"],
    "description": card_info["description"],
}

print(card)
