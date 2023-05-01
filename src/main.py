from functools import lru_cache
import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from api import router as api_router
from app import router as app_router
from config import Settings

config = Settings()

app = FastAPI(title='UltiBot App', version='0.0.1')
app.mount('/static', StaticFiles(directory='static'), name='static')

origins= [
    'http://localhost:8080',
    'http://127.0.0.1:8080'
]


@lru_cache()
def get_settings():
    return Settings()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
async def event_startup():
    logging.info('Connect to OpenAI....')


@app.on_event('shutdown')
async def event_shutdown():
    logging.info('Shutdown...')


app.include_router(api_router, prefix='/api')
app.include_router(app_router)