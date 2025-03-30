from fastapi import FastAPI

from . import crypto

app = FastAPI()

app.include_router(crypto.router)
