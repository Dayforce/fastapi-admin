import os

from fastapi_admin.permissions import ROLES
from fastapi_admin.resources import Field, Model
from fastapi_admin.widgets import displays, inputs

from examples.models import Admin, Category, Config, Product


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
            name="role_names",
            label="Роли",
            display=displays.Display(),
            input_=inputs.Select(
                choices=[(name, name) for name in ROLES.keys()]
            ),
        ),
        Field(
            name="created_at",
            label="Дата создания",
            display=displays.DatetimeDisplay(),
            input_=inputs.DisplayOnly(),
        ),
    ]


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