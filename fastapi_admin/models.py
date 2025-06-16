from enum import Enum
from tortoise import Model, fields
from typing import List, Optional


class PermissionAction(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"


class Permission(Model):
    id = fields.IntField(pk=True)
    model_resource = fields.CharField(max_length=100)
    action = fields.CharEnumField(PermissionAction)
    conditions = fields.JSONField(default=dict)
    fields = fields.JSONField(default=dict)

    class Meta:
        table = "fastapi_admin_permission"
        unique_together = (("model_resource", "action"),)


class Role(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, unique=True)
    description = fields.TextField(null=True)
    permissions = fields.ManyToManyField("models.Permission", related_name="roles")

    class Meta:
        table = "fastapi_admin_role"


class AbstractAdmin(Model):
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=200)
    role_names = fields.JSONField(default=list)  # Список строк с именами ролей
    
    @property
    def roles(self) -> List[str]:
        """Возвращает список имен ролей пользователя"""
        return self.role_names if isinstance(self.role_names, list) else []
    
    @roles.setter
    def roles(self, value: List[str]):
        """Устанавливает список имен ролей пользователя"""
        self.role_names = value

    class Meta:
        abstract = True
