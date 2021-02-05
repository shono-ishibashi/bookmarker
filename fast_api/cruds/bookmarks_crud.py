from typing import List

from bson.objectid import ObjectId
from fastapi import HTTPException
from pymongo.cursor import Cursor

from database import db
from models.bookmark_models import BookMarkSchema


def bookmark_helper(bookmark) -> dict:
    return {
        "id": str(bookmark["_id"]),
        "title": bookmark["title"],
        "url": bookmark["url"],
        "memo": bookmark["memo"],
        "tags": bookmark["tags"],
        "user_id": bookmark["user_id"]
    }


def convert_schema_to_dict(bookmark_schema: BookMarkSchema) -> dict:
    return {
        "title": bookmark_schema.title,
        "url": bookmark_schema.url,
        "memo": bookmark_schema.memo,
        "tags": bookmark_schema.tags
    }


def fetch_bookmarks(user_id: str, search_words: List[str]) -> List[dict]:
    # 検索条件があれば、絞り込み
    # なければ全件取得
    if len(search_words) != 0:
        search_filter_array = []
        for search_word in search_words:
            search_filter_array.append({'title': {'$regex': search_word, "$options": "i"}})
            search_filter_array.append({'memo': {'$regex': search_word, "$options": "i"}})
        search_filter_array.append({'tags': {'$in': search_words}})
        search_filter = {'$or': search_filter_array, "user_id": user_id}
        bookmarks = db.bookmarks.find(filter=search_filter)
    else:
        bookmarks: Cursor = db.bookmarks.find({"user_id": user_id})

    bookmarks_dict = []
    print("###############")
    print(bookmarks.count())
    print("###############")

    if bookmarks.count() != 0:
        for bookmark in bookmarks:
            bookmarks_dict.append(bookmark_helper(bookmark))
    return bookmarks_dict


def fetch_bookmark(user_id: str, bookmark_id: str) -> dict:
    bookmark = db.bookmarks.find_one({"user_id": user_id,
                                      "_id": ObjectId(bookmark_id)})
    if bookmark is None:
        raise HTTPException(status_code=404)
    return bookmark_helper(bookmark)


def add_bookmark(bookmark_data: BookMarkSchema, user_id: str) -> dict:
    """
    bookmarkをdbに追加

    :param user_id: ログイン中のユーザーid
    :param bookmark_data: 追加するbookmarkのデータ
    :return: 追加したデータ
    """
    bookmark_dict = convert_schema_to_dict(bookmark_data)
    bookmark_dict["user_id"] = user_id
    bookmark = db.bookmarks.insert_one(bookmark_dict)
    new_bookmark = \
        db.bookmarks.find_one({"_id": bookmark.inserted_id})
    return bookmark_helper(new_bookmark)


def update_bookmark(bookmark_id: str, user_id: str, bookmark_data: BookMarkSchema) -> bool:
    """
    bookmarkを更新

    :param user_id: ログイン中のユーザーデータ
    :param bookmark_id: bookmarkのid
    :param bookmark_data: bookmarkのデータ
    :return: True:　更新ができた False: 更新できなかった
    """
    bookmark_dict = convert_schema_to_dict(bookmark_data)
    if len(bookmark_dict) < 1:
        return False
    bookmark = db.bookmarks.find_one({"_id": ObjectId(bookmark_id), "user_id": user_id})
    if bookmark:
        updated_bookmark = db.bookmarks.update_one(
            {"_id": ObjectId(bookmark_id)}, {"$set": bookmark_dict}
        )
        if updated_bookmark:
            return True
    return False


def quick_add_bookmark(bookmark_dict: dict, user_id: str):
    bookmark_dict["user_id"] = user_id
    bookmark = db.bookmarks.insert_one(bookmark_dict)
    new_bookmark = \
        db.bookmarks.find_one({"_id": bookmark.inserted_id})
    return bookmark_helper(new_bookmark)


def delete_bookmark(bookmark_id: str, user_id: str):
    db.bookmarks.delete_one({"_id": ObjectId(bookmark_id)})
