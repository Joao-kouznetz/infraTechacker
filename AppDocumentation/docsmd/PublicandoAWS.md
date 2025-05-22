# Publicando na AWS

## Pré requisitos

- ter uma conta aws com condiçoes de adiministrador
- Já ter imagens no docker-hub que rodam em arquitetura x86_64 caso não acesse [esse link](https://docs.docker.com/build/building/multi-platform/) e faca a sua imagem docker rodar com a arquitetura
- Conta ter acesso Ao cloudShell

# Instruções

1. Acesse o cloud shell e instale o eksctl para fazer isso é apenas rodar o comando abaixo: (pode rever no seguinte [link](https://eksctl.io/installation/):)

```zsh
# for ARM systems, set ARCH to: `arm64`, `armv6` or `armv7`
ARCH=amd64
PLATFORM=$(uname -s)_$ARCH

curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.tar.gz"

# (Optional) Verify checksum
curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check

tar -xzf eksctl_$PLATFORM.tar.gz -C /tmp && rm eksctl_$PLATFORM.tar.gz

sudo mv /tmp/eksctl /usr/local/bin
```

2. Criar os clusters em são paulo:

```zsh
eksctl create cluster --name projcomp --region sa-east-1 --nodes 2
```

3. Configurando

```zsh
aws eks --region sa-east-1 update-kubeconfig --name projcomp
```

4. Criando arquivo para dar deploy da minha aplicaçao `deployment.yaml`
Segue o arquivo com variaveis de enviroment como exemplos:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
        - name: fastapi
          image: joaokb/projeto1-app:latest
          ports:
            - containerPort: 8000
          env:
            - name: SECRET_KEY
              value: "asdfj423419823he912b3912983h0982nr98n2948b928n492j903"
            - name: sqlite
              value: "dataaabase.db"
            - name: salt
              value: "salzinhotopppp"
            - name: MYSQL_USER
              value: "usuario"
            - name: MYSQL_PASSWORD
              value: "cloud"
            - name: DB_HOST
              value: "mysql"
            - name: DB_PORT
              value: "3306"
            - name: MYSQL_DATABASE

apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 8000
  selector:
    app: fastapi
```

1. Criando arquivo do deploy da database: `db-deployment.yaml`

variaveis de enveroment como exemplo:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql-db-cloud
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
        - name: mysql
          image: mysql:8.0
          ports:
            - containerPort: 3306
          env:
            - name: MYSQL_ROOT_PASSWORD
              value: "root_password"
            - name: MYSQL_USER
              value: "user"
            - name: MYSQL_PASSWORD
              value: "cloud"
            - name: MYSQL_DATABASE
              value: "db"
---
apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  ports:
```

6. Aplicando os arquivos criados: (rode no CloudShell)

```zsh
kubectl apply -f deployment.yaml
```

7. Acesse a aplicação (aqui tem o link para ver onde ta publicado)

```zsh
kubectl get svc fastapi-service
```

8. Como debugar caso de problema:

## `kubectl get pods`

Esse comando é usado para listar todos os **pods** no cluster Kubernetes. Um **pod** é a menor unidade de implantação no Kubernetes e pode conter um ou mais containers.

### Exemplo de uso

```bash
kubectl get pods
```

### Exemplo de saída

```
NAME                                READY   STATUS    RESTARTS   AGE
fastapi-app-64757d454d-c7s72         1/1     Running   0          3d
```

---

## `kubectl get deployments`

O comando `kubectl get deployments` exibe uma lista dos "deployments" no cluster Kubernetes. Um "deployment" é uma configuração que especifica como o Kubernetes deve manter o número desejado de réplicas de um pod em execução. O comando é útil para visualizar o estado atual de cada deployment, como quantas réplicas estão sendo executadas, e se há algum erro nos pods.

### Exemplo de uso

```bash
kubectl get deployments
```

### Exemplo de saída

```
NAME              DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
fastapi-app       1         1         1            1           3d
```

---

## `kubectl logs <pod-name>`

O comando `kubectl logs <pod-name>` exibe os logs de contêineres específicos dentro de um pod. Isso é útil para depuração e monitoramento, permitindo que você visualize a saída de processos dentro do contêiner. Caso o pod tenha múltiplos contêineres, você pode especificar qual contêiner visualizar.

### Exemplo de uso

```bash
kubectl logs fastapi-app-64757d454d-c7s72
```

### Exemplo de saída

```
INFO: FastAPI app started on http://0.0.0.0:8000
INFO: Uvicorn worker is ready to serve requests
```

---
