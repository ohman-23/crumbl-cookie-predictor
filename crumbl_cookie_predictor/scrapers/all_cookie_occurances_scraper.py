import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from cleantext import clean
from crumbl_cookie_predictor.database import CookieEntries, Database, DatabaseNames
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path="chromedriver", options=options)
    return driver


def get_number_of_weeks(soup):
    """
    Determine the number of weeks that are currently accounted for in the Crumbl Cookies Weekly Flavor website
    """
    containers = soup.find_all("div", {"class": "elementor-container"})
    return len(containers)


def get_utc_datetime(date_str):
    """
    Function description - formats: (MM Dth|rd|st-Dth|rd|st, YYYY), or (MM Dth|rd|st - MM Dth|rd|st, YYYY),
    or (December 27th, 2021 – January 1st, 2022)
    """
    title_arr = date_str.split(",")
    if len(title_arr) > 2:
        title_arr = [title_arr[0], title_arr[2]]
    title_arr[0] = re.split(re.compile(r"(\s)*([–-])(\s)*"), title_arr[0])[0].strip()
    if re.findall(re.compile(r"(\dth)|(\dst)|(\drd)|(\dnd)"), title_arr[0]):
        title_arr[0] = title_arr[0][:-2]
    # edge case fix (spelling mistake), happens once:
    format_edge_cases(title_arr)
    title_arr[1] = title_arr[1].strip()
    title = " ".join(title_arr)
    return datetime.strptime(title, "%B %d %Y"), title


def format_edge_cases(title_arr):
    title_arr[0] = re.sub(re.compile(r"Janruary"), "January", title_arr[0])
    title_arr[0] = re.sub(re.compile(r"Dec\s"), "December ", title_arr[0])
    title_arr[0] = re.sub(re.compile(r"Nov\s"), "November ", title_arr[0])


def get_all_past_cookies(soup):
    """
    Function description - strangely enough, sometimes dates are double counted? Have to track and make sure we don't do that
    """
    date_seen = {}
    weeks = soup.find_all("div", {"class": "elementor-container"})
    for week in weeks:
        title = week.find("h2", {"class": "elementor-heading-title elementor-size-default"})
        title_text = re.sub(re.compile(r"(For the week of)|(None)"), "", title.text).strip()
        utc_datetime, formated_date = get_utc_datetime(title_text)
        if date_seen.get(formated_date, None) is not None:
            continue
        date_seen[formated_date] = True

        # MAKE/FORMAT DATE INTO THE FORMAT YOU WANT! (UTC Date OBJECT!)
        print(formated_date)
        flavors = week.find_all("div", {"class": "jet-listing-dynamic-repeater__item"})
        for flavor in flavors:
            text = clean(flavor.text, no_emoji=True)[2:].strip()
            print(text)
            # MAP COOKIE TEXT TO A COOKIE OBJECT/DATABASE


def run_scrape(URL):
    """
    TODO: Function description
    """
    print("Initializing Selenium Web Driver...")
    driver = init_driver()
    driver.get(URL)
    # wait for page to load
    time.sleep(4)

    weeks_counted = 0
    for _ in range(10):
        print("Scrolling...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4)
        card_container = driver.find_element(
            by=By.XPATH, value="/html/body/div/div[2]/div/div/div/section[2]/div/div/div/div/div"
        )
        soup = BeautifulSoup(card_container.get_attribute("innerHTML"), "html.parser")
        temp_count = get_number_of_weeks(soup)
        if temp_count == weeks_counted:
            get_all_past_cookies(soup)
            driver.close()
            return
        weeks_counted = temp_count


if __name__ == "__main__":
    # database = Database(DatabaseNames.DESCRIPTIVE)
    # query = database.session.query(CookieEntries).all()
    # print(query)
    run_scrape("https://crumblcookieflavors.com/")
