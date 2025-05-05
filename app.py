from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="Test Deployment API")

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI! Deployment is working!"}

@app.get("/health")
async def health_check():
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "version": "1.0.0"}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 