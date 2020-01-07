from pydantic import json
from starlette.requests import Request

from fastapi_sqlalchemy import FastAPI_SQLAlchemy, crud
from models.base import db
from models.places import Country, Place, PlaceType
from models.user import UserApi

# Instantiate the application
app = FastAPI_SQLAlchemy(
    db,
    debug=True,
    title="Esteira de Tradução",
    description="API for Translation data",
    version="0.1.0"
)
app.create_all()

# # Load some data
session = app.Session()
for name in ["alice", "bob", "charlie", "david"]:
    user = UserApi.get_by_username(session, name)
    if user is None:
        user = UserApi(username=name)
        session.add(user)
session.commit()

for c in [
    {"name": "Brasil", "code": "BR"},
    {"name": "Argentina", "code": "AR"},
]:
    exists = Country.get_by_code(session, c['code'])
    if exists is None:
        session.add(Country(**c))
session.commit()


# Users
@app.get("/users")
async def list_users(request: Request):
    return await crud.list_instances(UserApi, request.state.session)


# Contries
@app.get("/countries")
async def list_countries(request: Request, code: str = None):
    country = Country.get_by_code(session, code) if code else None
    return country if code else await crud.list_instances(Country, request.state.session)
