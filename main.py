from fastapi import FastAPI
from routes.health import health_router
from routes.user_router import api_router
from routes.user.user_routes import router
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()
DEV_PORT = os.getenv("DEVELOPMENT_PORT")

app = FastAPI()

app.include_router(api_router)
app.include_router(health_router)
app.include_router(router)


def main():
    # i have changed the port=8002 for development , since the port 8000 is in use by production EC2 server
    uvicorn.run(app, host="0.0.0.0", port=int(DEV_PORT))


'''
Will extend the above functionality , now by adding DB also
- add a postgresql, can run a docker image 
- 


'''

if __name__ == "__main__":
    main()
