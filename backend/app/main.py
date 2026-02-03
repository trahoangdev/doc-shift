from __future__ import annotations

from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="DocShift API", version="0.1.0")
app.include_router(router, prefix="/api")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
