from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

# Enum for Categories(like Dart enums)
class AddictionCategory(str, Enum):
    digital = "digital"
    physical = "physical"
    spiritual = "spiritual"

class SeverityLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class AddictionCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example= "Social Media")
    description: str = Field(..., min_length=10, example="Excessive scrolling and dopamine hits from likes")
    category: AddictionCategory
    severity: SeverityLevel


    class Config:
        json_schema_extra = {
            "example": {
                "name": "Social Media",
                "description": "Excessive scrolling and seeking validation through likes and comments",
                "category": "digital",
                "severity": "medium",
            }
        }

class AddictionUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, min_length=10)
    category: AddictionCategory | None = None
    severity: SeverityLevel | None = None

    class Config:
        son_schema_extra = {
            "example": {
                "name": "Social Media",
                "severity": "high",
            }
        }


class AddictionResponse(BaseModel):
    id: UUID
    name: str
    description: str
    category: AddictionCategory
    severity: SeverityLevel


class AddictionListResponse(BaseModel):
    count: int
    addictions: list[AddictionResponse]