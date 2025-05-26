# Launches the backend
from fastapi import FastAPI
from BackendService.routes import router as backend_router
import uvicorn


app = FastAPI(
    title="Backend Service API",
    version="1.0.0",
    description="API for managing image metadata and users."
)

# Include your router (assumes prefix is empty or handled in routes.py)
app.include_router(backend_router)

if __name__ == "__main__":
    uvicorn.run("BackendService.api:app", host="0.0.0.0", port=8000, reload=True)