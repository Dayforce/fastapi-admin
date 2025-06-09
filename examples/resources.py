import os
from typing import List

from starlette.requests import Request

from examples import enums
from examples.constants import BASE_DIR
from examples.models import Admin, Category, Config, Product
from fastapi_admin.app import app
from fastapi_admin.enums import Method
from fastapi_admin.file_upload import FileUpload
from fastapi_admin.resources import Action, Dropdown, Field, Link, Model, ToolbarAction
from fastapi_admin.widgets import displays, filters, inputs
from fastapi_admin.models import Permission, Role

upload = FileUpload(uploads_dir=os.path.join(BASE_DIR, "static", "uploads"))


@app.register
class Dashboard(Link):
    label = "Dashboard"
    icon = "fas fa-home"
    url = "/admin"


@app.register
class AdminResource(Model):
    model = Admin
    icon = "fas fa-user"
    label = "Администраторы"
    page_pre_title = "Управление пользователями"
    page_title = "Список администраторов"
    filters = [
        "username",
    ]
    fields = [
        "id",
        "username",
        Field(
            name="password",
            label="Пароль",
            display=displays.InputOnly(),
            input_=inputs.Password(),
        ),
        Field(
            name="roles",
            label="Роли",
            display=displays.ManyToMany(
                Row="name",
            ),
            input_=inputs.ManyToMany(
                model=Role, 
                value_field="id",
                display_field="name",
            ),
        ),
        Field(
            name="created_at",
            label="Дата создания",
            display=displays.DatetimeDisplay(),
            input_=inputs.DisplayOnly(),
        ),
    ]

    async def get_toolbar_actions(self, request: Request) -> List[ToolbarAction]:
        return []

    async def cell_attributes(self, request: Request, obj: dict, field: Field) -> dict:
        if field.name == "id":
            return {"class": "bg-danger text-white"}
        return await super().cell_attributes(request, obj, field)

    async def get_actions(self, request: Request) -> List[Action]:
        return []

    async def get_bulk_actions(self, request: Request) -> List[Action]:
        return []


@app.register
class Content(Dropdown):
    class CategoryResource(Model):
        model = Category
        icon = "fas fa-list"
        label = "Категории"
        page_pre_title = "Управление категориями"
        page_title = "Список категорий"
        filters = [
            "name",
            "product_type",
        ]
        fields = [
            "id",
            "name",
            "slug",
            "product_type",
        ]

    class ProductResource(Model):
        model = Product
        icon = "fas fa-box"
        label = "Товары"
        page_pre_title = "Управление товарами"
        page_title = "Список товаров"
        filters = [
            "name",
            "category__name",
        ]
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "category",
            "image",
            "created_at",
        ]

    label = "Content"
    icon = "fas fa-bars"
    resources = [ProductResource, CategoryResource]


@app.register
class ConfigResource(Model):
    model = Config
    icon = "fas fa-cogs"
    label = "Настройки"
    page_pre_title = "Управление настройками"
    page_title = "Настройки системы"
    filters = [
        "key",
        "value",
    ]
    fields = [
        "id",
        "key",
        "value",
    ]

    async def row_attributes(self, request: Request, obj: dict) -> dict:
        if obj.get("status") == enums.Status.on:
            return {"class": "bg-green text-white"}
        return await super().row_attributes(request, obj)

    async def get_actions(self, request: Request) -> List[Action]:
        actions = await super().get_actions(request)
        switch_status = Action(
            label="Switch Status",
            icon="ti ti-toggle-left",
            name="switch_status",
            method=Method.PUT,
        )
        actions.append(switch_status)
        return actions


@app.register
class GithubLink(Link):
    label = "Github"
    url = "https://github.com/fastapi-admin/fastapi-admin"
    icon = "fab fa-github"
    target = "_blank"


@app.register
class DocumentationLink(Link):
    label = "Documentation"
    url = "https://fastapi-admin-docs.long2ice.io"
    icon = "fas fa-file-code"
    target = "_blank"


@app.register
class ProLink(Link):
    label = "Pro Version"
    url = "https://fastapi-admin-pro.long2ice.io/admin/login"
    icon = "far fa-heart"
    target = "_blank"


class RoleResource(Model):
    model = Role
    icon = "fas fa-user-tag"
    label = "Роли"
    page_pre_title = "Управление ролями"
    page_title = "Список ролей"
    filters = [
        "name",
    ]
    fields = [
        "id",
        "name",
        "description",
        Field(
            name="permissions",
            label="Разрешения",
            display=displays.ManyToMany(
                Row=lambda x: f"{x.model_resource}:{x.action}",
            ),
            input_=inputs.ManyToMany(
                model=Permission,
                value_field="id",
                display_field=lambda x: f"{x.model_resource}:{x.action}",
            ),
        ),
    ]


class PermissionResource(Model):
    model = Permission
    icon = "fas fa-shield-alt"
    label = "Разрешения"
    page_pre_title = "Управление разрешениями"
    page_title = "Список разрешений"
    filters = [
        "model_resource",
    ]
    fields = [
        "id",
        "model_resource",
        "action",
        Field(
            name="fields",
            label="Поля",
            display=displays.Json(),
            input_=inputs.Json(),
        ),
        Field(
            name="conditions",
            label="Условия",
            display=displays.Json(),
            input_=inputs.Json(),
        ),
    ]
