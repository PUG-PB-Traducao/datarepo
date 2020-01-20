
from fastapi import FastAPI
from fastapi_sqlalchemy import db
from pydantic import json

from .models.base import configure_db
from .models.core import User

# Instantiate the application
app = FastAPI()

# Third party
configure_db(app)

# Users
@app.get("/users")
async def get_users():
    return json.dumps(db.session.query(User).all())
