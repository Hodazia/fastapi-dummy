from fastapi import FastAPI
from routes.health import health_router
from routes.user_router import api_router
import uvicorn

app = FastAPI()
app.include_router(api_router)
app.include_router(health_router)


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
