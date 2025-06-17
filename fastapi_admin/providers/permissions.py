import typing
from typing import Dict, List, Optional, Set, Type, Union

from fastapi import Depends, HTTPException
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN
from tortoise import Model as TortoiseModel

from fastapi_admin.depends import get_current_admin
from fastapi_admin.models import AbstractAdmin, Permission, PermissionAction, Role
from fastapi_admin.providers import Provider
from fastapi_admin.resources import Field, Model

if typing.TYPE_CHECKING:
    from fastapi_admin.app import FastAPIAdmin


class PermissionProvider(Provider):
    name = "permission_provider"

    def __init__(self):
        self._cache = {}  # Простое кэширование для уменьшения запросов к БД

    async def register(self, app: "FastAPIAdmin"):
        await super(PermissionProvider, self).register(app)
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

    async def get_admin_roles(self, admin: AbstractAdmin) -> List[Role]:
        """Получение ролей администратора"""
        if not hasattr(admin, "roles"):
            return []
            
        # Загружаем связанные роли, если еще не загружены
        if not hasattr(admin, "_roles_loaded"):
            await admin.fetch_related("roles")
            setattr(admin, "_roles_loaded", True)
            
        return admin.roles

    async def get_role_permissions(self, role: Role) -> List[Permission]:
        """Получение разрешений для роли"""
        if not hasattr(role, "permissions"):
            return []
            
        # Загружаем связанные разрешения, если еще не загружены
        if not hasattr(role, "_permissions_loaded"):
            await role.fetch_related("permissions")
            setattr(role, "_permissions_loaded", True)
            
        return role.permissions

    async def get_admin_permissions(self, admin: AbstractAdmin) -> Dict[str, Dict[str, Permission]]:
        """Получение всех разрешений администратора"""
        # Проверяем кэш
        admin_id = getattr(admin, "id", None) or getattr(admin, "pk", None)
        if admin_id and admin_id in self._cache:
            return self._cache[admin_id]
            
        # Получаем все роли пользователя
        roles = await self.get_admin_roles(admin)
        
        # Собираем все разрешения из всех ролей
        permissions = {}
        for role in roles:
            role_permissions = await self.get_role_permissions(role)
            for permission in role_permissions:
                model_resource = permission.model_resource
                action = permission.action
                if model_resource not in permissions:
                    permissions[model_resource] = {}
                permissions[model_resource][action] = permission
        
        # Кэшируем результат
        if admin_id:
            self._cache[admin_id] = permissions
            
        return permissions
    
    async def has_permission(
        self, 
        admin: AbstractAdmin,
        model_resource: str,
        action: PermissionAction,
    ) -> bool:
        """Проверка наличия разрешения на действие над ресурсом"""
        # Получаем все разрешения пользователя
        permissions = await self.get_admin_permissions(admin)
        
        # Проверяем наличие разрешения для модели и действия
        return (
            model_resource in permissions and
            action in permissions[model_resource]
        )
    
    async def get_allowed_fields(
        self,
        admin: AbstractAdmin,
        model_resource: str,
        action: PermissionAction,
    ) -> Optional[Set[str]]:
        """Получение списка разрешенных полей для ресурса"""
        permissions = await self.get_admin_permissions(admin)
        
        if (
            model_resource not in permissions or
            action not in permissions[model_resource]
        ):
            return None
            
        permission = permissions[model_resource][action]
        fields = permission.fields
        
        # Если поля не указаны, то разрешены все поля
        if not fields or not fields.get("allowed"):
            return None
            
        return set(fields.get("allowed", []))
    
    async def filter_model_resources(
        self,
        admin: AbstractAdmin,
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
        admin: AbstractAdmin,
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

def get_permission_provider(request: Request) -> PermissionProvider:
    """Получение провайдера разрешений из запроса"""
    return request.state.permission_provider


async def check_model_permission(
    request: Request,
    action: PermissionAction,
    provider: PermissionProvider = Depends(get_permission_provider),
    admin: AbstractAdmin = Depends(get_current_admin),
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

# Добавляем функции-помощники для разных типов разрешений
def require_read_permission():
    """Проверка на право чтения ресурса"""
    async def check_permission(
        request: Request,
        provider: PermissionProvider = Depends(get_permission_provider),
        admin: AbstractAdmin = Depends(get_current_admin),
    ):
        return await check_model_permission(
            request=request,
            action=PermissionAction.READ,
            provider=provider,
            admin=admin
        )
    return Depends(check_permission)

def require_create_permission():
    """Проверка на право создания ресурса"""
    async def check_permission(
        request: Request,
        provider: PermissionProvider = Depends(get_permission_provider),
        admin: AbstractAdmin = Depends(get_current_admin),
    ):
        return await check_model_permission(
            request=request,
            action=PermissionAction.CREATE,
            provider=provider,
            admin=admin
        )
    return Depends(check_permission)

def require_update_permission():
    """Проверка на право обновления ресурса"""
    async def check_permission(
        request: Request,
        provider: PermissionProvider = Depends(get_permission_provider),
        admin: AbstractAdmin = Depends(get_current_admin),
    ):
        return await check_model_permission(
            request=request,
            action=PermissionAction.UPDATE,
            provider=provider,
            admin=admin
        )
    return Depends(check_permission)

def require_delete_permission():
    """Проверка на право удаления ресурса"""
    async def check_permission(
        request: Request,
        provider: PermissionProvider = Depends(get_permission_provider),
        admin: AbstractAdmin = Depends(get_current_admin),
    ):
        return await check_model_permission(
            request=request,
            action=PermissionAction.DELETE,
            provider=provider,
            admin=admin
        )
    return Depends(check_permission) 