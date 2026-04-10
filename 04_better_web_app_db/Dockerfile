FROM python:3 AS dev

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

FROM dev AS prod

COPY . .

ENTRYPOINT [ "fastapi", "run", "main.py" ]
