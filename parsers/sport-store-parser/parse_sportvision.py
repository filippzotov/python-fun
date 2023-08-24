import requests
from bs4 import BeautifulSoup
import csv


def get_info_from_card(card):
    title_block = card.find(class_="title")
    title = title_block.find("a")["title"]
    cur_price = card.find(class_="current-price")
    prev_price = card.find(class_="prev-price")
    if not prev_price:
        prev_price = cur_price
    url = title_block.find("a")["href"]

    card_info = {
        "title": title.strip(),
        "cur_price": cur_price.text.strip().split(" ")[0],
        "prev_price": prev_price.text.strip().split(" ")[0],
        "url": url,
    }
    return card_info


def parse_cards_from_page(src):
    soup = BeautifulSoup(src, "lxml")
    cards = soup.find_all(class_="item-data col-xs-12 col-sm-12")
    cards_info = []
    for card in cards:
        card_info = get_info_from_card(card)
        cards_info.append(card_info)
    return cards_info


def try_connect(url):
    response = requests.get(url)
    src = response.text
    with open("test.txt", "w", encoding="utf-8") as f:
        f.write(src)
    return src


def write_to_csv(products, fields, file_name):
    with open(file_name, "w", encoding="utf-8", newline="") as write_file:
        writer = csv.DictWriter(write_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(products)


def main():
    base_url = "https://www.sportvision.rs/obuca/za-muskarce+unisex/za-odrasle"
    url = base_url
    all_products = []
    i = 1
    while True:
        src = try_connect(url)
        cards_info = parse_cards_from_page(src)
        if not cards_info:
            break
        all_products.extend(cards_info)
        url = base_url + f"/page-{i}"
        i += 1
        print(i)
    write_to_csv(
        all_products, ["title", "cur_price", "prev_price", "url"], "sportvision.csv"
    )


if __name__ == "__main__":
    main()
