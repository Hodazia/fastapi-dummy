from fastapi import FastAPI,UploadFile,File
import uvicorn

app = FastAPI()


@app.get("/")
def main():
    return {
        "message":"hello from microservice-2"
    }

@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    with open(f"uploads/{file.filename}", "wb") as buffer:
        buffer.write(await file.read())

    return {"filename": file.filename}
    


if __name__ == "__main__":    
    uvicorn.run(app, host="0.0.0.0", port=8001)

