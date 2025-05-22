from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import Session
from models import User, Base
from sqlalchemy import select
from typing import Annotated  # para ter validaçÕes
from fastapi import Depends  #
from dotenv import load_dotenv
import os


from sqlalchemy.pool import StaticPool

# https://docs.sqlalchemy.org/en/20/tutorial/engine.html
# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
# # A url indica, qual é a database que utilizaremos,
DATABASE_URL = os.getenv("DATABASE_URL") or (
    f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:"
    f"{os.getenv('MYSQL_PASSWORD')}@{os.getenv('DB_HOST','mysql')}:"
    f"{os.getenv('DB_PORT','3306')}/{os.getenv('MYSQL_DATABASE')}"
)

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
else:
    engine = create_engine(DATABASE_URL)
# criando database


# # DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@mysql:{os.getenv('DB_PORT')}/{os.getenv('MYSQL_DATABASE')}"
# engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    Base.metadata.create_all(
        engine
    )  # isso cria todas as base de dados Emitting DDL to the database from an ORM mapping¶


# Criando sessão


# Uma Session é o que armazena o objeto na memória e mantêm validando e vendo a as alterações
#  necessárias com os dados depois é utilizado a engine para comunicar com a base de dados
def get_session():
    with Session(engine) as session:
        yield session


# vai se criado uma dependencia com o fastAPI com yiel para fazer uma a sessão para cada
# requisição isso garante que so tem uma sessão por requisição
SessionDB = Annotated[Session, Depends(get_session)]
