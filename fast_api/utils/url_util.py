import requests
from bs4 import BeautifulSoup

from models.bookmark_models import BookMarkSchema


def fetch_site_info(url: str) -> dict or None:
    response = requests.get(url=url)
    if response.status_code == 200:
        response_text = response.text

        soup = BeautifulSoup(response_text, "html.parser")
        soup_title = soup.find("title").text
        print(soup_title)

        bookmark = {
            "url": url,
            "title": soup_title,
            "memo": "",
            "tags": []
        }
        return bookmark

    return None
