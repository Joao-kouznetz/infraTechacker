import os
import pytest

import os

# 1) OVERRIDE ANTES DE QUALQUER IMPORTAÇÃO
os.environ["MYSQL_USER"] = "test_user"
os.environ["MYSQL_PASSWORD"] = "test_pass"
os.environ["MYSQL_DATABASE"] = "test_db"  # <- nome que seu código espera
os.environ["SECRET_KEY"] = "testsecret"
os.environ["SALT"] = "testsalt"
os.environ["DB_PORT"] = "3307"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"  # ou

from fastapi.testclient import TestClient
from main import app  # ajuste o import conforme o seu projeto

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    """
    Cria as tabelas antes de cada sessão de testes e limpa depois.
    """
    from database import create_db_and_tables, engine, Base

    # cria
    create_db_and_tables()
    yield
    # limpa
    Base.metadata.drop_all(engine)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Hello World"}


def test_register_and_login_and_me():
    # 1) Registrar
    user = {"nome": "João Teste", "email": "teste@example.com", "senha": "abc123"}
    r = client.post("/usuarios/registrar/", json=user)
    assert r.status_code == 200
    data = r.json()
    assert "access_token" in data and data["token_type"] == "bearer"

    token = data["access_token"]

    # 2) Login
    creds = {"email": user["email"], "senha": user["senha"]}
    r2 = client.post("/usuarios/login", json=creds)
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["token_type"] == "bearer"
    assert data2["access_token"] != ""

    # 3) /auth/me
    headers = {"Authorization": f"Bearer {data2['access_token']}"}
    r3 = client.get("/usuarios/auth/me", headers=headers)
    assert r3.status_code == 200
    me = r3.json()
    assert me["email"] == user["email"]
    assert "nome" in me


def test_register_duplicate_email():
    user = {"nome": "Dup", "email": "dup@example.com", "senha": "pw"}
    client.post("/usuarios/registrar/", json=user)
    r = client.post("/usuarios/registrar/", json=user)
    assert r.status_code == 409
    assert r.json()["detail"] == "Email já cadastrado."


def test_login_wrong_password():
    user = {"nome": "Foo", "email": "foo@example.com", "senha": "rightpw"}
    client.post("/usuarios/registrar/", json=user)
    bad = {"email": user["email"], "senha": "wrongpw"}
    r = client.post("/usuarios/login", json=bad)
    assert r.status_code == 401
    assert "senha incorreta" in r.json()["detail"]
