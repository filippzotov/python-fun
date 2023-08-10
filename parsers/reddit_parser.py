import requests
from bs4 import BeautifulSoup

url = "https://www.reddit.com/svc/shreddit/community-more-posts/top/?t=DAY&name=Basketball&after=dDNfMTVuZ241dw=="
# url = "https://old.reddit.com/r/Basketball/top/?sort=top&t=week&after=dDNfMTVuajl4aQ=="dDNfMTVuZ241dw

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
}

req = requests.get(url, headers=headers, timeout=5)

src = req.text
# print(src)
with open("index.html", "w", encoding="utf-8") as file:
    file.write(src)


with open("index.html", encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
all_posts = soup.find_all(class_="absolute inset-0")
# print(soup.find())
print(len(all_posts))
for post in all_posts:
    print(post)
