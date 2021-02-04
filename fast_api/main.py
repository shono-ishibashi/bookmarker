from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from auth.fastapi_users_setup import (
    auth_router,
    register_router,
    reset_password_router,
    verify_router,
    users_router
)

from routers import bookmarks_router, url_utils_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,  # 追記により追加
    allow_methods=["*"],  # 追記により追加
    allow_headers=["*"]  # 追記により追加
)

# auth routers
app.include_router(
    auth_router, prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    register_router, prefix="/auth", tags=["auth"]
)
app.include_router(
    reset_password_router,
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    verify_router,
    prefix="/auth",
    tags=["auth"],
)
app.include_router(users_router, prefix="/users", tags=["users"])

# bookmarker router
app.include_router(bookmarks_router.router, prefix="/bookmark", tags=["bookmark"])

app.include_router(url_utils_router.router, prefix="/url-info", tags=["url_util"])
