import typing
from typing import Dict, List, Optional, Set, Type, Union

from fastapi import Depends, HTTPException
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN
from tortoise import Model as TortoiseModel

from fastapi_admin.depends import get_current_admin
from fastapi_admin.permissions import PermissionAction, Role, get_role_by_name, has_permission
from fastapi_admin.providers import Provider
from fastapi_admin.resources import Field, Model

if typing.TYPE_CHECKING:
    from fastapi_admin.app import FastAPIAdmin


class CodePermissionProvider(Provider):
    name = "permission_provider"

    def __init__(self):
        self._cache = {}  # Простое кэширование для уменьшения вычислений

    async def register(self, app: "FastAPIAdmin"):
        await super(CodePermissionProvider, self).register(app)
        app.add_middleware(self._permission_middleware_class(self))

    def _permission_middleware_class(self, provider):
        """Создание класса middleware для проверки разрешений"""
        
        class PermissionMiddleware:
            def __init__(self, app):
                self.app = app
                self.provider = provider

            async def __call__(self, request, call_next):
                # Добавляем провайдер в запрос для использования в зависимостях
                request.state.permission_provider = self.provider
                return await call_next(request)

        return PermissionMiddleware

    async def clear_cache(self):
        """Очистка кэша разрешений"""
        self._cache = {}

    async def get_admin_roles(self, admin) -> List[str]:
        """Получение имен ролей администратора"""
        if not hasattr(admin, "roles"):
            return []
        
        return admin.roles
            
    async def has_permission(
        self, 
        admin,
        model_resource: str,
        action: PermissionAction,
    ) -> bool:
        """Проверка наличия разрешения на действие над ресурсом"""
        # Получаем имена ролей пользователя
        role_names = await self.get_admin_roles(admin)
        
        # Проверяем наличие разрешения у ролей
        return has_permission(role_names, model_resource, action)
    
    async def get_allowed_fields(
        self,
        admin,
        model_resource: str,
        action: PermissionAction,
    ) -> Optional[Set[str]]:
        """Получение списка разрешенных полей для ресурса"""
        # Получаем имена ролей пользователя
        role_names = await self.get_admin_roles(admin)
        
        # Для каждой роли проверяем разрешенные поля
        for role_name in role_names:
            role = get_role_by_name(role_name)
            if role:
                # Если роль * (админская), возвращаем None (все поля)
                if role.has_permission("*", action):
                    return None
                    
                # Если есть разрешение для данной модели и действия
                if role.has_permission(model_resource, action):
                    return role.get_allowed_fields(model_resource, action)
        
        # Если нет доступа ни к одному полю
        return set()
    
    async def filter_model_resources(
        self,
        admin,
        resources: List[dict],
    ) -> List[dict]:
        """Фильтрация ресурсов, доступных пользователю"""
        filtered_resources = []
        
        for resource in resources:
            resource_type = resource.get("type")
            
            # Если это ссылка, то просто добавляем её
            if resource_type == "link":
                filtered_resources.append(resource)
                continue
                
            # Если это модель, проверяем права доступа
            elif resource_type == "model":
                model_name = resource.get("model")
                has_access = await self.has_permission(
                    admin, model_name, PermissionAction.READ
                )
                
                if has_access:
                    filtered_resources.append(resource)
                    
            # Если это выпадающее меню, фильтруем его содержимое
            elif resource_type == "dropdown":
                sub_resources = resource.get("resources", [])
                filtered_sub = await self.filter_model_resources(admin, sub_resources)
                
                # Добавляем выпадающее меню только если есть доступные подресурсы
                if filtered_sub:
                    resource_copy = resource.copy()
                    resource_copy["resources"] = filtered_sub
                    filtered_resources.append(resource_copy)
        
        return filtered_resources
    
    async def filter_fields(
        self,
        admin,
        model_resource: str,
        action: PermissionAction,
        fields: List[Field],
    ) -> List[Field]:
        """Фильтрация полей на основе разрешений"""
        allowed_fields = await self.get_allowed_fields(admin, model_resource, action)
        
        # Если нет ограничений по полям, возвращаем все поля
        if allowed_fields is None:
            return fields
            
        return [field for field in fields if field.name in allowed_fields]


# Зависимости для использования в маршрутах

def get_permission_provider(request: Request) -> CodePermissionProvider:
    """Получение провайдера разрешений из запроса"""
    return request.state.permission_provider


async def check_model_permission(
    request: Request,
    action: PermissionAction,
    provider: CodePermissionProvider = Depends(get_permission_provider),
    admin = Depends(get_current_admin),
    model_resource: Optional[str] = None,
):
    """Проверка прав на действие с моделью"""
    if model_resource is None:
        path_params = request.path_params
        model_resource = path_params.get("resource")
    
    if not model_resource:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Resource not specified",
        )
    
    has_permission = await provider.has_permission(admin, model_resource, action)
    
    if not has_permission:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f"No permission for {action} on {model_resource}",
        )
    
    return True 