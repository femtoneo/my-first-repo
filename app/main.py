from fastapi import FastAPI
import psycopg
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI in Docker"}

@app.get("/health")
def health_check():
    return {"status": "ok"}



@app.get("/db-check")
def db_check():
    database_url = os.environ.get("DATABASE_URL")
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            pg_version = cur.fetchone()[0]
            cur.execute("SELECT extname FROM pg_extension WHERE extname = 'vector';")
            vector_row = cur.fetchone()
    return {"PostgreSQL Version": pg_version,
            "pgvector_installed": vector_row is not None}