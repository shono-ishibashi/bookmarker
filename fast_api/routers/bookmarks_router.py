import uuid
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Query

from cruds import bookmarks_crud
from models.bookmark_models import BookMarkSchema
from auth.fastapi_users_setup import fastapi_users, User
from utils import url_util

router = APIRouter()


@router.get("/")
def fetch_bookmarks(search_words: Optional[List[str]] = Query(None),
                    user: User = Depends(fastapi_users.get_current_user)):
    user_id = user.id.__str__()
    uniq_search_words = []
    # 重複を削除
    if search_words:
        uniq_search_words = list(set(search_words))
    bookmarks = bookmarks_crud.fetch_bookmarks(user_id, uniq_search_words)
    print(bookmarks)
    return bookmarks


@router.get("/{bookmark_id}")
def fetch_bookmarks(bookmark_id: str, user: User = Depends(fastapi_users.get_current_user)):
    user_id = user.id.__str__()
    bookmark = bookmarks_crud.fetch_bookmark(user_id, bookmark_id)
    return bookmark


@router.post("/")
def add_bookmark(user: User = Depends(fastapi_users.get_current_user),
                 bookmark: BookMarkSchema = Body(...)):
    user_id = user.id.__str__()
    inserted_bookmark = bookmarks_crud.add_bookmark(bookmark, user_id)
    return inserted_bookmark


@router.post("/quickadd")
def quick_add_bookmark(url: str, user: User = Depends(fastapi_users.get_current_user)):
    user_id = user.id.__str__()
    bookmark = url_util.fetch_site_info(url)
    inserted_bookmark = bookmarks_crud.quick_add_bookmark(bookmark, user_id)
    return inserted_bookmark


@router.put("/{bookmark_id}")
def update_bookmark(
        bookmark_id: str,
        user: User = Depends(fastapi_users.get_current_user),
        bookmark_data: BookMarkSchema = Body(...)):
    user_id = user.id.__str__()
    is_update_succeeded = \
        bookmarks_crud.update_bookmark(bookmark_id, user_id, bookmark_data)
    if is_update_succeeded:
        return "更新に成功しました"
    return "更新に失敗しました"


@router.delete("/{bookmark_id}")
def delete_bookmark(
        bookmark_id: str,
        user: User = Depends(fastapi_users.get_current_user)):
    print("bookmark_id", bookmark_id)
    user_id = user.id.__str__()
    bookmarks_crud.delete_bookmark(bookmark_id, user_id)
