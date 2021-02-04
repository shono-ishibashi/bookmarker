from fastapi import APIRouter

from utils.url_util import fetch_site_info

router = APIRouter()


@router.get("/")
def fetch_url_info(url: str):
    return fetch_site_info(url)
