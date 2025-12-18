from fastapi import FastAPI, Depends, HTTPException
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from app.models.addictions import Addictions
from app.schemas.addictions import (
    AddictionCreate,
    AddictionResponse,
    AddictionListResponse,
    AddictionCategory,
    SeverityLevel,
)
from app.database import Base, engine, get_db

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

# ========= ACTUAL ENDPOINTS ========

@app.get("/addictions/{addiction_id}", response_model=AddictionResponse)
def get_addiction(addiction_id: UUID, db: Session = Depends(get_db)):
    """
    Get details of a specific addiction type by ID
    """
    addiction = db.query(Addictions).filter(Addictions.id == str(addiction_id)).first()

    if not addiction:
        raise HTTPException(status_code=404, detail= "Resource not found")
    
    return addiction

@app.get("/addictions", response_model=AddictionListResponse)
def list_addictions(category: AddictionCategory = None, severity: SeverityLevel = None, db: Session = Depends(get_db)):
    """
    List all addiction types with optional filters.
    """
    query = db.query(Addictions)

    if category:
        query = query.filter(Addictions.category == category)
    
    if severity:
        query = query.filter(Addictions.severity == severity)
    
    addictions = query.all()

    return {
        "count": len(addictions),
        "addictions": addictions
    }

@app.post("/addictions",response_model=AddictionResponse, status_code= 201)
def create_addiction(addiction: AddictionCreate, db: Session = Depends(get_db)):
    """
    Create a new addiction type.
    """
    db_addiction = Addictions(
        name = addiction.name,
        description = addiction.description,
        category = addiction.category,
        severity = addiction.severity
    )

    db.add(db_addiction)
    db.commit()
    db.refresh(db_addiction)

    return db_addiction