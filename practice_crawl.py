from selenium import webdriver
import json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


hotel = []
json_data = {}
count = 0
driver = webdriver.Firefox(executable_path="geckodriver.exe")
driver.get("https://travel.rakuten.co.jp/yado/hokkaido/A.html")
# driver.get("https://search.travel.rakuten.co.jp/ds/yado/hokkaido/A-p3")
driver.implicitly_wait(5)
driver.maximize_window()
try:
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.htlList")))
    while driver.current_url:
        title = [title_element.text for title_element in driver.find_elements(By.CSS_SELECTOR, "div.info > h1 > a")]
        price = [price_element.text for price_element in driver.find_elements(By.CSS_SELECTOR, "div.info > p.htlPrice > span:nth-child(1)")]
        url = [url_element.get_attribute("href") for url_element in driver.find_elements(By.CSS_SELECTOR, "div.info > h1 > a")]
        # if driver.find_elements(By.CSS_SELECTOR, "div.paging > ul.pagingNumber > li.pagingTo > span.pagingActive"):
        for i in range(len(title)):
            json_data = {}
            count += 1
            try:
                driver.find_elements(By.CSS_SELECTOR, "div.info > p.htlPrice > span:nth-child(1)")
                json_data["index"] = count
                json_data["title"] = title[i]
                json_data["url"] = url[i]
                json_data["price"] = price[i]
            except:
                json_data["index"] = count
                json_data["title"] = title[i]
                json_data["url"] = url[i]
                json_data["price"] = None
            hotel.append(json_data)
        jsonString = json.dumps(hotel, indent=1, separators=(",", ":"))
        jsonFile = open("data.json", "w+")
        jsonFile.write(jsonString)
        jsonFile.close()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.paging > ul.pagingNumber > li.pagingBack > a"))).click()
except TimeoutException as e:
    print(e)
    driver.close()
