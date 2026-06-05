from fastapi import APIRouter

health_router = APIRouter()

@health_router.get("/", status_code=200)
def begin():
    return {
        "message":"fastapi backend tutorial"
    }

@health_router.get("/health", status_code=200)
def check_health():
    return {
        "status":"healthy"
    }
