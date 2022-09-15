from selenium import webdriver
import json
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


def rakuten_crawl():
    hotel = []
    count = 0
    driver = webdriver.Firefox(executable_path="geckodriver.exe")
    driver.get("https://travel.rakuten.co.jp/yado/hokkaido/A.html")
    # driver.get("https://search.travel.rakuten.co.jp/ds/yado/hokkaido/A-p3")
    driver.maximize_window()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.htlList")))
    try:
        driver.find_elements(
            By.CSS_SELECTOR, "div.paging > ul.pagingNumber > li.pagingTo > span.pagingActive")
        while True:
            hotel_lst = [elem for elem in driver.find_elements(
                By.CSS_SELECTOR, "ul.htlList > li")]
            for htl in range(len(hotel_lst)):
                title = driver.find_elements(
                    By.CSS_SELECTOR, "div.info > h1 > a")
                price = driver.find_elements(
                    By.CSS_SELECTOR, "div.info > p.htlPrice > span:nth-child(1)")
                url = driver.find_elements(
                    By.CSS_SELECTOR, "div.info > h1 > a")
                json_data = {}
                count += 1
                try:
                    json_data["index"] = count
                    json_data["title"] = title[htl].text
                    json_data["url"] = url[htl].get_attribute("href")
                    json_data["price"] = price[htl].text
                    hotel.append(json_data)
                except:
                    json_data["index"] = count
                    json_data["title"] = title[htl].text
                    json_data["url"] = url[htl].get_attribute("href")
                    json_data["price"] = None
                    hotel.append(json_data)
            jsonString = json.dumps(hotel, indent=1, separators=(",", ":"))
            jsonFile = open("data.json", "w+")
            jsonFile.write(jsonString)
            jsonFile.close()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.paging > ul.pagingNumber > li.pagingBack > a"))).click()
    except TimeoutException as e:
        print(e)
        driver.close()


def main():
    crawl = rakuten_crawl()
    return crawl


if __name__ == "__main__":
    main()
