import requests
from bs4 import BeautifulSoup
import re
import json
import csv
import time
import base64
import os


def fetch_next_page(mark, url):
    cursorMark = f"&paging[cursorMark]={mark}"

    req = requests.get(url + cursorMark)
    src = req.text
    products = json.loads(src)
    products = products["data"]
    slugs = []
    if products["projects"] is None:
        return None, None
    for project in products["projects"]:
        slugs.append(project["slug"])
    return (slugs, products["paging"]["total"])


def write_slugs_to_csv(slugs, category):
    with open(f"{category}.csv", "a") as f:
        f.writelines("\n".join(slugs) + "\n")


def get_all_projects(category, url):
    count = 0
    total_projects = 25
    flag_first = True
    while total_projects and count < total_projects and count < 9980:
        d = {"sortValues": None, "from": count, "boostedProjectUids": None}
        next_mark = json.dumps(d)
        mark = "version_2_" + base64.b64encode(next_mark.encode("utf-8")).decode(
            "utf-8"
        )
        slugs, new_totoal = fetch_next_page(mark, url)
        count += 24
        if flag_first:
            total_projects = new_totoal
            flag_first = False
        if slugs is None:
            continue
        write_slugs_to_csv(slugs, category)


def get_categories_from_file(file_name):
    categories = []
    with open(file_name, "r") as file:
        reader = csv.DictReader(file)
        for line in reader:
            categories.append(line)
    return categories


if __name__ == "__main__":
    folder_name = "categories"
    categories = get_categories_from_file("categories_count.csv")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    cur_big_category = ""
    for category in categories:
        print(category["category"])
        if os.path.isfile(
            folder_name + "/" + category["general"] + ".csv"
        ) or os.path.isfile(folder_name + "/" + category["category"] + ".csv"):
            print("skip")
            continue
        if category["general"] != cur_big_category:
            cur_big_category = category["general"]
            skip_to_next_big = False
            if int(category["count"]) < 10000:
                skip_to_next_big = True
                get_all_projects(
                    folder_name + "/" + category["general"], category["url"]
                )
            else:
                continue

        if skip_to_next_big:
            continue
        get_all_projects(folder_name + "/" + category["category"], category["url"])
