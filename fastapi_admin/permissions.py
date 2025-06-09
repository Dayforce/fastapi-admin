from enum import Enum
from typing import Dict, List, Optional, Set, Type, Union
import functools

from tortoise import Model as TortoiseModel


class PermissionAction(str, Enum):
    """Типы действий для разрешений"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"


class Permission:
    """Класс разрешения для модели"""
    
    def __init__(
        self, 
        model_name: str, 
        action: PermissionAction,
        allowed_fields: Optional[List[str]] = None,
        conditions: Optional[Dict] = None,
    ):
        self.model_name = model_name
        self.action = action
        self.allowed_fields = set(allowed_fields) if allowed_fields else None
        self.conditions = conditions or {}
    
    def __repr__(self):
        return f"<Permission: {self.model_name}.{self.action}>"


class Role:
    """Класс роли с набором разрешений"""
    
    def __init__(self, name: str, permissions: Optional[List[Permission]] = None):
        self.name = name
        self.permissions = permissions or []
        # Создаем индекс для быстрой проверки разрешений
        self._permissions_index = {}
        for permission in self.permissions:
            if permission.model_name not in self._permissions_index:
                self._permissions_index[permission.model_name] = {}
            self._permissions_index[permission.model_name][permission.action] = permission
    
    def has_permission(self, model_name: str, action: PermissionAction) -> bool:
        """Проверяет наличие разрешения для модели и действия"""
        return (model_name in self._permissions_index and 
                action in self._permissions_index[model_name])
    
    def get_allowed_fields(self, model_name: str, action: PermissionAction) -> Optional[Set[str]]:
        """Возвращает список разрешенных полей для модели и действия"""
        if not self.has_permission(model_name, action):
            return None
            
        permission = self._permissions_index[model_name][action]
        return permission.allowed_fields
    
    def __repr__(self):
        return f"<Role: {self.name}>"


# Роль с полным доступом
ADMIN_ROLE = Role(
    name="admin",
    permissions=[
        Permission(model_name="*", action=PermissionAction.CREATE),
        Permission(model_name="*", action=PermissionAction.READ),
        Permission(model_name="*", action=PermissionAction.UPDATE),
        Permission(model_name="*", action=PermissionAction.DELETE),
    ]
)


# Пустая роль для создания пользовательских ролей
EMPTY_ROLE = Role(name="empty", permissions=[])


# Словарь доступных ролей
ROLES = {
    "admin": ADMIN_ROLE,
    "empty": EMPTY_ROLE,
}


def create_editor_role(model_names: List[str]) -> Role:
    """Создает роль редактора для указанных моделей"""
    permissions = []
    for model_name in model_names:
        permissions.extend([
            Permission(model_name=model_name, action=PermissionAction.CREATE),
            Permission(model_name=model_name, action=PermissionAction.READ),
            Permission(model_name=model_name, action=PermissionAction.UPDATE),
        ])
    return Role(name=f"editor_{'+'.join(model_names)}", permissions=permissions)


def create_viewer_role(model_names: List[str]) -> Role:
    """Создает роль просмотрщика для указанных моделей"""
    permissions = []
    for model_name in model_names:
        permissions.append(Permission(model_name=model_name, action=PermissionAction.READ))
    return Role(name=f"viewer_{'+'.join(model_names)}", permissions=permissions)


def register_role(role: Role):
    """Регистрирует новую роль в системе"""
    ROLES[role.name] = role
    return role


def get_role_by_name(name: str) -> Optional[Role]:
    """Получает роль по имени"""
    return ROLES.get(name)


def has_permission(role_names: List[str], model_name: str, action: PermissionAction) -> bool:
    """Проверяет наличие разрешения для списка ролей"""
    for role_name in role_names:
        role = get_role_by_name(role_name)
        if role and (role.has_permission(model_name, action) or role.has_permission("*", action)):
            return True
    return False 