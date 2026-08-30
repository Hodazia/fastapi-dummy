from fastapi import FastAPI
import os 
import uvicorn
from dotenv import load_dotenv
from routes.user.user_routes import router as userauth_router
from routes.content.content_routes import router as content_router

load_dotenv()

app = FastAPI()
app.include_router(userauth_router)
app.include_router(content_router)

@app.get("/health")
def get_health():
    return {
        "status":"the server is healthy"
    }



def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
