from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Update CLI Test API", version="0.1.0")


class Calculation(BaseModel):
    a: int
    b: int


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "update-cli-test"}


@app.get("/api/message")
def message() -> dict[str, str]:
    return {"message": "Hello from FastAPI"}


@app.post("/api/add")
def add(payload: Calculation) -> dict[str, int]:
    return {"result": payload.a + payload.b}
