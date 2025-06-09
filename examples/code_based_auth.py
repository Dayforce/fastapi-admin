import os
import sys

import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from fastapi_admin.app import app as admin_app
from fastapi_admin.permissions import (
    Permission, PermissionAction, Role, register_role, 
    ADMIN_ROLE, create_editor_role, create_viewer_role
)
from fastapi_admin.providers.code_permissions import CodePermissionProvider
from fastapi_admin.providers.login import UsernamePasswordProvider

# Импортируем модели из вашего проекта
# Замените этот путь на путь к своим моделям
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from examples.models import Admin, Category, Config, Product


# Определяем пользовательские роли
CATALOG_EDITOR = create_editor_role(["category", "product"])
CATALOG_VIEWER = create_viewer_role(["category", "product"])

# Роль для работы только с настройками
CONFIG_MANAGER = Role(
    name="config_manager",
    permissions=[
        Permission(model_name="config", action=PermissionAction.CREATE),
        Permission(model_name="config", action=PermissionAction.READ),
        Permission(model_name="config", action=PermissionAction.UPDATE),
        Permission(model_name="config", action=PermissionAction.DELETE),
    ]
)

# Регистрируем пользовательские роли
register_role(CATALOG_EDITOR)
register_role(CATALOG_VIEWER)
register_role(CONFIG_MANAGER)

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
            # Регистрируем провайдер разрешений на основе кода
            CodePermissionProvider(),
        ],
    )

    # Регистрируем ресурсы
    from examples.resources import (
        AdminResource,
        CategoryResource,
        ConfigResource,
        ProductResource,
    )

    admin_app.register_resources(
        AdminResource,
        CategoryResource,
        ConfigResource,
        ProductResource,
    )
    
    # Создаем тестовых администраторов с разными ролями, если их нет
    admin_count = await Admin.all().count()
    if admin_count == 0:
        # Администратор с полными правами
        await Admin.create(
            username="admin",
            password="admin",
            role_names=["admin"]  # Роль определена в fastapi_admin.permissions 
        )
        
        # Редактор каталога
        await Admin.create(
            username="editor",
            password="editor",
            role_names=["editor_category+product"]  # Роль создана через create_editor_role
        )
        
        # Просмотрщик каталога
        await Admin.create(
            username="viewer",
            password="viewer",
            role_names=["viewer_category+product"]  # Роль создана через create_viewer_role
        )
        
        # Менеджер настроек
        await Admin.create(
            username="config",
            password="config",
            role_names=["config_manager"]  # Пользовательская роль
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
    uvicorn.run("examples.code_based_auth:app", reload=True) 