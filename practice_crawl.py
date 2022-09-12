from genericpath import exists
from selenium import webdriver
import json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

hotel_ = []
count = 0
driver = webdriver.Firefox(executable_path="geckodriver.exe")
driver.get("https://travel.rakuten.co.jp/yado/hokkaido/A.html")
driver.implicitly_wait(5)
driver.maximize_window()
title = [
    title_element.text
    for title_element in driver.find_elements(By.CSS_SELECTOR, "h1 > a")
]
price = [
    price_element.text
    for price_element in driver.find_elements(
        By.CSS_SELECTOR, "p.htlPrice > span:nth-child(1)"
    )
]
url = [
    url_element.get_attribute("href")
    for url_element in driver.find_elements(By.CSS_SELECTOR, "h1 > a")
]

while (
    bool(
        WebDriverWait(driver, 5)
        .until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.paging > ul.pagingNumber > li.pagingBack > a")
            )
        )
        .click()
    )
    == False
):
    page = (
        WebDriverWait(driver, 5)
        .until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.paging > ul.pagingNumber > li.pagingBack > a")
            )
        )
        .click()
    )
    for i in range(len(title)) and range(len(url)) and range(len(price)):
        json_data = {}
        count += 1
        json_data["title"] = title[i]
        json_data["price"] = price[i]
        json_data["url"] = url[i]
        json_data["index"] = count
        hotel_.append(json_data)
    print(bool)
    jsonString = json.dumps(hotel_, indent=1, separators=(",", ":"))
    jsonFile = open("data.json", "w+")
    jsonFile.write(jsonString)
    jsonFile.close()
driver.close()
