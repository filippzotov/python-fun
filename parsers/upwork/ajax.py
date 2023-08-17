import requests
from bs4 import BeautifulSoup
import json

url = "https://www.upwork.com/ab/services/pub/api/catalog_search/search/vcs/v3?paging[cursorMark]=version_2_eyJzb3J0VmFsdWVzIjpudWxsLCJmcm9tIjoyNCwiYm9vc3RlZFByb2plY3RVaWRzIjpudWxsfQ==&paging[rows]=24&projectCategoryId=projectCategory:wordPress"


# url = "https://www.upwork.com/services/logo-design?all=true"
# headers = {
#     "Host": "www.upwork.com",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#     "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Alt-Used": "www.upwork.com",
#     "Connection": "keep-alive",
#     "Cookie": '__cflb=02DiuEXPXZVk436fJfSVuuwDqLqkhavJbs75W8ZSYZb6j; visitor_id=93.86.199.232.1691952699451000; device_view=full; _upw_id.5831=49c7b7a2-a5ca-4b60-b223-6ccde6436c88.1691952701.5.1692279497.1692276412.f6df83c0-23da-438b-84c6-45e22f7400c2.eed8b013-35aa-4096-bd04-728278c2fb56.d89f3b7c-ccd1-4878-a685-769ecf9a9a51.1692276417165.1145; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Aug+17+2023+15%3A36%3A56+GMT%2B0200+(%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%95%D0%B2%D1%80%D0%BE%D0%BF%D0%B0%2C+%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202305.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=88bd6fa8-8617-4c3d-8c97-a49723a83760&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=RS%3B00; AWSALB=COWlw6DEGFh+GgkPACh8zl7czmCZSYmLcuZL90LaSGHo/tODw0a1KHvuk7XfCDcw3ww4fYUWzzQKAH9W03aYYTHklNOsSoBjh+3/ZQdALyKZYFuJSAXnhLDWy8Wd; AWSALBCORS=COWlw6DEGFh+GgkPACh8zl7czmCZSYmLcuZL90LaSGHo/tODw0a1KHvuk7XfCDcw3ww4fYUWzzQKAH9W03aYYTHklNOsSoBjh+3/ZQdALyKZYFuJSAXnhLDWy8Wd; spt=0b279929-1e6a-4a92-a564-70d99c43d243; _gcl_au=1.1.1514201675.1691952702; _ga_KSM221PNDX=GS1.1.1692276417.4.1.1692279430.0.0.0; _ga=GA1.1.375872138.1691952702; _cq_duid=1.1691952702.RgK8TlFmFxGKOAn8; _mkto_trk=id:518-RKL-392&token:_mch-upwork.com-1691952703016-92939; _tt_enable_cookie=1; _ttp=Kc4UYs1EsWRoVIF9cY6EPyl0Zrj; _rdt_uuid=1691952703799.22d4b778-c26a-453b-93c1-127a9dc36d6d; __pdst=59d89d8629ba4e2e8dec0aaa1d722d93; _zitok=d03d12f56c10c301bea31691952703; _fbp=fb.1.1691952705084.1101960311; _cfuvid=f1JS0ZLmoMZaR0ChjDsPvau2nmhok0cMzIfF6959vCQ-1691952699202-0-604800000; enabled_ff=CI9570Air2Dot5,!pxWTA3,TONB2256Air3Migration,!CI10270Air2Dot5QTAllocations,!CI10857Air3Dot0,air2Dot76,!CI12577UniversalSearch,!JPAir3,i18nOn,!SSINavUser,!MP16400Air3Migration,OTBnrOn,pxTHA3,!pxFAA3,!pxGPA3,!air2Dot76Qt,!pxBPA3,CI11132Air2Dot75,!RMTAir3Talent,!TONB3476Air3Migration; XSRF-TOKEN=a93a06891f11a6d99ef5244d5ea9ff3b; cookie_prefix=; cookie_domain=.upwork.com; _cq_suid=1.1691952702.jwb3v0Gvz0RBeFgp; IR_gbd=upwork.com; IR_13634=1692279424293%7C0%7C1692279424293%7C%7C; visitor_gql_token=oauth2v2_078833e3d27387b92d714c0dfd1107c8; country_code=RS; __cf_bm=DvDh5sHZ2NQ1OkOK7bm.0dZmC2Rdm_HHG7OkREGd4RE-1692279153-0-Aa5HR9EBoMeBGkvweDNORsVq8edJ9tmXCBq0kG6knRbCXUBpniBhkUcswSxcJIoNS8R0WIWoZBuYDCqf7ABZDDM=; umq=1536; _upw_ses.5831=*; forterToken=0e2888c99b2849afb6cd923aeff436f4_1692279001661__UDF43-mnf-anf_14ck; ftr_blst_1h=1692276418260; _gid=GA1.2.1343942159.1692276419; ln_or=eyI2MzgxNCI6ImQifQ%3D%3D; OptanonAlertBoxClosed=2023-08-17T12:47:02.580Z; g_state={"i_p":1692283625949,"i_l":1}; visitor_ui_gql_token=oauth2v2_02c44dae5261cdb198b0bc3d861c3c6f; _uetsid=2748c0e03cfc11ee906c312c282d338c; _uetvid=727334003a0a11eea435af1147b96046',
#     "Upgrade-Insecure-Requests": "1",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "none",
#     "Sec-Fetch-User": "?1",
#     "TE": "trailers",
# }
req = requests.get(url)
src = req.text
page = json.loads(src)

version_2_eyJzb3J0VmFsdWVzIjpudWxsLCJmcm9tIjoyNCwiYm9vc3RlZFByb2plY3RVaWRzIjpudWxsfQ==                                                                                                                                                                                                                                                                                                                                       
version_2_eyJzb3J0VmFsdWVzIjpudWxsLCJmcm9tIjo0OCwiYm9vc3RlZFByb2plY3RVaWRzIjpudWxsfQ==                                                                                                                                                                                                                                                                                                                                            