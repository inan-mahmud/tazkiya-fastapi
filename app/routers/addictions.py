from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID


from app.database import get_db
from app.models.addictions import Addictions
from app.schemas.addictions import (
    AddictionCreate,
    AddictionUpdate,
    AddictionResponse,
    AddictionListResponse,
    AddictionCategory,
    SeverityLevel,
)

router = APIRouter(
    prefix="/addictions",
    tags=["Addictions"]
)

# ================ CREATE ===============
@router.post("/",response_model=AddictionResponse, status_code= 201)
def create_addiction(addiction: AddictionCreate, db: Session = Depends(get_db)):
    """
    Create a new addiction type
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

# =========== READ ALL ==============

@router.get("/",response_model=AddictionListResponse)
def list_addictions(category: AddictionCategory = None, severity: SeverityLevel = None, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """
    List all addiction types with optional filters.
    """
    query = db.query(Addictions)

    if category:
        query = query.filter(Addictions.category == category)
    
    if severity:
        query = query.filter(Addictions.severity == severity)
    
    addictions = query.offset(skip).limit(limit).all()

    return {
        "count": len(addictions),
        "addictions": addictions
    }

# ============ READ ONE ===============
@router.get("/addictions/{addiction_id}", response_model=AddictionResponse)
def get_addiction(addiction_id: UUID, db: Session = Depends(get_db)):
    """
    Get details of a specific addiction type by ID
    """
    addiction = db.query(Addictions).filter(Addictions.id == str(addiction_id)).first()

    if not addiction:
        raise HTTPException(status_code=404, detail= "Resource not found")
    
    return addiction


# ============== UPDATE ===============
@router.put("/{addiction_id}", response_model=AddictionResponse)
def update_addiction(
    addiction_id: UUID,
    addiction_update: AddictionUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing addiction.
    Only provided fields will be updated.
    """
    # Find the addiction
    db_addiction = db.query(Addictions).filter(Addictions.id == str(addiction_id)).first()
    
    if not db_addiction:
        raise HTTPException(status_code=404, detail="Addiction not found")
    
    # Get the update data, excluding unset fields
    update_data = addiction_update.model_dump(exclude_unset=True)
    
    # Update only the fields that were provided
    for field, value in update_data.items():
        setattr(db_addiction, field, value)
    
    db.commit()
    db.refresh(db_addiction)
    
    return db_addiction

# ========= DELETE ===========
def delete_addiction(addiction_id: UUID, db: Session = Depends(get_db)):
    """ Delete an addiction by ID"""
    db_addiction = db.query(Addictions).filter(Addictions.id == str(addiction_id)).first()

    if not db_addiction:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    db.delete(db_addiction)
    db.commit()

    return None