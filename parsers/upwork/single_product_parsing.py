import requests
from bs4 import BeautifulSoup
import re


def find_product_info(page_text):
    # with open("index.html", "r", encoding="utf-8") as f:
    #     page_text = f.read()
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

    product_info["title"] = title
    product_info["reviews"] = reviews
    product_info["price"] = price
    product_info["details"] = details
    product_info["this_project"] = this_project
    product_info["all_projects"] = all_projects

    print(product_info)


headers = {
    "Host": "www.upwork.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.upwork.com/services/design/brand-identity-design",
    "Alt-Used": "www.upwork.com",
    "Connection": "keep-alive",
    "Cookie": '__cflb=02DiuEXPXZVk436fJfSVuuwDqLqkhavJbnqXebxkeZf9D; visitor_id=93.86.199.232.1691952699451000; device_view=full; _upw_id.5831=49c7b7a2-a5ca-4b60-b223-6ccde6436c88.1691952701.5.1692286936.1692276412.f6df83c0-23da-438b-84c6-45e22f7400c2.eed8b013-35aa-4096-bd04-728278c2fb56.d89f3b7c-ccd1-4878-a685-769ecf9a9a51.1692276417165.2747; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Aug+17+2023+17%3A15%3A40+GMT%2B0200+(%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202305.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=88bd6fa8-8617-4c3d-8c97-a49723a83760&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=RS%3B00; AWSALB=F3ZkR1AMslHM1Uh4TSwv0aztZXxjEyX+xN+qtSFvPHZ9g49Tzcz3WEqMBXkSAeoN3cx4Yah63w/+KPdUkrPIz6xeTzbl8ISzjtqcDHfeGVumkI5Xph5D9hqhQ3UY; AWSALBCORS=F3ZkR1AMslHM1Uh4TSwv0aztZXxjEyX+xN+qtSFvPHZ9g49Tzcz3WEqMBXkSAeoN3cx4Yah63w/+KPdUkrPIz6xeTzbl8ISzjtqcDHfeGVumkI5Xph5D9hqhQ3UY; spt=0b279929-1e6a-4a92-a564-70d99c43d243; _gcl_au=1.1.1514201675.1691952702; _ga_KSM221PNDX=GS1.1.1692276417.4.1.1692285342.0.0.0; _ga=GA1.2.375872138.1691952702; _cq_duid=1.1691952702.RgK8TlFmFxGKOAn8; _mkto_trk=id:518-RKL-392&token:_mch-upwork.com-1691952703016-92939; _tt_enable_cookie=1; _ttp=Kc4UYs1EsWRoVIF9cY6EPyl0Zrj; _rdt_uuid=1691952703799.22d4b778-c26a-453b-93c1-127a9dc36d6d; __pdst=59d89d8629ba4e2e8dec0aaa1d722d93; _zitok=d03d12f56c10c301bea31691952703; _fbp=fb.1.1691952705084.1101960311; _cfuvid=f1JS0ZLmoMZaR0ChjDsPvau2nmhok0cMzIfF6959vCQ-1691952699202-0-604800000; enabled_ff=CI9570Air2Dot5,pxTHA3,!pxGPA3,i18nOn,TONB2256Air3Migration,!RMTAir3Talent,!CI10270Air2Dot5QTAllocations,!CI10857Air3Dot0,!MP16400Air3Migration,CI11132Air2Dot75,!pxFAA3,air2Dot76,!air2Dot76Qt,!CI12577UniversalSearch,!pxBPA3,OTBnrOn,!TONB3476Air3Migration,!SSINavUser,!JPAir3,!pxWTA3; XSRF-TOKEN=24767741651a2e9d998b97412320b645; cookie_prefix=; cookie_domain=.upwork.com; _cq_suid=1.1691952702.jwb3v0Gvz0RBeFgp; IR_gbd=upwork.com; IR_13634=1692285342094%7C0%7C1692285342094%7C%7C; visitor_gql_token=oauth2v2_078833e3d27387b92d714c0dfd1107c8; country_code=RS; __cf_bm=5RafVCf2WYTAWLtrjZzkSytsfUUSpBPrwTG9SvXgOho-1692286176-0-AXCwTjZLnY++eLIW2bFyOAhlGJthJ5cIvMygA2GtTDaQaVfaE1+u982TM3pbF7/lS7kfQFH0a7uprmzotmh49Oc=; umq=1536; _upw_ses.5831=*; forterToken=0e2888c99b2849afb6cd923aeff436f4_1692285339741__UDF43-m4_14ck; _gid=GA1.2.1343942159.1692276419; ln_or=eyI2MzgxNCI6ImQifQ%3D%3D; OptanonAlertBoxClosed=2023-08-17T12:47:02.580Z; g_state={"i_p":1692283625949,"i_l":1}; visitor_ui_gql_token=oauth2v2_d9b6e7d6f14953975522e09de910213f; att_vt=oauth2v2_dbc27e0828cf277e056fdf58601312bd; ftr_blst_1h=1692285325258; _uetsid=2748c0e03cfc11ee906c312c282d338c; _uetvid=727334003a0a11eea435af1147b96046',
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "TE": "trailers",
}  # ... any other headers you want to add
url = "https://www.upwork.com/services/product/video-audio-awesome-custom-animated-stickers-for-most-chat-platform-1480452950411137024"
session = requests.Session()

req = session.get(url, headers=headers)
print(req.headers)
src = req.text
find_product_info(src)
# soup = BeautifulSoup(src, "lxml")
# print(soup)
