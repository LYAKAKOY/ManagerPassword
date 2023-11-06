from logging import getLogger
from fastapi import FastAPI
from fastapi.routing import APIRouter
from api.passwords.handlers import manager_password_router
from api.users.handlers import user_router

app = FastAPI(title="ManagerPassword")

logger = getLogger(__name__)

main_api_router = APIRouter()
main_api_router.include_router(manager_password_router, prefix="/password", tags=["password"])
main_api_router.include_router(user_router, prefix="/user", tags=["password"])

app.include_router(main_api_router)