#!user/bin/dev/env python3
# -*- coding: utf-8 -*-

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.database import Base, engine
from app.routers.auth import router as router_auth
from app.routers.health import router as router_health
from app.routers.healthcheck_heroku import router as router_healthcheck_heroku
from app.routers.permission import router as router_permission
from app.routers.role import router as router_role
from app.routers.shutdown import router as router_shutdown
from app.routers.startup import router as router_startup
from app.routers.user import router as router_user
from app.settings import get_settings


Base.metadata.create_all(bind=engine)


app = FastAPI(
    debug=get_settings().api_debug,
    description="Role Base Access Control API to handle users, roles and permission",
    title="RBAC API",
    version="Bêta",
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=["*"],
)

app.include_router(router_auth)
app.include_router(router_health)
app.include_router(router_healthcheck_heroku)
app.include_router(router_permission)
app.include_router(router_role)
app.include_router(router_shutdown)
app.include_router(router_startup)
app.include_router(router_user)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
