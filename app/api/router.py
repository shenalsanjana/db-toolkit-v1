from ninja import Router
from app.api.auth import router as auth_router

api_router = Router()

api_router.add_router("/auth", auth_router)
