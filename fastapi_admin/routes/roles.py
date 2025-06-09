from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, Path, Query
from pydantic import BaseModel
from starlette.requests import Request
from tortoise.expressions import Q

from fastapi_admin.depends import get_current_admin, get_resources
from fastapi_admin.models import Permission, PermissionAction, Role
from fastapi_admin.template import templates

router = APIRouter()


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None


class RoleUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: List[int] = []


class PermissionCreate(BaseModel):
    model_resource: str
    action: PermissionAction
    fields: Dict = {}
    conditions: Dict = {}


# Страница списка ролей
@router.get("/roles")
async def roles_list(
    request: Request,
    resources=Depends(get_resources),
    admin=Depends(get_current_admin),
):
    roles = await Role.all()
    context = {
        "request": request,
        "resources": resources,
        "roles": roles,
        "page_title": "Управление ролями",
        "page_pre_title": "Система ролей",
    }
    return templates.TemplateResponse(
        "roles/list.html",
        context=context,
    )


# Страница создания роли
@router.get("/roles/create")
async def role_create_view(
    request: Request,
    resources=Depends(get_resources),
    admin=Depends(get_current_admin),
):
    context = {
        "request": request,
        "resources": resources,
        "page_title": "Создание роли",
        "page_pre_title": "Система ролей",
    }
    return templates.TemplateResponse(
        "roles/create.html",
        context=context,
    )


# API для создания роли
@router.post("/api/roles")
async def role_create(
    role: RoleCreate,
    admin=Depends(get_current_admin),
):
    return await Role.create(name=role.name, description=role.description)


# Страница редактирования роли
@router.get("/roles/{role_id}")
async def role_edit_view(
    request: Request,
    role_id: int = Path(...),
    resources=Depends(get_resources),
    admin=Depends(get_current_admin),
):
    role = await Role.get(id=role_id)
    await role.fetch_related("permissions")
    
    # Получаем все доступные разрешения
    all_permissions = await Permission.all()
    
    # Получаем ID разрешений, связанных с ролью
    role_permission_ids = [p.id for p in role.permissions]
    
    context = {
        "request": request,
        "resources": resources,
        "role": role,
        "all_permissions": all_permissions,
        "role_permission_ids": role_permission_ids,
        "page_title": f"Редактирование роли: {role.name}",
        "page_pre_title": "Система ролей",
    }
    return templates.TemplateResponse(
        "roles/edit.html",
        context=context,
    )


# API для обновления роли
@router.put("/api/roles/{role_id}")
async def role_update(
    role_data: RoleUpdate,
    role_id: int = Path(...),
    admin=Depends(get_current_admin),
):
    role = await Role.get(id=role_id)
    role.name = role_data.name
    role.description = role_data.description
    await role.save()
    
    # Обновляем связи с разрешениями
    permissions = await Permission.filter(id__in=role_data.permissions)
    await role.permissions.clear()
    await role.permissions.add(*permissions)
    
    return {"success": True}


# API для удаления роли
@router.delete("/api/roles/{role_id}")
async def role_delete(
    role_id: int = Path(...),
    admin=Depends(get_current_admin),
):
    role = await Role.get(id=role_id)
    await role.delete()
    return {"success": True}


# Страница списка разрешений
@router.get("/permissions")
async def permissions_list(
    request: Request,
    resources=Depends(get_resources),
    admin=Depends(get_current_admin),
    model_filter: Optional[str] = None,
):
    # Фильтрация разрешений по модели
    query = Permission.all()
    if model_filter:
        query = query.filter(model_resource=model_filter)
    
    permissions = await query
    
    # Получение уникального списка моделей для фильтра
    models = await Permission.all().distinct().values_list("model_resource", flat=True)
    
    context = {
        "request": request,
        "resources": resources,
        "permissions": permissions,
        "models": models,
        "model_filter": model_filter,
        "page_title": "Управление разрешениями",
        "page_pre_title": "Система ролей",
    }
    return templates.TemplateResponse(
        "permissions/list.html",
        context=context,
    )


# Страница создания разрешения
@router.get("/permissions/create")
async def permission_create_view(
    request: Request,
    resources=Depends(get_resources),
    admin=Depends(get_current_admin),
):
    # Получение списка ресурсов для выбора
    available_models = []
    for resource in resources:
        if resource.get("type") == "model":
            available_models.append(resource.get("model"))
    
    context = {
        "request": request,
        "resources": resources,
        "available_models": available_models,
        "actions": [e.value for e in PermissionAction],
        "page_title": "Создание разрешения",
        "page_pre_title": "Система ролей",
    }
    return templates.TemplateResponse(
        "permissions/create.html",
        context=context,
    )


# API для создания разрешения
@router.post("/api/permissions")
async def permission_create(
    permission: PermissionCreate,
    admin=Depends(get_current_admin),
):
    # Проверяем, что такого разрешения еще нет
    existing = await Permission.filter(
        model_resource=permission.model_resource,
        action=permission.action
    ).first()
    
    if existing:
        return {"success": False, "error": "Такое разрешение уже существует"}
    
    # Создаем разрешение
    return await Permission.create(
        model_resource=permission.model_resource,
        action=permission.action,
        fields=permission.fields,
        conditions=permission.conditions,
    )


# Страница редактирования разрешения
@router.get("/permissions/{permission_id}")
async def permission_edit_view(
    request: Request,
    permission_id: int = Path(...),
    resources=Depends(get_resources),
    admin=Depends(get_current_admin),
):
    permission = await Permission.get(id=permission_id)
    
    # Получение списка ресурсов для выбора
    available_models = []
    for resource in resources:
        if resource.get("type") == "model":
            available_models.append(resource.get("model"))
    
    context = {
        "request": request,
        "resources": resources,
        "permission": permission,
        "available_models": available_models,
        "actions": [e.value for e in PermissionAction],
        "page_title": f"Редактирование разрешения: {permission.model_resource}.{permission.action}",
        "page_pre_title": "Система ролей",
    }
    return templates.TemplateResponse(
        "permissions/edit.html",
        context=context,
    )


# API для обновления разрешения
@router.put("/api/permissions/{permission_id}")
async def permission_update(
    permission_data: PermissionCreate,
    permission_id: int = Path(...),
    admin=Depends(get_current_admin),
):
    # Проверяем, что такого разрешения еще нет
    existing = await Permission.filter(
        Q(model_resource=permission_data.model_resource) & 
        Q(action=permission_data.action) & 
        ~Q(id=permission_id)
    ).first()
    
    if existing:
        return {"success": False, "error": "Такое разрешение уже существует"}
    
    permission = await Permission.get(id=permission_id)
    permission.model_resource = permission_data.model_resource
    permission.action = permission_data.action
    permission.fields = permission_data.fields
    permission.conditions = permission_data.conditions
    await permission.save()
    
    return {"success": True}


# API для удаления разрешения
@router.delete("/api/permissions/{permission_id}")
async def permission_delete(
    permission_id: int = Path(...),
    admin=Depends(get_current_admin),
):
    permission = await Permission.get(id=permission_id)
    await permission.delete()
    return {"success": True} 