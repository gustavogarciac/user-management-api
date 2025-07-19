from http import HTTPStatus

from fastapi import FastAPI

from src.adapters.api.routers.create_user import router as create_user_router
from src.adapters.api.routers.delete_user import router as delete_user_router
from src.adapters.api.routers.get_user import router as get_user_router
from src.adapters.api.routers.update_user import router as update_user_router
from src.infrastructure.database.sqlite_db import init_db

app = FastAPI()

app.include_router(create_user_router, prefix='/api/v1', tags=['users'])
app.include_router(get_user_router, prefix='/api/v1', tags=['users'])
app.include_router(delete_user_router, prefix='/api/v1', tags=['users'])
app.include_router(update_user_router, prefix='/api/v1', tags=['users'])


@app.on_event('startup')
async def startup_event():
    await init_db()


@app.get(
    '/health',
    status_code=HTTPStatus.OK,
    responses={HTTPStatus.OK: {'description': 'OK'}},
)
async def health_check():
    return 'OK'
