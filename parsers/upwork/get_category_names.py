import requests
from bs4 import BeautifulSoup
import re
import time
import csv
import json

url = "https://www.upwork.com/services/wordpress"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Alt-Used": "www.upwork.com",
    "Connection": "keep-alive",
    "Cookie": "_fbp=fb.1.1692299968331.1049674458; OptanonAlertBoxClosed=2023-08-17T19:19:28.342Z; OptanonConsent=landingPath=NotLandingPage&datestamp=Fri+Aug+18+2023+11%3A36%3A53+GMT%2B0200+(%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202305.1.0&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&hosts=&consentId=61b95c53-519c-441a-9f40-ad8eb64325be&interactionCount=1&isGpcEnabled=0…!pxWTA3,pxTHA3; country_code=RS; cookie_prefix=; cookie_domain=.upwork.com; _cq_suid=1.1692299986.IernP3x0pfdOMRY9; IR_gbd=upwork.com; IR_13634=1692351416263%7C0%7C1692351416263%7C%7C; XSRF-TOKEN=69920c9d820cf8f93e79f1629875c8f7; ftr_blst_1h=1692348039436; _upw_ses.5831=*; __cf_bm=LN.ttk15pYqEajZ1G2.Xh66dcIlS8.vDuD82sJ8wFRg-1692351406-0-AQWkpVO8/gWSi2I0/rXR8ZCzKyxZen1DYyFzOnFCWzR7nzS/et8C27XS7yQ3kwxjdQLuyj81TckglORsp7hYqo4=; _uetsid=2748c0e03cfc11ee906c312c282d338c; _uetvid=727334003a0a11eea435af1147b96046".encode(
        "utf-8"
    ),  #
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "TE": "trailers",
}  # ... any other headers you want to add


# url = "https://www.upwork.com/services/product/video-audio-awesome-custom-animated-stickers-for-most-chat-platform-1480452950411137024"
def get_categories():
    session = requests.Session()
    session.headers = headers
    req = session.get(url, headers=headers)

    src = req.text
    soup = BeautifulSoup(src, "lxml")
    wrapper = soup.find(class_="up-mega-dropdown-wrapper")
    all_links = wrapper.find_all("a")
    dict_links = []
    general_link = ""
    for link in all_links:
        if "occupation" in link["class"]:
            general_link = link.text.strip()
        dict_links.append({"general": general_link, "category": link.text.strip()})
    write_to_csv(dict_links, ["general", "category"], "categories.csv")


def write_to_csv(categories, fields, file_name):
    fieldnames = fields
    with open(file_name, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for category in categories:
            writer.writerow(category)


def count_projects(category, big_category):
    if big_category:
        url = f"https://www.upwork.com/ab/services/pub/api/catalog_search/search/vcs/v3?paging[rows]=24&serviceId=upworkOccupation:{category}"
    else:
        url = f"https://www.upwork.com/ab/services/pub/api/catalog_search/search/vcs/v3?paging[rows]=24&projectCategoryId=projectCategory:{category}"

    # req = requests.get(url + cursorMark + rows + category)
    req = requests.get(url)
    src = req.text
    products = json.loads(src)
    products = products["data"]
    return (products["paging"]["total"], url)


def try_different_url(category):
    category = category.replace(" ", "")
    c = category[0].lower() + category[1:]
    count, url = count_projects(c, False)
    if count != 0:
        return count, url
    count, url = count_projects(c, True)
    if count != 0:
        return count, url
    c = category.lower()
    count, url = count_projects(c, False)
    if count != 0:
        return count, url
    count, url = count_projects(c, True)
    if count != 0:
        return count, url
    count, url = count_projects(category, True)
    if count != 0:
        return count, url
    count, url = count_projects(category, False)
    return count, url


def count_all_projects(categories_file):
    new_file_lines = []
    count_zero = []
    with open(categories_file, "r") as f:
        reader = csv.DictReader(f)
        for line in reader:
            category = line["category"]
            category = category.replace("&", "")
            category = category.replace("-", "")
            category = category.replace(",", "")

            count, url = try_different_url(category)
            line["count"] = count
            line["url"] = url
            print(line)
            if count == 0:
                count_zero.append(line["category"])
            new_file_lines.append(line)
    write_to_csv(
        new_file_lines,
        ["general", "category", "count", "url"],
        "categories_count.csv",
    )
    print(count_zero)
    print(len(count_zero))


if __name__ == "__main__":
    count_all_projects("categories.csv")
