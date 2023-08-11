import requests
from bs4 import BeautifulSoup
import csv


def get_posts_from_page(url, headers):
    req = requests.get(url, headers=headers, timeout=5)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    next_page_links = soup.find_all(
        class_="block cursor-pointer relative bg-neutral-background focus-within:bg-neutral-background-hover hover:bg-neutral-background-hover xs:rounded-[16px] p-md my-2xs nd:visible"
    )
    next_page = None
    for link in next_page_links:
        if link.get("more-posts-cursor") is not None:
            next_page = link.get("more-posts-cursor")
    return (next_page_links, next_page)


def get_reddit_posts(duration, subreddit):
    base_url = f"https://www.reddit.com/svc/shreddit/community-more-posts/top/?t={duration}&name={subreddit}"
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    }
    all_posts = []
    url = base_url
    while True:
        posts = get_posts_from_page(url, headers)
        all_posts.extend(posts[0])
        if posts[1] is None or len(posts[0]) < 25:
            break
        url = base_url + f"&after={posts[1]}=="
    return all_posts


def get_data_from_html(posts):
    answer = []
    for post in posts:
        url = post["content-href"]
        title = post["post-title"]
        author = post["author"]
        rating = post.get("score")
        date = post["created-timestamp"]

        text = post.find(
            class_="text-neutral-content md max-h-[337px] overflow-hidden text-12 xs:text-14"
        )
        if text:
            text = text.text
        tmp = {
            "author": author,
            "title": title,
            "text": text,
            "rating": rating,
            "date": date,
            "url": url,
        }
        answer.append(tmp)
    return answer


def write_to_csv(periud, subreddit, posts):
    fieldnames = ["author", "title", "text", "rating", "date", "url"]
    with open(
        f"{subreddit}_{periud}.csv", "w", encoding="utf-8", newline=""
    ) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(posts)


if __name__ == "__main__":
    periud = ["HOUR", "DAY", "WEEK", "MONTH"]
    print("Enter subreddit name")
    subreddit = input()
    p_index = 0
    while p_index < 1 or p_index > 4:
        print("Chose periud of time:\n1. hour\n2. day\n3. week\n4. month")
        p_index = int(input())
    html_posts = get_reddit_posts(periud[p_index - 1], subreddit)
    posts = get_data_from_html(html_posts)
    write_to_csv(periud[p_index - 1], subreddit, posts)
    print("Done")
