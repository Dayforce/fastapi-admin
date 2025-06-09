import typing

if typing.TYPE_CHECKING:
    from fastapi_admin.app import FastAPIAdmin


class Provider:
    name = "provider"

    async def register(self, app: "FastAPIAdmin"):
        setattr(app, self.name, self)

# Импортируем провайдер разрешений на основе базы данных (устаревший)
from fastapi_admin.providers.permissions import PermissionProvider
# Импортируем провайдер разрешений на основе кода
from fastapi_admin.providers.code_permissions import CodePermissionProvider
