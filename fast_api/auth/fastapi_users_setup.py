import motor.motor_asyncio
from fastapi import Request
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import JWTAuthentication, BaseAuthentication
from fastapi_users.db import MongoDBUserDatabase

from database import DATABASE_URL


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


SECRET = "SECRET"

client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)

db = client["bookmarker"]
collection = db["users"]
user_db = MongoDBUserDatabase(UserDB, collection)


def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")


jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=100000000, tokenUrl="/auth/jwt/login", name="my-jwt"
)

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

auth_router = fastapi_users.get_auth_router(jwt_authentication)

register_router = fastapi_users.get_register_router(on_after_register)

reset_password_router = fastapi_users.get_reset_password_router(
    SECRET, after_forgot_password=on_after_forgot_password
)

verify_router = fastapi_users.get_verify_router(
    SECRET, after_verification_request=after_verification_request
)

users_router = fastapi_users.get_users_router()
