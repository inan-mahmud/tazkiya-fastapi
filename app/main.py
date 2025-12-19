from fastapi import FastAPI
from app.database import Base, engine, get_db
from app.routers import addiction_router

Base.metadata.create_all(bind = engine)

app = FastAPI(
    title="Tazkiya API",
    description = "Islamic Detox Companion - Backend API",
    version = "1.0.0"
)
# ======== HEALTH CHECK =======

@app.get("/")
def health_check():
    """
    Health check endpoint.
    Returns a single message to confirm the API is running
    """
    return {
         "status": "healthy",
         "message": "Tazkiyah API is running",
         "version": "1.0.0"
    }

@app.get("/welcome")
def welcome():
    """
    Welcome message for the Tazkiya App.
    """
    return {
        "message": "Welcome",
        "welcome":"Welcome to your journey of spiritual purification"
    }

app.include_router(addiction_router)