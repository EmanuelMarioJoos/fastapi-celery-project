from fastapi import FastAPI
import uvicorn
import os
from settings import settings
from celery import current_app as current_celery_app

from app.api import api


def create_celery():
    celery_app = current_celery_app
    celery_app.config_from_object(settings, namespace="CELERY")

    return celery_app


app = FastAPI()

celery = create_celery()
app.celery_app = celery

app.include_router(api.api_router)


@app.on_event("startup")
def migrate_database():
    os.popen("alembic upgrade head").read()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001, host="0.0.0.0")
