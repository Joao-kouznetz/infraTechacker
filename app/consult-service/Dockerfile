FROM python:3.10-slim

WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# EXPOSE 8000 # Exposto pelo compose.yaml

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]