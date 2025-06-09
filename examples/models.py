from datetime import datetime

from tortoise import fields

from fastapi_admin.models import AbstractAdmin, Role


class Admin(AbstractAdmin):
    created_at = fields.DatetimeField(default=datetime.now)

    class Meta:
        table = "admin"
        ordering = ["-created_at"]


class Category(fields.Model):
    name = fields.CharField(max_length=50)
    slug = fields.CharField(max_length=100, unique=True)
    product_type = fields.CharField(max_length=20)
    created_at = fields.DatetimeField(default=datetime.now)

    class Meta:
        table = "category"


class Product(fields.Model):
    name = fields.CharField(max_length=100)
    slug = fields.CharField(max_length=200, unique=True)
    description = fields.TextField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    category = fields.ForeignKeyField("models.Category", related_name="products")
    image = fields.CharField(max_length=200, null=True)
    created_at = fields.DatetimeField(default=datetime.now)

    class Meta:
        table = "product"


class Config(fields.Model):
    key = fields.CharField(max_length=100, unique=True)
    value = fields.JSONField()

    class Meta:
        table = "config"
