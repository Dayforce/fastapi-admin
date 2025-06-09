import os
import sys

import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.providers.permissions import PermissionProvider
from fastapi_admin.resources import ActionType

# Импортируем модели из вашего проекта
# Замените этот путь на путь к своим моделям
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.models import Admin, Category, Config, Product, Role, Permission

# Создаем основное приложение FastAPI
app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Регистрируем FastAPI Admin как подприложение
app.mount("/admin", admin_app)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Создаем ресурсы для моделей
@app.on_event("startup")
async def startup():
    r = redis.Redis.from_url(
        "redis://localhost:6379/0", encoding="utf8", decode_responses=True
    )
    
    # Настраиваем FastAPI Admin
    await admin_app.configure(
        redis=r,
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        admin_path="/admin",
        template_folders=["examples/templates"],
        providers=[
            UsernamePasswordProvider(
                admin_model=Admin,
                login_logo_url="https://preview.tabler.io/static/logo.svg",
            ),
            # Регистрируем провайдер разрешений
            PermissionProvider(),
        ],
    )

    # Регистрируем ресурсы
    from examples.resources import (
        AdminResource,
        CategoryResource,
        ConfigResource,
        ProductResource,
        RoleResource,
        PermissionResource,
    )

    admin_app.register_resources(
        AdminResource,
        CategoryResource,
        ConfigResource,
        ProductResource,
        RoleResource, 
        PermissionResource,
    )


# Регистрируем модели Tortoise ORM
register_tortoise(
    app,
    config={
        "connections": {"default": "sqlite://./db.sqlite3"},
        "apps": {
            "models": {
                "models": ["examples.models"],
                "default_connection": "default",
            }
        },
        "use_tz": False,
        "timezone": "Asia/Shanghai",
    },
    generate_schemas=True,
)


if __name__ == "__main__":
    uvicorn.run("examples.role_based_auth:app", reload=True) 