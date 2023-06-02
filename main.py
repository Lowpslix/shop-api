from fastapi import FastAPI

from server.database import init_db
from server.routes.admin import router as adminRoutes
from server.routes.auth import router as authRouter
from server.routes.shop import router as shopRouter

app = FastAPI()

app.include_router(adminRoutes, tags=["Admin Operations"], prefix="/admin")
app.include_router(shopRouter, tags=["User Operations"])
app.include_router(authRouter, tags=["Auth"])


@app.on_event("startup")
async def start_db():
    await init_db()


@app.get("/", tags=["Root"])
async def read_root() -> dict:
    return {"msg": "Welcome to our store"}
