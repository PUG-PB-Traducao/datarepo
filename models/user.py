from fastapi_sqlalchemy.models import User


# Define our model
class UserApi(User):
    __abstract__ = False
