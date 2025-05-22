from pydantic import BaseModel, Field, EmailStr
from typing import Literal, List, Optional, Annotated
from uuid import UUID, uuid4


class User(BaseModel):
    model_config = {"extra": "forbid"}  # proibe atributos extras que não tem no schema

    model_config = {  # maneira mais facil de colocar exemplo
        "json_schema_extra": {
            "unique": True,
            "examples": [
                {
                    "nome": "Joao Bresser",
                    "email": "joao.bresserpereira@gmail.com",
                    "senha": "1234d",
                }
            ],
        },
        "from_attributes": True,  # Permite a conversão de modelos ORM
    }
    id: UUID = Field(
        ...,
        default_factory=uuid4,  # ja gera automaticamento o uuid
        description="ID único referente ao usuario",
    )
    nome: str = Field(
        ...,
        description="Nome do usuário",
    )
    email: EmailStr = Field(  # faz a validação com email
        ...,
        # pattern=r"[A-Za-z0-9._%+-]+[@][A-Za-z0-9_%-]+[.]?[A-Za-z0-9_%-]+?[.]com", # isso é se eu quiser verificar o email com uma string ai teria que retirar o Emailstr e colocar str
        description="email do usuario",
    )
    senha: str = Field(..., description="Coloque a sua senha")


class UserValidate(BaseModel):
    model_config = {"extra": "forbid"}  # proibe atributos extras que não tem no schema

    model_config = {  # maneira mais facil de colocar exemplo
        "json_schema_extra": {
            "examples": [
                {
                    "nome": "Joao Bresser",
                    "email": "joao.bresserpereira@gmail.com",
                    "senha": "1234d",
                }
            ]
        },
        "from_attributes": True,  # Permite a conversão de modelos ORM
    }
    email: EmailStr = Field(  # faz a validação com email
        ...,
        # pattern=r"[A-Za-z0-9._%+-]+[@][A-Za-z0-9_%-]+[.]?[A-Za-z0-9_%-]+?[.]com", # isso é se eu quiser verificar o email com uma string ai teria que retirar o Emailstr e colocar str
        description="email do usuario",
    )
    senha: str = Field(..., description="Coloque a sua senha")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str
    exp: str
