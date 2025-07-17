from http import HTTPStatus

from fastapi import FastAPI

app = FastAPI()


@app.get(
    '/health',
    status_code=HTTPStatus.OK,
    responses={HTTPStatus.OK: {'description': 'OK'}},
)
async def health_check():
    return 'OK'
