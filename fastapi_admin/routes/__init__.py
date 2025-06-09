from fastapi import APIRouter, Depends

from fastapi_admin.depends import get_current_admin

from .resources import router as resources_router
from .roles import router as roles_router

router = APIRouter()
router.include_router(resources_router, dependencies=[Depends(get_current_admin)])
router.include_router(roles_router, dependencies=[Depends(get_current_admin)])
