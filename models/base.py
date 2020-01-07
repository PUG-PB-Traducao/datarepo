from sqlalchemy import MetaData, create_engine

import os
from dotenv import load_dotenv
load_dotenv()

PG_SERVER = os.environ.get('PG_SERVER')
PG_USER = os.environ.get('PG_USR')
PG_PW = os.environ.get('PG_PWD')
PG_DB = os.environ.get('PG_DB')
PG_URL = f'{PG_SERVER}:5432'
DB_URL = f'postgresql+psycopg2://{PG_USER}:{PG_PW}@{PG_URL}/{PG_DB}'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_DATABASE_URI = DB_URL

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uk": "uk_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = create_engine(DB_URL)
metadata.create_all(db)
