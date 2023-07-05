from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import pandas as pd


def scrap(job_name):
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://hh.ru/?hhtmFrom=vacancy_search_list")
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "bloko-input-text").send_keys(job_name)
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "supernova-search-submit-text").click()
    time.sleep(1)
    res = check_all_pages(driver)

    create_csv_file(res, job_name)
    driver.close()


def check_all_pages(driver):
    ans = []
    while True:
        time.sleep(1)
        try:
            ans.extend(scrap_hh_page(driver))
            element = driver.find_element(By.CLASS_NAME, "bloko-gap_top")
            element.find_element(By.CSS_SELECTOR, "[data-qa='pager-next']").click()
            time.sleep(2)
            print("page done")
        except:
            break
    return ans


def scrap_hh_page(driver):
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "serp-item"))
    )
    res = []
    for i in elements:
        tmp = []
        name = i.find_element(By.CLASS_NAME, "serp-item__title")
        expirience = i.find_element(By.CLASS_NAME, "bloko-h-spacing-container_base-0")
        try:
            data = "vacancy-serp__vacancy-compensation"
            salary = i.find_element(By.CSS_SELECTOR, f"[data-qa='{data}']").text
        except:
            salary = ""
        tmp = [name.text, salary, expirience.text]
        res.append(tmp)
    return res


def create_csv_file(jobs, file_name):
    frame = pd.DataFrame(convert_list_to_dict(jobs))
    frame.to_csv(f"{file_name}.csv")


def convert_list_to_dict(jobs_list):
    d = {
        "name": [],
        "salary": [],
        "expirience": [],
    }
    for job in jobs_list:
        d["name"].append(job[0])
        d["salary"].append(job[1])
        d["expirience"].append(job[2])
    return d


# serp-item

if __name__ == "__main__":
    print("enter job name")
    name = input()
    scrap(name)
