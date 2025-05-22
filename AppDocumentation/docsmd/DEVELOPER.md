
# Como é a estrutura de código

Fui inspirado pela  estrutura que esta sendo recomendada no seguinte github:
[best practicies in fast-api](https://github.com/zhanymkanov/fastapi-best-practices#1-project-structure-consistent--predictable)

A estrutura que eu fiz á  a seguinte:

```zsh
├── app/
│   ├── auth-service/
│   │   ├── database.py    # db connection related stuf 
│   │   ├── Dockerfile      # dockerfile utilizado para criar a imagme  
│   │   ├── main.py   
│   │   ├── models.py      # global database models   
│   │   ├── requirements.py    # extensões do python  
│   │   ├── router.py  # router das apis  
│   │   └── schemas.py    # pydantic models   
│   └── consult-service/
│       ├── Dockerfile      # dockerfile utilizado para criar a imagme  
│       ├── main.py   
│       ├── requirements.py    # extensões do python  
│       ├── schemas.py    # pydantic models   
│       └── security.py    # pydantic models   
├── AppDocumentation/  
│   ├── amkdocs.yml #configuração da documentação
│   └── docs/
│       ├──index.MD 
│       ├── ... 
│       └── DEVELOPER.MD  
│   └── site/ # site gerado mkdocs 
│       ├──index.html 
│       ├── ... 
│       └── 404.html
├── requirements .txt  
├── .env  
├── .gitignore  
└── docker-compose.yml # conteiner docker utilizado para testes
```

No fim do documento tem a estrutura recomendada:

# Autenticação

A autenticação foi feita utilizando JWT nela voce cria um token de acesso passando a informação que você quer encode com uma SECRET key um algoritmo de criptografia e coloca uma data de expiração para revogar a autenticação.Quando fizer uma requsição para esse endpoint ele vai devolver o token JWT que tera a autenticação.

Para acessar os dados que foram criptografados é necesário do Token criado, para isso vai verfificar se o Usuario tem um token valido e vera se esse token ja foi expirado. Caso não for nenhum desses dois casos vai prosseguir com o intuito da requisição.

[link para documentação de jwt](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#about-jwt)

[Como fiz o bearer do jwt](https://testdriven.io/blog/fastapi-jwt-auth/)

[link documentação do jwt](https://pyjwt.readthedocs.io/en/stable/api.html?highlight=decode#jwt.decode)

# Estrutura recomendada no fast-api best practices

In this structure, Each package has its own router, schemas, models, etc.

```
fastapi-project  
├── alembic/  
├── src  
│   ├── auth  
│   │   ├── router.py         # auth main router with all the endpoints  
│   │   ├── schemas.py        # pydantic models  
│   │   ├── models.py         # database models  
│   │   ├── dependencies.py   # router dependencies  
│   │   ├── config.py         # local configs  
│   │   ├── constants.py      # module-specific constants  
│   │   ├── exceptions.py     # module-specific errors  
│   │   ├── service.py        # module-specific business logic  
│   │   └── utils.py          # any other non-business logic functions  
│   ├── aws  
│   │   ├── client.py  # client model for external service communication  
│   │   ├── schemas.py  
│   │   ├── config.py  
│   │   ├── constants.py  
│   │   ├── exceptions.py  
│   │   └── utils.py  
│   └── posts  
│   │   ├── router.py  
│   │   ├── schemas.py  
│   │   ├── models.py  
│   │   ├── dependencies.py  
│   │   ├── constants.py  
│   │   ├── exceptions.py  
│   │   ├── service.py  
│   │   └── utils.py  
│   ├── config.py      # global configs  
│   ├── models.py      # global database models  
│   ├── exceptions.py  # global exceptions  
│   ├── pagination.py  # global module e.g. pagination  
│   ├── database.py    # db connection related stuff  
│   └── main.py  
├── tests/  
│   ├── auth  
│   ├── aws  
│   └── posts  
├── templates/  
│   └── index.html  
├── requirements  
│   ├── base.txt  
│   ├── dev.txt  
│   └── prod.txt  
├── .env  
├── .gitignore  
├── logging.ini  
└── alembic.ini
```

## **In this structure**

Store all domain directories inside `src` folder.

1. `src/`: The highest level of an app, contains common models, configs, and constants, etc.
2. `src/main.py`: Root of the project, which inits the FastAPI app

Each package has its own router, schemas, models, etc.

1. `router.py`: is the core of each module with all the endpoints
2. `schemas.py`: for pydantic models
3. `models.py`: for database models
4. `service.py`: module-specific business logic
5. `dependencies.py`: router dependencies
6. `constants.py`: module-specific constants and error codes
7. `config.py`: e.g. env vars
8. `utils.py`: non-business logic functions, e.g. response normalization, data enrichment, etc.
9. `exceptions.py`: module-specific exceptions, e.g. `PostNotFound`, `InvalidUserData`

## Referencia

[referencia](https://medium.com/@amirm.lavasani/how-to-structure-your-fastapi-projects-0219a6600a8f)

Referencia do mkdocs [mkdocs.org](https://www.mkdocs.org).

## Schemas

- A "schema" is a definition or description of something. Not the code that implements it, but just an abstract description.

No caso estamos utilizando schema para modelar como seria os parâmetros que são necessários para passar para cada o modelo da base de dados

# Documentação de Deploy com MkDocs

Essa documentação explica os comandos necessários para construir e publicar a documentação do projeto usando MkDocs.

## 1. Construção da Documentação

Para gerar a documentação localmente, use o comando:

```bash
mkdocs build
```

## Publicando no git hub -pages

```zsh
mkdocs gh-deploy --remote-branch Docs
```

O que este comando faz?

- gh-deploy: Faz o deploy da documentação no GitHub Pages.
- --remote-branch Docs: Especifica que a documentação será enviada para a branch Docs do repositório remoto.

Isso faz com que a versão mais recente da documentação gerada seja publicada na branch Docs, tornando-a acessível online.
