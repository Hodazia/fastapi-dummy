from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def main():
    return {
        "message":"hello from microservice-2"
    }

    


if __name__ == "__main__":    
    uvicorn.run(app, host="0.0.0.0", port=8001)

