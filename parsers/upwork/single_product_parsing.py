import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import cloudscraper
import concurrent.futures
import random

# from selenium import webdriver
import os

random_secs = [random.randint(4, 5) for i in range(300)]


def find_product_info(page_text):
    soup = BeautifulSoup(page_text, "lxml")
    # with open("index.txt", "w", encoding="utf-8") as f:
    #     f.write(soup.text)

    product_info = {
        "title": "",
        "price": "",
        "details": "",
        "this_project": "",
        "all_projects": "",
    }
    try:
        title = soup.find(
            class_="mb-20 display-rebrand h2 d-none d-lg-block"
        ).text.strip()
    except:
        title = ""
    try:
        prices = soup.find_all(class_="tier__price")
        price = ", ".join([i.text for i in prices[: len(prices) // 2]])
    except:
        price = ""
    if not prices:
        try:
            price = soup.find(class_="text-right d-none d-lg-block").text.strip()
        except:
            price = ""
    try:
        details = soup.find("div", {"id": "project-details"}).text
    except:
        details = ""
    try:
        this_project = re.findall(
            r"\d+", soup.find(attrs={"aria-controls": "this_project"}).text
        )[0]

    except:
        this_project = ""
    try:
        all_projects = re.findall(
            r"\d+", soup.find(attrs={"aria-controls": "all_projects"}).text
        )[0]
    except:
        all_projects = ""

    product_info["title"] = title
    product_info["price"] = price
    product_info["details"] = details
    product_info["this_project"] = this_project
    product_info["all_projects"] = all_projects

    return product_info


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
    # "Cookie": r"_fbp=fb.1.1692299968331.1049674458; OptanonAlertBoxClosed=2023-08-17T19:19:28.342Z; OptanonConsent=landingPath=NotLandingPage&datestamp=Sat+Aug+19+2023+11%3A00%3A12+GMT%2B0200+(%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202305.1.0&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&hosts=&consentId=61b95c53-519c-441a-9f40-ad8eb64325be&interactionCount=1&isGpcEnabled=0…76Air3Migration,!pxFAA3,CI9570Air2Dot5,!CI10270Air2Dot5QTAllocations,!pxWTA3,CI11132Air2Dot75,i18nOn,!air2Dot76Qt,OTBnrOn,!RMTAir3Talent,!CI10857Air3Dot0,TONB2256Air3Migration,!pxBPA3; XSRF-TOKEN=302b1e79e080703d6b9d7fb50e277543; __cf_bm=MM2SvpVJsRQmFs6uVJu.ZjUDTMbx35uImxo7SuSOcMI-1692435436-0-AScRp++giJShPUQ5AQ4W/4t+dLMbjckht5cRCdXSmGSqnqB53Nn8czseXlyKT+Ii5pPJHN0mQlFTHHKfDoDzy+k=; _upw_ses.5831=*; ftr_blst_1h=1692435442420; _uetsid=2748c0e03cfc11ee906c312c282d338c; _uetvid=727334003a0a11eea435af1147b96046".encode(
    #     "utf-8"
    # ),
}  # ... any other headers you want to add


def get_slugs_from_file(file_name):
    slugs = []
    with open(file_name, "r") as file:
        slugs = file.readlines()
    return slugs


def get_file_names_from_dir(dir_name):
    return [os.path.join(dir_name, file) for file in os.listdir(dir_name)]


def write_product_info_to_file(file_name, products):
    write_header = True
    if os.path.isfile(file_name):
        write_header = False
    fieldnames = [
        "title",
        "price",
        "details",
        "this_project",
        "all_projects",
        "url",
    ]
    with open(f"{file_name}", "a", encoding="utf-8", newline="") as write_file:
        writer = csv.DictWriter(write_file, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerows(products)


def scrape_urls_from_file(file_name):
    base_url = "https://www.upwork.com/services/product/"
    folder_name = "product_pages"
    global random_secs
    delay = random_secs.pop()
    write_file_name = file_name.split("\\")[-1]
    print(write_file_name)
    slugs = get_slugs_from_file(file_name)
    products = []
    s = cloudscraper.create_scraper()
    limit_write = 24
    for slug in slugs:
        url = base_url + slug[:-1]
        time.sleep(0.5)

        product = get_product_from_url(s, url)
        attempts = 5
        while not product["title"] and attempts:
            time.sleep(20)
            product = get_product_from_url(s, url)
            attempts -= 1
        products.append(product)
        limit_write -= 1
        if not limit_write:
            write_product_info_to_file(folder_name + "/" + write_file_name, products)
            limit_write = 24
            products = []
    print("ended")


def get_product_from_url(scraper, url):
    req = scraper.get(url, headers=headers)
    src = req.text
    # with open("bybass.txt", "w", encoding="utf-8") as f:
    #     f.write(src)
    print(url)
    try:
        product = find_product_info(src)
    except:
        product = {
            "title": "",
            "price": "",
            "details": "",
            "this_project": "",
            "all_projects": "",
        }

        print("skiped")
    finally:
        product["url"] = url
    return product


if __name__ == "__main__":
    base_url = "https://www.upwork.com/services/product/"
    # session = requests.Session()
    read_dir = "categories"
    files = get_file_names_from_dir(read_dir)

    folder_name = "product_pages"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(scrape_urls_from_file, files))


# def test_func():
#     url = "https://www.upwork.com/services/product/admin-customer-support-a-fantastic-flyer-design-for-your-business-campaign-1668851164277727232"
#     s = cloudscraper.create_scraper()
#     req = s.get(url, headers=headers)
#     src = req.text
#     product = find_product_info(src)
#     print(product)


# test_func()
