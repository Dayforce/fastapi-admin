from typing import Any, Dict, List, Optional, Tuple, Type, Union

from pydantic import BaseModel, validator
from starlette.datastructures import FormData
from starlette.requests import Request
from tortoise import ForeignKeyFieldInstance, ManyToManyFieldInstance
from tortoise import Model as TortoiseModel
from tortoise.fields import BooleanField, DateField, DatetimeField, JSONField
from tortoise.fields.data import CharEnumFieldInstance, IntEnumFieldInstance, IntField, TextField
from tortoise.queryset import QuerySet

from fastapi_admin.enums import Method
from fastapi_admin.exceptions import NoSuchFieldFound
from fastapi_admin.i18n import _
from fastapi_admin.models import PermissionAction
from fastapi_admin.widgets import Widget, displays, inputs
from fastapi_admin.widgets.filters import Filter, Search


class Resource:
    """
    Base Resource
    """

    label: str
    icon: str = ""


class Link(Resource):
    url: str
    target: str = "_self"


class Field:
    name: str
    label: str
    display: displays.Display
    input: inputs.Input

    def __init__(
        self,
        name: str,
        label: Optional[str] = None,
        display: Optional[displays.Display] = None,
        input_: Optional[Widget] = None,
    ):
        self.name = name
        self.label = label or name.title()
        if not display:
            display = displays.Display()
        display.context.update(label=self.label)
        self.display = display
        if not input_:
            input_ = inputs.Input()
        input_.context.update(label=self.label, name=name)
        self.input = input_


class ComputeField(Field):
    async def get_value(self, request: Request, obj: dict):
        return obj.get(self.name)


class Action(BaseModel):
    icon: str
    label: str
    name: str
    method: Method = Method.POST
    ajax: bool = True

    @validator("ajax")
    def ajax_validate(cls, v: bool, values: dict, **kwargs):
        if not v and values["method"] != Method.GET:
            raise ValueError("ajax is False only available when method is Method.GET")


class ToolbarAction(Action):
    class_: Optional[str]


class Model(Resource):
    model: Type[TortoiseModel]
    fields: List[Union[str, Field, ComputeField]] = []
    page_size: int = 10
    page_pre_title: Optional[str] = None
    page_title: Optional[str] = None
    filters: List[Union[str, Filter]] = []

    async def get_toolbar_actions(self, request: Request) -> List[ToolbarAction]:
        # Проверяем права на создание
        if not await self._has_action_permission(request, PermissionAction.CREATE):
            return []
        
        return [
            ToolbarAction(
                label=_("create"),
                icon="fas fa-plus",
                name="create",
                method=Method.GET,
                ajax=False,
                class_="btn-dark",
            )
        ]

    async def row_attributes(self, request: Request, obj: dict) -> dict:
        return {}

    async def column_attributes(self, request: Request, field: Field) -> dict:
        return {}

    async def cell_attributes(self, request: Request, obj: dict, field: Field) -> dict:
        return {}

    async def _has_action_permission(self, request: Request, action: PermissionAction) -> bool:
        """Проверка прав на действие с учетом провайдера разрешений"""
        admin = request.state.admin
        provider = getattr(request.state, "permission_provider", None)
        if not provider or not admin:
            return True  # Если провайдер не зарегистрирован, считаем что доступ разрешен
        
        model_name = self.model.__name__.lower()
        return await provider.has_permission(admin, model_name, action)

    async def get_actions(self, request: Request) -> List[Action]:
        actions = []
        
        # Проверяем права на обновление
        if await self._has_action_permission(request, PermissionAction.UPDATE):
            actions.append(Action(
                label=_("update"), icon="ti ti-edit", name="update", method=Method.GET, ajax=False
            ))
        
        # Проверяем права на удаление
        if await self._has_action_permission(request, PermissionAction.DELETE):
            actions.append(Action(
                label=_("delete"), icon="ti ti-trash", name="delete", method=Method.DELETE
            ))
        
        return actions

    async def get_bulk_actions(self, request: Request) -> List[Action]:
        # Проверяем права на удаление
        if not await self._has_action_permission(request, PermissionAction.DELETE):
            return []
            
        return [
            Action(
                label=_("delete_selected"),
                icon="ti ti-trash",
                name="delete",
                method=Method.DELETE,
            ),
        ]

    @classmethod
    async def get_inputs(cls, request: Request, obj: Optional[TortoiseModel] = None):
        # Фильтруем поля по правам доступа
        fields = await cls._filter_fields_by_permission(request, PermissionAction.UPDATE if obj else PermissionAction.CREATE)
        
        ret = []
        for field in fields:
            input_ = field.input
            name = input_.context.get("name")
            if isinstance(input_, inputs.DisplayOnly):
                continue
            if isinstance(input_, inputs.File):
                cls.enctype = "multipart/form-data"
            if (
                isinstance(input_, inputs.ForeignKey)
                and (obj is not None)
                and name in obj._meta.fk_fields
            ):
                await obj.fetch_related(name)
                # Value must be the string representation of the fk obj
                value = str(getattr(obj, name, None))
                ret.append(await input_.render(request, value))
                continue
            ret.append(await input_.render(request, getattr(obj, name, None)))
        return ret

    @classmethod
    async def resolve_query_params(cls, request: Request, values: dict, qs: QuerySet):
        ret = {}
        for f in cls.filters:
            if isinstance(f, str):
                f = Search(name=f, label=f.title())
            name = f.context.get("name")
            v = values.get(name)
            if v is not None and v != "":
                ret[name] = await f.parse_value(request, v)
                qs = await f.get_queryset(request, v, qs)
        return ret, qs

    @classmethod
    async def resolve_data(cls, request: Request, data: FormData):
        ret = {}
        m2m_ret = {}
        
        # Фильтруем поля по правам доступа
        fields = await cls._filter_fields_by_permission(
            request, 
            PermissionAction.CREATE if not data.get("id") else PermissionAction.UPDATE
        )
        
        field_names = [field.name for field in fields]
        
        for field in fields:
            input_ = field.input
            if input_.context.get("disabled") or isinstance(input_, inputs.DisplayOnly):
                continue
            name = input_.context.get("name")
            if isinstance(input_, inputs.ForeignKey):
                v = data.getlist(name)[0]
                ret[name] = int(v) if v else None
                continue
            if isinstance(input_, inputs.ManyToMany):
                v = data.getlist(name)
                value = await input_.parse_value(request, v)
                m2m_ret[name] = await input_.model.filter(pk__in=value)
            else:
                v = data.get(name)
                value = await input_.parse_value(request, v)
                if value is None:
                    continue
                ret[name] = value
        return ret, m2m_ret

    @classmethod
    async def get_filters(cls, request: Request, values: Optional[dict] = None):
        if not values:
            values = {}
        ret = []
        for f in cls.filters:
            if isinstance(f, str):
                f = Search(name=f, label=f.title())
            name = f.context.get("name")
            value = values.get(name)
            ret.append(await f.render(request, value))
        return ret

    @classmethod
    def _get_fields_attr(cls, attr: str, display: bool = True):
        ret = []
        for field in cls.get_fields(is_display=display):
            ret.append(getattr(field, attr))
        return ret

    @classmethod
    def get_fields_name(cls, display: bool = True):
        return cls._get_fields_attr("name", display=display)

    @classmethod
    def _get_display_input_field(cls, field_name: str) -> Field:
        field_model_map = {}
        field_name_origin = field_name
        try:
            field_model = cls.model._meta.fields_map[field_name]
            field_model_map[field_name] = field_model
        except KeyError:
            if "." in field_name:
                field_model = cls.model
                field_schema = []
                for field_ in field_name.split("."):
                    try:
                        field_model = field_model._meta.fields_map[field_]
                        field_schema.append(field_model)
                    except (KeyError, AttributeError):
                        break
                field_model_map[field_name] = field_schema[-1]
        try:
            field_model = field_model_map[field_name]
        except KeyError:
            raise NoSuchFieldFound(field_name)
        display = None
        input_ = None
        if isinstance(field_model, (DatetimeField, DateField)):
            display = displays.DatetimeDisplay()
            input_ = inputs.DatetimeInput()
        elif isinstance(field_model, IntEnumFieldInstance):
            mapping = {}
            for e in field_model.enum_type:
                mapping[e.value] = e.name
            display = displays.EnumDisplay(enum=field_model.enum_type, options=mapping)
            input_ = inputs.Enum(enum=field_model.enum_type)
        elif isinstance(field_model, CharEnumFieldInstance):
            mapping = {}
            for e in field_model.enum_type:
                mapping[e.value] = e.name
            display = displays.EnumDisplay(enum=field_model.enum_type, options=mapping)
            input_ = inputs.Enum(enum=field_model.enum_type)
        elif isinstance(field_model, ForeignKeyFieldInstance):
            remote_model = field_model.related_model
            display = displays.Display()
            input_ = inputs.ForeignKey(model=remote_model)
        elif isinstance(field_model, ManyToManyFieldInstance):
            remote_model = field_model.related_model
            display = displays.Display()
            input_ = inputs.ManyToMany(model=remote_model)
        elif isinstance(field_model, BooleanField):
            display = displays.BooleanDisplay()
            input_ = inputs.Input(input_type="checkbox")
        elif isinstance(field_model, TextField):
            display = displays.Display()
            input_ = inputs.TextArea()
        elif isinstance(field_model, JSONField):
            display = displays.Json()
            input_ = inputs.Json()
            else:
            input_type = "text"
            if isinstance(field_model, IntField):
                input_type = "number"
            input_ = inputs.Input(input_type=input_type)
        return Field(name=field_name_origin, display=display, input_=input_)

    @classmethod
    async def _filter_fields_by_permission(cls, request: Request, action: PermissionAction) -> List[Field]:
        """Фильтрует поля в соответствии с правами доступа"""
        fields = cls.get_fields(is_display=action == PermissionAction.READ)
        
        provider = getattr(request.state, "permission_provider", None)
        admin = getattr(request.state, "admin", None)
        
        # Если нет провайдера или пользователя, возвращаем все поля
        if not provider or not admin:
            return fields
            
        model_name = cls.model.__name__.lower()
        return await provider.filter_fields(admin, model_name, action, fields)

    @classmethod
    def get_fields(cls, is_display: bool = True):
        ret = []
        for field in cls.fields:
            if isinstance(field, str):
                field = cls._get_display_input_field(field)
            if isinstance(field, Field):
                if is_display:
                    field.input = inputs.DisplayOnly()
            ret.append(field)
        return ret

    @classmethod
    def get_fields_label(cls, display: bool = True):
        return cls._get_fields_attr("label", display=display)

    @classmethod
    def get_m2m_field(cls):
        ret = {}
        for field_name in cls.model._meta.m2m_fields:
            field_model = cls.model._meta.fields_map[field_name]
            ret[field_name] = field_model
        return ret

    @classmethod
    def get_fk_field(cls):
        ret = {}
        for field_name in cls.model._meta.fk_fields:
            field_model = cls.model._meta.fields_map[field_name]
            ret[field_name] = field_model
        return ret


class Dropdown(Resource):
    resources: List[Type[Resource]]


async def render_values(
    request: Request,
    model: "Model",
    fields: List["Field"],
    values: List[Dict[str, Any]],
    display: bool = True,
) -> Tuple[List[List[Any]], List[dict], List[dict], List[List[dict]]]:
    """
    render values with template render
    :params model:
    :params request:
    :params fields:
    :params values:
    :params display:
    :params request:
    :params model:
    :return:
    """
    ret = []
    cell_attributes: List[List[dict]] = []
    row_attributes: List[dict] = []
    column_attributes: List[dict] = []
    for field in fields:
        column_attributes.append(await model.column_attributes(request, field))
    for value in values:
        row_attributes.append(await model.row_attributes(request, value))
        item = []
        cell_item = []
        for field in fields:
            if isinstance(field, ComputeField):
                v = await field.get_value(request, value)
            else:
                v = value.get(field.name)
            cell_item.append(await model.cell_attributes(request, value, field))
            if display:
                item.append(await field.display.render(request, v))
            else:
                item.append(await field.input.render(request, v))
        ret.append(item)
        cell_attributes.append(cell_item)
    return ret, row_attributes, column_attributes, cell_attributes
