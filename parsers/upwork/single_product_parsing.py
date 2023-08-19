import requests
from bs4 import BeautifulSoup
import re
import csv
import time
import cloudscraper
import concurrent.futures

# from selenium import webdriver
import os


def find_product_info(page_text):
    soup = BeautifulSoup(page_text, "lxml")
    with open("index.txt", "w", encoding="utf-8") as f:
        f.write(soup.text)

    product_info = {
        "title": "",
        "reviews": "",
        "price": "",
        "details": "",
        "this_project": "",
        "all_projects": "",
    }

    title = soup.find(class_="mb-20 display-rebrand h2 d-none d-lg-block").text
    reviews = soup.find(class_="h2 mb-0 ml-10").text.split()[0]
    prices = soup.find_all(class_="tier__price")
    price = ", ".join([i.text for i in prices])
    details = soup.find("div", {"id": "project-details"}).text
    this_project = re.findall(
        r"\d+", soup.find(attrs={"aria-controls": "this_project"}).text
    )[0]
    all_projects = re.findall(
        r"\d+", soup.find(attrs={"aria-controls": "all_projects"}).text
    )[0]

    product_info["title"] = title.strip()
    product_info["reviews"] = reviews
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
        "reviews",
        "price",
        "details",
        "this_project",
        "all_projects",
    ]
    with open(f"{file_name}", "a", encoding="utf-8", newline="") as write_file:
        writer = csv.DictWriter(write_file, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerows(products)


if __name__ == "__main__":
    base_url = "https://www.upwork.com/services/product/"
    session = requests.Session()
    read_dir = "categories"
    files = get_file_names_from_dir(read_dir)

    folder_name = "product_pages"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    for file_name in files:
        products = []
        slugs = get_slugs_from_file(file_name)
        limit_write = 24
        write_file_name = file_name.split("\\")[-1]
        print(write_file_name)
        for slug in slugs:
            url = base_url + slug[:-1]
            s = cloudscraper.create_scraper()
            req = s.get(url, headers=headers)
            # req = session.get(url, headers=headers, timeout=2)

            src = req.text
            time.sleep(0.5)
            with open("bybass.txt", "w", encoding="utf-8") as f:
                f.write(src)
            print(url)
            try:
                product = find_product_info(src)

            except AttributeError:
                product = [
                    {
                        "title": None,
                        "reviews": None,
                        "price": None,
                        "details": None,
                        "this_project": None,
                        "all_projects": None,
                    }
                ]
            product["url"] = url
            products.append(product)
            limit_write -= 1
            if not limit_write:
                write_product_info_to_file(
                    folder_name + "/" + write_file_name, products
                )
                limit_write = 24
                products = []
