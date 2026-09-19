from fastapi import FastAPI

from abss.api.routes.companies import router as companies_router
from abss.api.routes.simulations import router as simulations_router
from abss.config.settings import settings

app = FastAPI(title=settings.app_name)

app.include_router(companies_router)
app.include_router(simulations_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
    }