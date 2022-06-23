import re

import requests
from bs4 import BeautifulSoup
from crumbl_cookie_predictor.database import CookieEntries, Database, DatabaseNames

IMAGE_PATH_PREFIX = "../imgs/"
IMAGE_FILE_TYPE = ".png"


def get_page_soup(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return soup


def download_and_save_image(img_link, cookie_name):
    image = requests.get(img_link).content
    img_path = f"{IMAGE_PATH_PREFIX}{cookie_name}{IMAGE_FILE_TYPE}"
    with open(img_path, "wb") as file:
        file.write(image)
    return img_path


def scrape_crumbl_site(url):
    database = Database(DatabaseNames.DESCRIPTIVE)
    soup = get_page_soup(url)
    cookie_elements = soup.find_all("li", {"id": re.compile("individual-cookie-flavor")})[:6]
    for cookie_soup in cookie_elements:
        img = cookie_soup.find_all("img", {"src": re.compile("https://")})[0]
        img_link = img["src"]
        info_div = cookie_soup.find_all("div", {"class": re.compile(r"_info|text-left")})[0]
        name = info_div.find_all("h3")[0].text.strip()
        desc = info_div.find_all("p")[0].text
        temperature = info_div.find_all("small")[0].text

        # download cookie image
        img_filepath = download_and_save_image(img_link, name)
        entry = CookieEntries(
            name,
            image=img_filepath,
            description=desc,
            temperature=temperature,
        )
        database.session.add(entry)
        database.session.commit()


if __name__ == "__main__":
    scrape_crumbl_site("https://crumblcookies.com/")
