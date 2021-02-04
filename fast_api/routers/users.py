# from fastapi import APIRouter, Body, Depends, HTTPException
# from fastapi.encoders import jsonable_encoder
#
# from cruds import users
# from models import UserSchema, UpdateUserModel
#
# router = APIRouter()
#
#
# @router.get("/")
# def get_test():
#     return "user_test"
#
#
# @router.post("/user", response_description="user data added into into the database")
# def add_user(user: UserSchema = Body(...)):
#     user_json = jsonable_encoder(user)
#     return users.add_user(user_json)
