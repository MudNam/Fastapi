from fastapi import FastAPI
from google.cloud import storage
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/test-credentials")
def test_credentials():
    try:
        # Try to create a storage client (will use service account automatically)
        client = storage.Client()
        
        # Try to list buckets
        buckets = list(client.list_buckets())
        
        return {
            "status": "success",
            "buckets": [bucket.name for bucket in buckets]
        }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        } 