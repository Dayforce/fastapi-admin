# FastAPI Admin

[![image](https://img.shields.io/pypi/v/fastapi-admin.svg?style=flat)](https://pypi.python.org/pypi/fastapi-admin)
[![image](https://img.shields.io/github/license/fastapi-admin/fastapi-admin)](https://github.com/fastapi-admin/fastapi-admin)
[![image](https://github.com/fastapi-admin/fastapi-admin/workflows/deploy/badge.svg)](https://github.com/fastapi-admin/fastapi-admin/actions?query=workflow:deploy)
[![image](https://github.com/fastapi-admin/fastapi-admin/workflows/pypi/badge.svg)](https://github.com/fastapi-admin/fastapi-admin/actions?query=workflow:pypi)

[中文文档](./README-zh.md)
[한국어 문서](./README-ko.md)
[日本語ドキュメント](./README-ja.md)

## Introduction

`fastapi-admin` is a fast admin dashboard based on [FastAPI](https://github.com/tiangolo/fastapi)
and [TortoiseORM](https://github.com/tortoise/tortoise-orm/) with [tabler](https://github.com/tabler/tabler) ui,
inspired by Django admin.

This fork adds a code-based role management system that allows developers to define and control access permissions directly in code rather than through database models.

## Features

- Standard FastAPI-Admin features
- Extended role-based access control:
  - Define roles and permissions directly in code
  - Control access at model, action, and field levels
  - No database configuration for permissions needed
  - Better security and version control for roles
  - Multiple predefined role types and creation helpers

## Installation

```shell
> pip install fastapi-admin
```

## Requirements

- [Redis](https://redis.io)

## Online Demo

You can check a online demo [here](https://fastapi-admin.long2ice.io/admin/login).

- username: `admin`
- password: `123456`

Or pro version online demo [here](https://fastapi-admin-pro.long2ice.io/admin/login).

- username: `admin`
- password: `123456`

## Role-Based Access Control

This fork implements a code-based permission system that allows defining roles and permissions in code:

```python
# Define a role with specific permissions
EDITOR_ROLE = Role(
    name="editor",
    permissions=[
        Permission(model_name="category", action=PermissionAction.READ),
        Permission(model_name="category", action=PermissionAction.CREATE),
        Permission(model_name="category", action=PermissionAction.UPDATE),
        Permission(model_name="product", action=PermissionAction.READ),
    ]
)

# Register the role
register_role(EDITOR_ROLE)

# Use helper functions to create common roles
CATALOG_VIEWER = create_viewer_role(["category", "product"])
```

To use the role-based system:

1. Define roles in your application
2. Register the `CodePermissionProvider` in your app
3. Assign roles to administrators through the `role_names` field

See `examples/code_based_auth.py` for a complete example.

## Screenshots

![](https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/login.png)

![](https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/dashboard.png)

## Run examples in local

1. Clone repo.
2. Create `.env` file.

   ```dotenv
   DATABASE_URL=mysql://root:123456@127.0.0.1:3306/fastapi-admin
   REDIS_URL=redis://localhost:6379/0
   ```

3. Run `docker-compose up -d --build`.
4. Visit <http://localhost:8000/admin/init> to create first admin.

## Documentation

See documentation at <https://fastapi-admin-docs.long2ice.io>.

## License

This project is licensed under the
[Apache-2.0](https://github.com/fastapi-admin/fastapi-admin/blob/master/LICENSE)
License.

## Credits

[![image](./images/yxvm.png)](https://yxvm.com/)

[NodeSupport](https://github.com/NodeSeekDev/NodeSupport) supports this project.
