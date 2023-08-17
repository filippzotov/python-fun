import requests
from bs4 import BeautifulSoup
import re
import json
import csv
import time
import base64


def first_page():
    pass


def fetch_next_page(mark, category):
    url = "https://www.upwork.com/ab/services/pub/api/catalog_search/search/vcs/v3?"
    cursorMark = f"paging[cursorMark]={mark}"
    rows = "&paging[rows]=24"
    category = f"&projectCategoryId=projectCategory:{category}"

    req = requests.get(url + cursorMark + rows + category)
    src = req.text
    products = json.loads(src)
    products = products["data"]
    slugs = []
    for project in products["projects"]:
        slugs.append(project["slug"])
    return (slugs, products["paging"]["nextCursorMark"], products["paging"]["total"])


def write_slugs_to_csv(slugs, category):
    with open(f"{category}.csv", "a") as f:
        f.writelines("\n".join(slugs) + "\n")


def get_all_projects():
    mark = "version_2_eyJzb3J0VmFsdWVzIjpudWxsLCJmcm9tIjoyNCwiYm9vc3RlZFByb2plY3RVaWRzIjpudWxsfQ=="
    cat = "logoDesign"
    count = 0
    total_projects = 25

    while count < total_projects:
        d = {"sortValues": None, "from": count, "boostedProjectUids": None}
        next_mark = json.dumps(d)
        mark = "version_2_" + base64.b64encode(next_mark.encode("utf-8")).decode(
            "utf-8"
        )
        slugs, mark, total_projects = fetch_next_page(mark, cat)
        write_slugs_to_csv(slugs, cat)
        count += 24
        print(mark)
        time.sleep(0.3)


get_all_projects()
# fetch_next_page(mark, cat)
