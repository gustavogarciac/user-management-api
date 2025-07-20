from http import HTTPStatus

from fastapi import FastAPI

from src.adapters.api.routers.auth import router as auth_router
from src.adapters.api.routers.create_user import router as create_user_router
from src.adapters.api.routers.delete_user import router as delete_user_router
from src.adapters.api.routers.get_user import router as get_user_router
from src.adapters.api.routers.list_users import router as list_users_router
from src.adapters.api.routers.update_user import router as update_user_router
from src.infrastructure.database.sqlite_db import init_db

app = FastAPI(
    title='User Management API',
    description='API for managing users',
    version='1.0.0',
    contact={
        'name': 'Gustavo Garcia',
        'email': 'gustavogarciac@gmail.com',
    },
    openapi_url='/openapi.json',
    docs_url='/docs',
)

app.include_router(create_user_router, prefix='/api/v1', tags=['users'])
app.include_router(get_user_router, prefix='/api/v1', tags=['users'])
app.include_router(delete_user_router, prefix='/api/v1', tags=['users'])
app.include_router(update_user_router, prefix='/api/v1', tags=['users'])
app.include_router(list_users_router, prefix='/api/v1', tags=['users'])
app.include_router(auth_router, prefix='/api/v1', tags=['auth'])


@app.on_event('startup')
async def startup_event():
    await init_db()


@app.get(
    '/',
    tags=['root'],
    status_code=HTTPStatus.OK,
    responses={HTTPStatus.OK: {'description': 'OK'}},
)
async def root():
    return {
        'message': 'API is running. you can use /docs',
        'status': 'ok',
    }


@app.get(
    '/health',
    tags=['health'],
    status_code=HTTPStatus.OK,
    responses={HTTPStatus.OK: {'description': 'OK'}},
)
async def health_check():
    return 'OK'
