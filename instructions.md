TITLE: Configuring FastAPI-Admin App (Python)
DESCRIPTION: Shows how to configure the FastAPI-Admin application during the FastAPI startup event. It sets up a username/password login provider, connects to Redis, and configures visual elements like logos and template folders.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/getting_started/quickstart.md#_snippet_1

LANGUAGE: Python
CODE:
```
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from examples.models import Admin
import aioredis
from fastapi import FastAPI

login_provider = UsernamePasswordProvider(
    admin_model=Admin,
    enable_captcha=True,
    login_logo_url="https://preview.tabler.io/static/logo.svg"
)

app = FastAPI()


@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool("redis://localhost", encoding="utf8")
    admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=[os.path.join(BASE_DIR, "templates")],
        providers=[login_provider],
        redis=redis,
    )
```

----------------------------------------

TITLE: Configure fastapi-admin on FastAPI startup
DESCRIPTION: This snippet demonstrates how to initialize the fastapi-admin application (`admin_app`) within the `startup` event handler of a FastAPI application. It shows how to create a Redis connection pool and pass it, along with other configuration options like logo URL, template folders, and login providers, to the `admin_app.configure()` method. This ensures the admin application is set up asynchronously when the FastAPI app starts.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/reference/index.md#_snippet_0

LANGUAGE: python
CODE:
```
import aioredis
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from examples.models import Admin

app = FastAPI()


@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool(address='redis://localhost')
    await admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=["templates"],
        providers=[
            UsernamePasswordProvider(
                login_logo_url="https://preview.tabler.io/static/logo.svg", admin_model=Admin
            )
        ],
        redis=redis,
    )
```

----------------------------------------

TITLE: Defining Model Resource for Admin (Python)
DESCRIPTION: Shows how to define a `Model` resource for a database model (e.g., `Admin`). It automatically generates CRUD pages and allows customization of fields, filters, displays, and inputs, including file uploads.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/getting_started/quickstart.md#_snippet_3

LANGUAGE: Python
CODE:
```
from examples.models import Admin
from fastapi_admin.app import app
from fastapi_admin.file_upload import FileUpload
from fastapi_admin.resources import Field, Model
from fastapi_admin.widgets import displays, filters, inputs

upload = FileUpload(uploads_dir=os.path.join(BASE_DIR, "static", "uploads"))


@app.register
class AdminResource(Model):
    label = "Admin"
    model = Admin
    icon = "fas fa-user"
    page_pre_title = "admin list"
    page_title = "admin model"
    filters = [
        filters.Search(
            name="username", label="Name", search_mode="contains", placeholder="Search for username"
        ),
        filters.Date(name="created_at", label="CreatedAt"),
    ]
    fields = [
        "id",
        "username",
        Field(
            name="password",
            label="Password",
            display=displays.InputOnly(),
            input_=inputs.Password(),
        ),
        Field(name="email", label="Email", input_=inputs.Email()),
        Field(
            name="avatar",
            label="Avatar",
            display=displays.Image(width="40"),
            input_=inputs.Image(null=True, upload=upload),
        ),
        "created_at",
    ]
```

----------------------------------------

TITLE: Configuring fastapi-admin on FastAPI Startup (Python)
DESCRIPTION: This snippet demonstrates how to configure the fastapi-admin application within a FastAPI startup event handler. It initializes a Redis connection using aioredis and calls `admin_app.configure` with parameters like logo URL, template folders, authentication providers (UsernamePasswordProvider), and the Redis instance. This configuration must happen within an asyncio loop context, typically during application startup. Requires fastapi, fastapi-admin, and aioredis.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/reference/index.md#_snippet_0

LANGUAGE: Python
CODE:
```
import aioredis
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from examples.models import Admin

app = FastAPI()


@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool(address='redis://localhost')
    await admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=["templates"],
        providers=[
            UsernamePasswordProvider(
                login_logo_url="https://preview.tabler.io/static/logo.svg", admin_model=Admin
            )
        ],
        redis=redis,
    )
```

----------------------------------------

TITLE: Registering a Model Resource (Python)
DESCRIPTION: Demonstrates registering a Model resource using @app.register. It shows configuring the resource with a menu label, the associated TortoiseORM model, page titles, and defining filters using built-in filter types like Search and Date.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/reference/resource.md#_snippet_6

LANGUAGE: python
CODE:
```
@app.register
class AdminResource(Model):
    label = "Admin"
    model = Admin
    page_pre_title = "admin list"
    page_title = "Admin Model"
    filters = [
        filters.Search(
            name="username",
            label="Name",
            search_mode="contains",
            placeholder="Search for username",
        ),
        filters.Date(name="created_at", label="CreatedAt"),
    ]

```

----------------------------------------

TITLE: Defining Model Fields with Field Objects (Python)
DESCRIPTION: Shows how to define fields for a Model resource, including using the Field object for custom display and input widgets like Password, Email, and Image. It also mentions using simple strings for auto-mapping based on field type.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/reference/resource.md#_snippet_1

LANGUAGE: python
CODE:
```
@app.register
class AdminResource(Model):
    fields = [
        "id",
        "username",
        Field(
            name="password",
            label="Password",
            display=displays.InputOnly(),
            input_=inputs.Password(),
        ),
        Field(name="email", label="Email", input_=inputs.Email()),
        Field(
            name="avatar",
            label="Avatar",
            display=displays.Image(width="40"),
            input_=inputs.Image(null=True, upload=upload),
        ),
        "created_at",
    ]
```

----------------------------------------

TITLE: Defining Fields for a Model Resource in FastAPI-Admin (Python)
DESCRIPTION: This example illustrates how to define the `fields` list for a `Model` resource. It shows how to include simple string field names for auto-mapping and how to use the `Field` class for custom display and input widgets, such as `displays.InputOnly` for password and `inputs.Image` for avatar.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/reference/resource.md#_snippet_1

LANGUAGE: python
CODE:
```
@app.register
class AdminResource(Model):
    fields = [
        "id",
        "username",
        Field(
            name="password",
            label="Password",
            display=displays.InputOnly(),
            input_=inputs.Password(),
        ),
        Field(name="email", label="Email", input_=inputs.Email()),
        Field(
            name="avatar",
            label="Avatar",
            display=displays.Image(width="40"),
            input_=inputs.Image(null=True, upload=upload),
        ),
        "created_at",
    ]
```

----------------------------------------

TITLE: Mounting FastAPI-Admin App (Python)
DESCRIPTION: Demonstrates how to mount the FastAPI-Admin application instance (`admin_app`) as a sub-application at the "/admin" path within a standard FastAPI application instance (`app`). This makes the admin interface accessible at `/admin`.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/getting_started/quickstart.md#_snippet_0

LANGUAGE: Python
CODE:
```
from fastapi_admin.app import app as admin_app
from fastapi import FastAPI

app = FastAPI()
app.mount("/admin", admin_app)
```

----------------------------------------

TITLE: Configuring Username/Password Login with FastAPI-Admin
DESCRIPTION: Demonstrates how to enable the built-in `UsernamePasswordProvider` for login in fastapi-admin. This requires adding the provider instance to the `providers` list during the `admin_app.configure` call, specifying the admin model.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/reference/login.md#_snippet_0

LANGUAGE: python
CODE:
```
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from examples.models import Admin

app = FastAPI()


@app.on_event("startup")
async def startup():
    await admin_app.configure(
        providers=[
            LoginProvider(
                login_logo_url="https://preview.tabler.io/static/logo.svg",
                admin_model=Admin,
            )
        ]
    )
```

----------------------------------------

TITLE: Configuring a Model Resource with Basic Options and Filters in FastAPI-Admin (Python)
DESCRIPTION: This example shows how to configure a `Model` resource with essential properties like the menu `label`, the underlying TortoiseORM `model`, page titles, and `filters`. It includes an example of defining search and date filters for the resource's table view.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/reference/resource.md#_snippet_6

LANGUAGE: python
CODE:
```
@app.register
class AdminResource(Model):
    label = "Admin"
    model = Admin
    page_pre_title = "admin list"
    page_title = "Admin Model"
    filters = [
        filters.Search(
            name="username",
            label="Name",
            search_mode="contains",
            placeholder="Search for username",
        ),
        filters.Date(name="created_at", label="CreatedAt"),
    ]

```

----------------------------------------

TITLE: Configuring Username/Password Login with FastAPI-Admin (Python)
DESCRIPTION: Demonstrates how to add the UsernamePasswordProvider to the fastapi-admin configuration during application startup. This enables login using a username and password against the specified admin_model.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/reference/login.md#_snippet_0

LANGUAGE: python
CODE:
```
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from examples.models import Admin

app = FastAPI()


@app.on_event("startup")
async def startup():
    await admin_app.configure(
        providers=[
            LoginProvider(
                login_logo_url="https://preview.tabler.io/static/logo.svg",
                admin_model=Admin,
            )
        ]
    )
```

----------------------------------------

TITLE: Configuring PermissionProvider in FastAPI App
DESCRIPTION: Configures the FastAPI application to use the PermissionProvider from fastapi_admin.providers.permission during the application startup event, integrating the defined Admin, Resource, and Permission models for permission management.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/reference/permission.md#_snippet_2

LANGUAGE: python
CODE:
```
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.permission import PermissionProvider

app = FastAPI()


@app.on_event("startup")
async def startup():
    await admin_app.configure(
        providers=[
            PermissionProvider(
                Admin,
                Resource,
                Permission,
            ),
        ]
    )
```

----------------------------------------

TITLE: Configure PermissionProvider
DESCRIPTION: Shows how to integrate the permission system into your FastAPI application by configuring the `fastapi_admin` app during startup. This involves adding the `PermissionProvider` and associating it with your custom `Admin`, `Resource`, and `Permission` models to enable permission checks.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/reference/permission.md#_snippet_2

LANGUAGE: python
CODE:
```
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.permission import PermissionProvider

app = FastAPI()


@app.on_event("startup")
async def startup():
    await admin_app.configure(
        providers=[
            PermissionProvider(
                Admin,
                Resource,
                Permission,
            ),
        ]
    )
```

----------------------------------------

TITLE: Configuring FileUpload and Using in Model Field - Python
DESCRIPTION: This snippet demonstrates how to initialize the basic FileUpload class by specifying the directory where files should be stored. It then shows how to integrate this configured upload instance into a model field definition, specifically using it with an inputs.Image input widget for an 'avatar' field.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/reference/file_upload.md#_snippet_0

LANGUAGE: python
CODE:
```
upload = FileUpload(uploads_dir=os.path.join(BASE_DIR, "static", "uploads"))

@app.register
class AdminResource(Model):
    fields = [
        Field(
            name="avatar",
            label="Avatar",
            display=displays.Image(width="40"),
            input_=inputs.Image(null=True, upload=upload),
        ),
    ]
```

----------------------------------------

TITLE: Create Custom Page Router with Authentication (Python)
DESCRIPTION: Defines a FastAPI router endpoint ('/') within the admin application that renders a specific template ('dashboard.html'). It uses the 'get_current_admin' dependency to ensure the user is logged in before accessing the page.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/custom/page.md#_snippet_1

LANGUAGE: python
CODE:
```
from fastapi_admin.app import app as admin_app
from fastapi_admin.template import templates
from starlette.requests import Request
from fastapi import Depends
from fastapi_admin.depends import get_current_admin


@admin_app.get("/", dependencies=[Depends(get_current_admin)])
async def home(request: Request):
    return templates.TemplateResponse("dashboard.html", context={"request": request})
```

----------------------------------------

TITLE: Custom ComputeField Implementation (Python)
DESCRIPTION: Provides an example of implementing a custom ComputeField called RestDays. It overrides the get_value method to calculate the remaining days based on a date field value.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/reference/resource.md#_snippet_4

LANGUAGE: python
CODE:
```
class RestDays(ComputeField):
    async def get_value(self, request: Request, obj: dict):
        days = (obj.get(self.name) - date.today()).days
        return days if days >= 0 else 0
```

----------------------------------------

TITLE: Configuring FileUpload and Using in Model Field - Python
DESCRIPTION: This snippet demonstrates how to initialize the FileUpload class with a specified upload directory and then integrate it into a model definition for an image field, using it as the input handler.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/reference/file_upload.md#_snippet_0

LANGUAGE: python
CODE:
```
upload = FileUpload(uploads_dir=os.path.join(BASE_DIR, "static", "uploads"))

@app.register
class AdminResource(Model):
    fields = [
        Field(
            name="avatar",
            label="Avatar",
            display=displays.Image(width="40"),
            input_=inputs.Image(null=True, upload=upload),
        ),
    ]
```

----------------------------------------

TITLE: Configuring OAuth2 Login with FastAPI-Admin (Python)
DESCRIPTION: Shows how to configure fastapi-admin to support OAuth2 login via providers like GitHub and Google by adding them to the providers list during startup. Requires client ID, client secret, and potentially a redirect URI.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/reference/login.md#_snippet_1

LANGUAGE: python
CODE:
```
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from examples.providers import GitHubProvider, GoogleProvider, LoginProvider
from examples.models import Admin

app = FastAPI()


@app.on_event("startup")
async def startup():
    await admin_app.configure(
        providers=[
            GitHubProvider(Admin, settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET),
            GoogleProvider(
                Admin,
                settings.GOOGLE_CLIENT_ID,
                settings.GOOGLE_CLIENT_SECRET,
                redirect_uri="https://fastapi-admin-pro.long2ice.io/admin/oauth2/google_oauth2_provider",
            ),
        ]
    )
```

----------------------------------------

TITLE: Creating a Custom Router for a FastAPI-Admin Page
DESCRIPTION: This code defines a FastAPI router within the `fastapi-admin` app to render a custom HTML template (`dashboard.html`). It includes the `get_current_admin` dependency to ensure the page is only accessible to logged-in administrators, protecting the custom route.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/custom/page.md#_snippet_1

LANGUAGE: python
CODE:
```
from fastapi_admin.app import app as admin_app
from fastapi_admin.template import templates
from starlette.requests import Request
from fastapi import Depends
from fastapi_admin.depends import get_current_admin


@admin_app.get("/", dependencies=[Depends(get_current_admin)])
async def home(request: Request):
    return templates.TemplateResponse("dashboard.html", context={"request": request})
```

----------------------------------------

TITLE: Configuring OAuth2 Login with FastAPI-Admin
DESCRIPTION: Shows how to configure OAuth2 providers like GitHub and Google for admin login. This involves adding instances of `GitHubProvider` and `GoogleProvider` (or similar custom providers) to the `providers` list during `admin_app.configure`, providing the admin model and client credentials.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/reference/login.md#_snippet_1

LANGUAGE: python
CODE:
```
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from examples.providers import GitHubProvider, GoogleProvider, LoginProvider
from examples.models import Admin

app = FastAPI()


@app.on_event("startup")
async def startup():
    await admin_app.configure(
        providers=[
            GitHubProvider(Admin, settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET),
            GoogleProvider(
                Admin,
                settings.GOOGLE_CLIENT_ID,
                settings.GOOGLE_CLIENT_SECRET,
                redirect_uri="https://fastapi-admin-pro.long2ice.io/admin/oauth2/google_oauth2_provider",
            ),
        ]
    )
```

----------------------------------------

TITLE: Configure OAuth2 Providers in FastAPI Admin
DESCRIPTION: Integrate OAuth2 authentication providers like GitHub and Google by adding their respective providers during the admin application configuration, including necessary client IDs, secrets, and redirect URIs.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/pro/exclusive.md#_snippet_8

LANGUAGE: python
CODE:
```
await admin_app.configure(
    providers=[
        GitHubProvider(Admin, settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET),
        GoogleProvider(
            Admin,
            settings.GOOGLE_CLIENT_ID,
            settings.GOOGLE_CLIENT_SECRET,
            redirect_uri="https://fastapi-admin-pro.long2ice.io/admin/oauth2/google_oauth2_provider",
        ),
    ]
)
```

----------------------------------------

TITLE: Installing fastapi-admin Pro Version (Shell)
DESCRIPTION: This command installs the fastapi-admin pro version directly from its Git repository using pip, requiring a GitHub token for authentication.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/pro/upgrade.md#_snippet_1

LANGUAGE: shell
CODE:
```
pip install git+https://${GH_TOKEN}@github.com/fastapi-admin/fastapi-admin-pro.git
```

----------------------------------------

TITLE: Adding Computed Fields in FastAPI Admin
DESCRIPTION: Shows how to define and add computed fields to a resource in the FastAPI admin interface. Computed fields are derived from other data and displayed alongside regular fields.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/reference/resource.md#_snippet_10

LANGUAGE: python
CODE:
```
@app.register
class SponsorResource(Model):
    async def get_compute_fields(self, request: Request) -> List[ComputeField]:
        return [RestDays(name="invalid_date", label="Days Remaining")]
```

----------------------------------------

TITLE: Hiding Default Actions and Bulk Actions in FastAPI-Admin (Python)
DESCRIPTION: This snippet shows how to customize the actions available for a `Model` resource by overriding the `get_actions` and `get_bulk_actions` methods. Returning an empty list from these methods removes the default edit, delete, and bulk delete actions from the resource's table view.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/reference/resource.md#_snippet_4

LANGUAGE: python
CODE:
```
@app.register
class AdminResource(Model):
    async def get_actions(self, request: Request) -> List[Action]:
        return []

    async def get_bulk_actions(self, request: Request) -> List[Action]:
        return []
```

----------------------------------------

TITLE: Install fastapi-admin-pro with pip
DESCRIPTION: Installs the fastapi-admin-pro package directly from the Git repository using pip. This method requires a GitHub personal access token (GH_TOKEN) to authenticate access to the repository.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/pro/installation.md#_snippet_0

LANGUAGE: shell
CODE:
```
> pip install git+https://${GH_TOKEN}@github.com/fastapi-admin/fastapi-admin-pro.git
```

----------------------------------------

TITLE: Adding Exception Handlers for HTTP Errors in FastAPI Admin
DESCRIPTION: This snippet shows how to register specific exception handler functions for 403 (Forbidden), 404 (Not Found), and 500 (Internal Server Error) HTTP status codes in a FastAPI Admin application instance. It utilizes pre-defined handler functions from `fastapi_admin.exceptions` and status codes from `starlette.status`.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/reference/errors.md#_snippet_0

LANGUAGE: python
CODE:
```
from fastapi_admin.exceptions import forbidden_error_exception, not_found_error_exception, server_error_exception
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

admin_app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
admin_app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
admin_app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
```

----------------------------------------

TITLE: Registering Error Handlers for FastAPI Admin (Python)
DESCRIPTION: This snippet demonstrates how to register built-in exception handlers provided by fastapi-admin for common HTTP status codes (403 Forbidden, 404 Not Found, 500 Internal Server Error). It requires importing the specific exception handler functions and the HTTP status codes from starlette.status. The add_exception_handler method of the admin application instance is used to map each status code to its corresponding handler function.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/reference/errors.md#_snippet_0

LANGUAGE: python
CODE:
```
from fastapi_admin.exceptions import forbidden_error_exception, not_found_error_exception, server_error_exception
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

admin_app.add_exception_handler(HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception)
admin_app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
admin_app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
```

----------------------------------------

TITLE: Overriding Model Actions (Python)
DESCRIPTION: Illustrates how to override the default row and bulk actions for a Model resource by implementing get_actions and get_bulk_actions methods. Returning an empty list effectively hides all default actions.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/reference/resource.md#_snippet_2

LANGUAGE: python
CODE:
```
@app.register
class AdminResource(Model):
    async def get_actions(self, request: Request) -> List[Action]:
        return []

    async def get_bulk_actions(self, request: Request) -> List[Action]:
        return []
```

----------------------------------------

TITLE: Defining the Base ComputeField Class in FastAPI-Admin (Python)
DESCRIPTION: This snippet provides the definition for the base `ComputeField` class, which is a subclass of `Field`. It is designed for creating virtual fields whose values are computed dynamically, requiring the user to override the `get_value` method.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/reference/resource.md#_snippet_2

LANGUAGE: python
CODE:
```
class ComputeField(Field):
    async def get_value(self, request: Request, obj: dict):
        return obj.get(self.name)
```

----------------------------------------

TITLE: Define Custom Permission Models
DESCRIPTION: Illustrates how to create custom database models for `Resource`, `Permission`, and `Role` by inheriting from the abstract base classes provided by `fastapi_admin.models`. These models are essential for storing and managing permission data in your application's database.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/reference/permission.md#_snippet_1

LANGUAGE: python
CODE:
```
from fastapi_admin.models import (
    AbstractPermission,
    AbstractResource,
    AbstractRole,
)


class Resource(AbstractResource):
    pass


class Permission(AbstractPermission):
    pass


class Role(AbstractRole):
    pass
```

----------------------------------------

TITLE: Defining Permission Models in Python
DESCRIPTION: Defines the necessary database models (Resource, Permission, Role) by inheriting from abstract base classes provided by fastapi_admin.models to support the permission control feature.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/reference/permission.md#_snippet_1

LANGUAGE: python
CODE:
```
from fastapi_admin.models import (
    AbstractPermission,
    AbstractResource,
    AbstractRole,
)


class Resource(AbstractResource):
    pass


class Permission(AbstractPermission):
    pass


class Role(AbstractRole):
    pass
```

----------------------------------------

TITLE: Configuring Global Search with SearchProvider (Python)
DESCRIPTION: This snippet demonstrates how to add the SearchProvider to the fastapi-admin application configuration within the startup event handler. This action enables the global search feature for the admin interface.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/reference/global_search.md#_snippet_0

LANGUAGE: python
CODE:
```
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.search import SearchProvider

app = FastAPI()


@app.on_event("startup")
async def startup():
    await admin_app.configure(
        providers=[SearchProvider()]
    )
```

----------------------------------------

TITLE: Implementing a Custom ComputeField (RestDays) in FastAPI-Admin (Python)
DESCRIPTION: This example demonstrates how to create a custom `ComputeField` subclass, `RestDays`, by overriding the `get_value` method. It calculates the number of days remaining based on a date field in the object, returning 0 if the date is in the past.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/reference/resource.md#_snippet_3

LANGUAGE: python
CODE:
```
class RestDays(ComputeField):
    async def get_value(self, request: Request, obj: dict):
        days = (obj.get(self.name) - date.today()).days
        return days if days >= 0 else 0
```

----------------------------------------

TITLE: Defining Search Filter in Python
DESCRIPTION: Configures a search filter for a model field. Allows specifying the field name, label, search mode (e.g., 'contains'), and placeholder text. The search_mode parameter supports various string matching options.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/reference/widget/filter.md#_snippet_0

LANGUAGE: python
CODE:
```
@app.register
class AdminResource(Model):
    filters = [
        filters.Search(
            name="username",
            label="Name",
            search_mode="contains",
            placeholder="Search for username",
        ),
    ]
```

----------------------------------------

TITLE: Add fastapi-admin-pro to requirements.txt
DESCRIPTION: Adds the fastapi-admin-pro package to a requirements.txt file, specifying the Git repository URL. When installing dependencies from this file using pip, the GH_TOKEN environment variable will be used for authentication.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/pro/installation.md#_snippet_2

LANGUAGE: shell
CODE:
```
-e https://${GH_TOKEN}@github.com/fastapi-admin/fastapi-admin-pro.git#egg=fastapi-admin-pro
```

----------------------------------------

TITLE: Defining Permission Enum in Python
DESCRIPTION: Defines an enumeration for the available permission types (create, delete, update, read) used within the FastAPI Admin permission control system.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/reference/permission.md#_snippet_0

LANGUAGE: python
CODE:
```
class Permission(str, Enum):
    create = "create"
    delete = "delete"
    update = "update"
    read = "read"
```

----------------------------------------

TITLE: Defining Base Widget Class in Python
DESCRIPTION: Explains the base Widget class, its purpose as a parent for display, input, and filter widgets, its use of Jinja2Templates, and the render method for rendering values using a template. Mentions the context parameter in __init__.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/custom/widget.md#_snippet_0

LANGUAGE: python
CODE:
```
class Widget:
    templates: Jinja2Templates = t
    template: str = ""

    def __init__(self, **context):
        """
        All context will pass to template render if template is not empty.
        :param context:
        """
        self.context = context

    async def render(self, request: Request, value: Any):
        if value is None:
            value = ""
        if not self.template:
            return value
        return self.templates.get_template(self.template).render(value=value, **self.context)
```

----------------------------------------

TITLE: Define Permission Enum
DESCRIPTION: Defines a Python Enum `Permission` listing the standard permission types available in FastAPI Admin: create, delete, update, and read. This enum provides a structured way to reference permission levels within the application.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/reference/permission.md#_snippet_0

LANGUAGE: python
CODE:
```
class Permission(str, Enum):
    create = "create"
    delete = "delete"
    update = "update"
    read = "read"
```

----------------------------------------

TITLE: Configure FastAPI-Admin Template Folders (Python)
DESCRIPTION: Configures the FastAPI-Admin application to use a specific directory ('templates') for loading HTML templates. This setup is typically performed during the application startup event.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/custom/page.md#_snippet_0

LANGUAGE: python
CODE:
```
from fastapi import FastAPI
from fastapi_admin.app import app as admin_app

app = FastAPI()


@app.on_event("startup")
async def startup():
    await admin_app.configure(template_folders=["templates"])
```

----------------------------------------

TITLE: Customizing Datetime Display Widget in Python
DESCRIPTION: Shows how to create a custom display widget for datetime and date objects by inheriting Display and overriding render. Explains how it formats the date/time using pendulum and calls the parent render method. Mentions the format_ parameter.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/custom/widget.md#_snippet_1

LANGUAGE: python
CODE:
```
class DatetimeDisplay(Display):
    def __init__(self, format_: str = constants.DATETIME_FORMAT):
        super().__init__()
        self.format_ = format_

    async def render(self, request: Request, value: datetime):
        if isinstance(value, datetime):
            return await super(DatetimeDisplay, self).render(
                request, pendulum.instance(value).format(self.format_) if value else None
            )
        elif isinstance(value, date):
            return await super(DatetimeDisplay, self).render(
                request,
                pendulum.date(value.year, value.month, value.day).format(self.format_)
                if value
                else None,
            )
```

----------------------------------------

TITLE: Defining Dropdown Resource with Nested Models (Python)
DESCRIPTION: Demonstrates how to create a `Dropdown` resource to group other resources (like `Model` or `Link`) in the sidebar. This example groups `CategoryResource` and `ProductResource` under a "Content" dropdown menu.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/getting_started/quickstart.md#_snippet_4

LANGUAGE: Python
CODE:
```
from examples import enums
from examples.models import Category, Product
from fastapi_admin.app import app
from fastapi_admin.resources import Dropdown, Field, Model
from fastapi_admin.widgets import displays, filters


@app.register
class Content(Dropdown):
    class CategoryResource(Model):
        label = "Category"
        model = Category
        fields = ["id", "name", "slug", "created_at"]

    class ProductResource(Model):
        label = "Product"
        model = Product
        filters = [
            filters.Enum(enum=enums.ProductType, name="type", label="ProductType"),
            filters.Datetime(name="created_at", label="CreatedAt"),
        ]
        fields = [
            "id",
            "name",
            "view_num",
            "sort",
            "is_reviewed",
            "type",
            Field(name="image", label="Image", display=displays.Image(width="40")),
            "body",
            "created_at",
        ]

    label = "Content"
    icon = "fas fa-bars"
    resources = [ProductResource, CategoryResource]
```

----------------------------------------

TITLE: Creating a Dropdown Menu Resource in FastAPI Admin
DESCRIPTION: Defines a dropdown resource that groups other resources (like Model or Link resources) under a common label and icon in the FastAPI admin sidebar, allowing for nested navigation.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/reference/resource.md#_snippet_12

LANGUAGE: python
CODE:
```
@app.register
class Content(Dropdown):
    label = "Content"
    icon = "fas fa-bars"
    resources = [ProductResource, CategoryResource]
```

----------------------------------------

TITLE: Creating Text Input Widget in Python
DESCRIPTION: Demonstrates creating a text input widget by inheriting Input. Explains the use of input_type and the parameters handled in the __init__ method (help_text, default, null, placeholder, disabled).
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/custom/widget.md#_snippet_2

LANGUAGE: python
CODE:
```
class Text(Input):
    input_type: Optional[str] = "text"

    def __init__(
            self,
            help_text: Optional[str] = None,
            default: Any = None,
            null: bool = False,
            placeholder: str = "",
            disabled: bool = False,
    ):
        super().__init__(
            null=null,
            default=default,
            input_type=self.input_type,
            placeholder=placeholder,
            disabled=disabled,
            help_text=help_text,
        )
```

----------------------------------------

TITLE: Customizing Input Widget for Text (Python)
DESCRIPTION: This snippet demonstrates creating a custom input widget specifically for text input by inheriting from the `Input` class. It defines the default `input_type` as 'text' and customizes the `__init__` method to accept parameters like `help_text`, `default`, `null`, `placeholder`, and `disabled`, passing them to the superclass constructor.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/custom/widget.md#_snippet_2

LANGUAGE: python
CODE:
```
class Text(Input):
    input_type: Optional[str] = "text"

    def __init__(
            self,
            help_text: Optional[str] = None,
            default: Any = None,
            null: bool = False,
            placeholder: str = "",
            disabled: bool = False,
    ):
        super().__init__(
            null=null,
            default=default,
            input_type=self.input_type,
            placeholder=placeholder,
            disabled=disabled,
            help_text=help_text,
        )
```

----------------------------------------

TITLE: Define Datetime Filter in FastAPI Admin
DESCRIPTION: This snippet demonstrates how to apply a Datetime filter to a field ('created_at') in a FastAPI Admin resource. This filter type is used for filtering based on datetime values.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/reference/widget/filter.md#_snippet_1

LANGUAGE: python
CODE:
```
@app.register
class AdminResource(Model):
    filters = [
        filters.Datetime(name="created_at", label="CreatedAt"),
    ]
```

----------------------------------------

TITLE: Defining File Upload Base Class - Python
DESCRIPTION: This Python class `FileUpload` serves as a base for handling file uploads in FastAPI-Admin. It provides methods for initializing upload parameters, saving files asynchronously, and the main upload logic which includes file size and extension validation. Custom backends should inherit this class and override the `upload` method.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/custom/file_upload.md#_snippet_0

LANGUAGE: python
CODE:
```
class FileUpload:
    def __init__(
            self,
            uploads_dir: str,
            allow_extensions: Optional[List[str]] = None,
            max_size: int = 1024 ** 3,
            filename_generator: Optional[Callable] = None,
            prefix: str = "/static/uploads",
    ):
        self.max_size = max_size
        self.allow_extensions = allow_extensions
        self.uploads_dir = uploads_dir
        self.filename_generator = filename_generator
        self.prefix = prefix

    async def save_file(self, filename: str, content: bytes):
        file = os.path.join(self.uploads_dir, filename)
        async with aiofiles.open(file, "wb") as f:
            await f.write(content)
        return os.path.join(self.prefix, filename)

    async def upload(self, file: UploadFile):
        if self.filename_generator:
            filename = self.filename_generator(file)
        else:
            filename = file.filename
        content = await file.read()
        file_size = len(content)
        if file_size > self.max_size:
            raise FileMaxSizeLimit(f"File size {file_size} exceeds max size {self.max_size}")
        if self.allow_extensions:
            for ext in self.allow_extensions:
                if filename.endswith(ext):
                    raise FileExtNotAllowed(
                        f"File ext {ext} is not allowed of {self.allow_extensions}"
                    )
        return await self.save_file(filename, content)
```

----------------------------------------

TITLE: Defining FileUpload Class for Custom Uploads in Python
DESCRIPTION: This Python class provides a base structure for implementing custom file upload backends. It includes methods for initializing with upload directory, allowed extensions, max size, and prefix, saving files asynchronously, and handling the upload process with size and extension validation.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/zh/docs/custom/file_upload.md#_snippet_0

LANGUAGE: Python
CODE:
```
class FileUpload:
    def __init__(
            self,
            uploads_dir: str,
            allow_extensions: Optional[List[str]] = None,
            max_size: int = 1024 ** 3,
            filename_generator: Optional[Callable] = None,
            prefix: str = "/static/uploads",
    ):
        self.max_size = max_size
        self.allow_extensions = allow_extensions
        self.uploads_dir = uploads_dir
        self.filename_generator = filename_generator
        self.prefix = prefix

    async def save_file(self, filename: str, content: bytes):
        file = os.path.join(self.uploads_dir, filename)
        async with aiofiles.open(file, "wb") as f:
            await f.write(content)
        return os.path.join(self.prefix, filename)

    async def upload(self, file: UploadFile):
        if self.filename_generator:
            filename = self.filename_generator(file)
        else:
            filename = file.filename
        content = await file.read()
        file_size = len(content)
        if file_size > self.max_size:
            raise FileMaxSizeLimit(f"File size {file_size} exceeds max size {self.max_size}")
        if self.allow_extensions:
            for ext in self.allow_extensions:
                if filename.endswith(ext):
                    raise FileExtNotAllowed(
                        f"File ext {ext} is not allowed of {self.allow_extensions}"
                    )
        return await self.save_file(filename, content)
```

----------------------------------------

TITLE: Define Enum Filter in FastAPI Admin
DESCRIPTION: This snippet shows how to use an Enum filter in a FastAPI Admin resource. It allows filtering a field ('type') based on choices provided by an Enum class ('enums.ProductType').
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/reference/widget/filter.md#_snippet_3

LANGUAGE: python
CODE:
```
class ProductResource(Model):
    filters = [
        filters.Enum(enum=enums.ProductType, name="type", label="ProductType"),
    ]
```

----------------------------------------

TITLE: Defining the Base Action Model (Python)
DESCRIPTION: Defines the base Pydantic model for actions in FastAPI-Admin, specifying common attributes like icon, label, name, method, and ajax. Includes a validator to ensure `ajax` is only False when the method is GET.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/custom/action.md#_snippet_0

LANGUAGE: python
CODE:
```
class Action(BaseModel):
    icon: str
    label: str
    name: str
    method: enums.Method = enums.Method.POST
    ajax: bool = True

    @validator("ajax")
    def ajax_validate(cls, v: bool, values: dict, **kwargs):
        if not v and values["method"] != enums.Method.GET:
            raise ValueError("ajax is False only available when method is Method.GET")

```

----------------------------------------

TITLE: Define Date Filter in FastAPI Admin
DESCRIPTION: This snippet illustrates how to add a Date filter to a field ('created_at') in a FastAPI Admin resource. This filter is specifically designed for filtering based on date values.
SOURCE: https://github.com/fastapi-admin/fastapi-admin.github.io/blob/main/docs/en/docs/reference/widget/filter.md#_snippet_2

LANGUAGE: python
CODE:
```
@app.register
class AdminResource(Model):
    filters = [
        filters.Date(name="created_at", label="CreatedAt"),
    ]
```

----------------------------------------

TITLE: Defining Code-Based Permission System (Python)
DESCRIPTION: Shows how to implement a code-based permission system in FastAPI Admin using enums, classes for permissions and roles, and utility functions. This approach allows defining and managing roles directly in code rather than in the database.
SOURCE: https://github.com/fastapi-admin/fastapi-admin-forked/blob/main/fastapi_admin/permissions.py

LANGUAGE: Python
CODE:
```
from enum import Enum
from typing import Dict, List, Optional, Set, Type, Union

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
```

----------------------------------------

TITLE: Using Predefined Roles and Role Utilities (Python)
DESCRIPTION: Demonstrates using predefined roles and utility functions for creating and registering custom roles. It includes examples of creating admin roles with full access, creating editor roles with specific model access, and registering custom roles.
SOURCE: https://github.com/fastapi-admin/fastapi-admin-forked/blob/main/fastapi_admin/permissions.py

LANGUAGE: Python
CODE:
```
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

# Словарь доступных ролей
ROLES = {
    "admin": ADMIN_ROLE,
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

# Пример создания и регистрации пользовательской роли
CATALOG_EDITOR = create_editor_role(["category", "product"])
register_role(CATALOG_EDITOR)
```

----------------------------------------

TITLE: Implementing Code-Based Roles in Admin Model (Python)
DESCRIPTION: Shows how to modify the AbstractAdmin model to store role names in a JSON field instead of using database relationships. This implementation uses property methods to provide a cleaner interface for accessing roles.
SOURCE: https://github.com/fastapi-admin/fastapi-admin-forked/blob/main/fastapi_admin/models.py

LANGUAGE: Python
CODE:
```
from tortoise import Model, fields
from typing import List, Optional


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
```

----------------------------------------

TITLE: Creating Code Permission Provider (Python)
DESCRIPTION: Demonstrates implementing a permission provider that works with code-defined roles instead of database-stored ones. This provider integrates with the FastAPI Admin routing system and enforces access controls for models, actions, and fields.
SOURCE: https://github.com/fastapi-admin/fastapi-admin-forked/blob/main/fastapi_admin/providers/code_permissions.py

LANGUAGE: Python
CODE:
```
import typing
from typing import Dict, List, Optional, Set, Type, Union

from fastapi import Depends, HTTPException
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN

from fastapi_admin.depends import get_current_admin
from fastapi_admin.permissions import PermissionAction, get_role_by_name, has_permission
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
```

----------------------------------------

TITLE: Configuring App with Code-Based Permission Provider (Python)
DESCRIPTION: Shows how to configure a FastAPI application to use the code-based permission system. It demonstrates defining custom roles, registering them, and setting up the application with the CodePermissionProvider during startup.
SOURCE: https://github.com/fastapi-admin/fastapi-admin-forked/blob/main/examples/code_based_auth.py

LANGUAGE: Python
CODE:
```
import os
import sys

import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from fastapi_admin.app import app as admin_app
from fastapi_admin.permissions import (
    Permission, PermissionAction, Role, register_role, 
    create_editor_role, create_viewer_role
)
from fastapi_admin.providers.code_permissions import CodePermissionProvider
from fastapi_admin.providers.login import UsernamePasswordProvider

from examples.models import Admin, Category, Config, Product


# Определяем пользовательские роли
CATALOG_EDITOR = create_editor_role(["category", "product"])
CATALOG_VIEWER = create_viewer_role(["category", "product"])

# Роль для работы только с настройками
CONFIG_MANAGER = Role(
    name="config_manager",
    permissions=[
        Permission(model_name="config", action=PermissionAction.CREATE),
        Permission(model_name="config", action=PermissionAction.READ),
        Permission(model_name="config", action=PermissionAction.UPDATE),
        Permission(model_name="config", action=PermissionAction.DELETE),
    ]
)

# Регистрируем пользовательские роли
register_role(CATALOG_EDITOR)
register_role(CATALOG_VIEWER)
register_role(CONFIG_MANAGER)

# Создаем основное приложение FastAPI
app = FastAPI()

@app.on_event("startup")
async def startup():
    r = redis.Redis.from_url(
        "redis://localhost:6379/0", encoding="utf8", decode_responses=True
    )
    
    # Настраиваем FastAPI Admin
    await admin_app.configure(
        redis=r,
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        admin_path="/admin",
        template_folders=["examples/templates"],
        providers=[
            UsernamePasswordProvider(
                admin_model=Admin,
                login_logo_url="https://preview.tabler.io/static/logo.svg",
            ),
            # Регистрируем провайдер разрешений на основе кода
            CodePermissionProvider(),
        ],
    )
    
    # Создаем тестовых администраторов с разными ролями, если их нет
    admin_count = await Admin.all().count()
    if admin_count == 0:
        # Администратор с полными правами
        await Admin.create(
            username="admin",
            password="admin",
            role_names=["admin"]  # Роль определена в fastapi_admin.permissions 
        )
        
        # Редактор каталога
        await Admin.create(
            username="editor",
            password="editor",
            role_names=["editor_category+product"]  # Роль создана через create_editor_role
        )
        
        # Просмотрщик каталога
        await Admin.create(
            username="viewer",
            password="viewer",
            role_names=["viewer_category+product"]  # Роль создана через create_viewer_role
        )
        
        # Менеджер настроек
        await Admin.create(
            username="config",
            password="config",
            role_names=["config_manager"]  # Пользовательская роль
        )
```

----------------------------------------

TITLE: Creating Administrators with Code-Based Roles (Python)
DESCRIPTION: Shows how to create administrator users with code-defined roles during application startup. This approach allows setting up default admin accounts with different permission levels when initializing the application.
SOURCE: https://github.com/fastapi-admin/fastapi-admin-forked/blob/main/examples/code_based_auth.py

LANGUAGE: Python
CODE:
```
@app.on_event("startup")
async def startup():
    # ... previous configuration code ...
    
    # Создаем тестовых администраторов с разными ролями, если их нет
    admin_count = await Admin.all().count()
    if admin_count == 0:
        # Администратор с полными правами
        await Admin.create(
            username="admin",
            password="admin",
            role_names=["admin"]  # Роль определена в fastapi_admin.permissions 
        )
        
        # Редактор каталога
        await Admin.create(
            username="editor",
            password="editor",
            role_names=["editor_category+product"]  # Роль создана через create_editor_role
        )
        
        # Просмотрщик каталога
        await Admin.create(
            username="viewer",
            password="viewer",
            role_names=["viewer_category+product"]  # Роль создана через create_viewer_role
        )
        
        # Менеджер настроек
        await Admin.create(
            username="config",
            password="config",
            role_names=["config_manager"]  # Пользовательская роль
        )
```

----------------------------------------

TITLE: Creating Admin Resource with Code-based Roles (Python)
DESCRIPTION: Shows how to create an Admin resource that works with code-defined roles using role_names field. This implementation uses a Select input widget to choose from available roles defined in the ROLES dictionary.
SOURCE: https://github.com/fastapi-admin/fastapi-admin-forked/blob/main/examples/resources_code.py

LANGUAGE: Python
CODE:
```
from fastapi_admin.permissions import ROLES
from fastapi_admin.resources import Field, Model
from fastapi_admin.widgets import displays, inputs

from examples.models import Admin


class AdminResource(Model):
    model = Admin
    icon = "fas fa-user"
    label = "Administrators"
    page_pre_title = "Manage users"
    page_title = "Administrator list"
    filters = [
        "username",
    ]
    fields = [
        "id",
        "username",
        Field(
            name="password",
            label="Password",
            display=displays.InputOnly(),
            input_=inputs.Password(),
        ),
        Field(
            name="role_names",
            label="Roles",
            display=displays.Display(),
            input_=inputs.Select(
                choices=[(name, name) for name in ROLES.keys()]
            ),
        ),
        Field(
            name="created_at",
            label="Created at",
            display=displays.DatetimeDisplay(),
            input_=inputs.DisplayOnly(),
        ),
    ]