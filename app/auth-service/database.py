from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import Session
from models import User, Base
from sqlalchemy import select
from typing import Annotated  # para ter validaçÕes
from fastapi import Depends  #
from dotenv import load_dotenv
import os

# criando database

# https://docs.sqlalchemy.org/en/20/tutorial/engine.html
# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


# Obter o salt da variável de ambiente
DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@mysql:{os.getenv('DB_PORT')}/{os.getenv('MYSQL_DATABASE')}"
engine = create_engine(DATABASE_URL)
# A url indica, qual é a database que utilizaremos,
# echo indica para colocar todos os SQL it emits to a Python logger that will write to standard out.


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
