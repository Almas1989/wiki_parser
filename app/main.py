from fastapi import FastAPI
from app.api.endpoints import router
from app.database import engine, Base

app = FastAPI(
    title="Wikipedia Parser with AI Summary",
    description="API для парсинга статей Wikipedia и генерации summary с помощью OpenAI",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router, prefix="/api/v1", tags=["articles"])

@app.get("/")
async def root():
    return {
        "message": "Wikipedia Parser API",
        "docs": "/docs",
        "endpoints": {
            "parse": "POST /api/v1/parse",
            "summary": "GET /api/v1/summary?url={wikipedia_url}"
        }
    }