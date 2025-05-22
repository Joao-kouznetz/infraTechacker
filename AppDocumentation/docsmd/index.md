# Porque o projeto foi desenvolvido?

Esse projeto tem como objetivo elaborar uma API RESTfull capaz de cadastrar e autenticar usuários. E dockernizar esse projeto para ser facilmente acessível.

# Tecnologias utilizadas

- FASTAPI (framework em python para desenvolvimento de APIs)
- SWAGGERUI (incluso no fastapi para desenvolvimento automático de documentação)
- PYDANTIC (método de tipagem para o python)
- JWT (método seguro para transmitir dados de maneira segura)
- SQLalchemy (ORM para conectar a base de dados)
- MYSQL (base de dados)
- Docker (método de conteinerização do aplicativo)
- MKDocs (maneira de fazer documentação utilizando markdown)

# Como rodar a aplicação?

Para rodar a aplicação em a sua máquina local é apenas necessário utilizar o comando abaixo .

``` zsh
docker compose up
```

e para descer o app fazer

``` zsh
docker compose down
```

Caso deseje criar na maquina local é necessario mudar o `compose.yaml` para que ele de build e não rode com o arquivo

1. Clonar o repositório
2. Na pasta raiz do repositório copiar o docker-composeDEVELOPMENT para o arquivo docker-compose.yml
3. Com o docker baixado rodar o seguinte comando; `docker compose up --build`
4. Com isso você vai ter criado a sua própria imagem do app, voce pode utilizar agora os comandos `docker compose up` e `docker compose down` para colocar no ar e retirar do ar sua aplicação.

# Como abrir a documentação

Esse projeto tem dois tipos de documentação, uma feita com SWAGGERUI que é a documentação das apis e uma feita com Mkdocs. Para acessar a primeira  quando o projeto estiver rodando acessar a seguite url : `http://localhost:8000/docs`

A segunda você pode acessar pelos srquivos markdown na pasta `AppDocumentation/docs` ou de maneira mais estruturada voce roda o seguinte comando no terminal dentro da aba `appDocumeentation`

```bash
mkdocs serve
```

Com isso abrira uma url em que voce pode ler a documentação de forma mais organizada

# link para imgagem no docker hub

[link para docker hub](https://hub.docker.com/repository/docker/joaokb/projeto1-app/general)

# Onde o compose.yaml esta?

O arquivo compose.yaml está na raiz do projeto.

Segue o codigo dele:

```yaml
services:
    app:
        image: joaokb/projeto1-app # Utilize a imagem publicada no Docker Hub
        ports:
            - "8000:8000"
            # Portas abertas são necessárias para acessar o serviço fora do container.
        environment:
            - SECRET_KEY=${SECRET_KEY:-2e6e8cc741f246604c750dcc672fed67c877b2fe9f77eafaa41245ce91b5a0d3}
            - sqlite_file_name=${sqlite_file_name:-database.db}
            - salt=${salt:-18274393}
            - MYSQL_USER=${MYSQL_USER:-user}
            - MYSQL_PASSWORD=${MYSQL_PASSWORD:-cloud}
            - DB_HOST=mysql
            - DB_PORT=3306
            - MYSQL_DATABASE=${MYSQL_DB:-db}
        depends_on:
            mysql:
                condition: service_healthy

    mysql:
        image: mysql:8.0
        restart: always
        environment:
            MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:-root_password}
            MYSQL_USER: ${MYSQL_USER:-user}
            MYSQL_PASSWORD: ${MYSQL_PASSWORD:-cloud}
            MYSQL_DATABASE: ${MYSQL_DB:-db}
        healthcheck:
            test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
            interval: 10s
            timeout: 5s
            retries: 10
```
