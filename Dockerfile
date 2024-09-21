FROM python:3.12

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .


CMD ["alembic", "upgrade", "head"]
CMD ["uvicorn", "main:app", "--host","0.0.0.0","--port","8000"]

