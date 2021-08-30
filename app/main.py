#!user/bin/dev/env python3
# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers.user import router as router_user
from app.routers.startup import router as router_startup
from app.routers.permission import router as router_permission
from app.routers.role import router as router_role
from app.routers.auth import router as router_auth
from app.settings import get_settings


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="RBAC API",
    description="Role Base Access Control API to handle users, roles and permission",
    version="Bêta",
    debug=get_settings().api_debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_startup)
app.include_router(router_user)
app.include_router(router_permission)
app.include_router(router_role)
app.include_router(router_auth)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")

