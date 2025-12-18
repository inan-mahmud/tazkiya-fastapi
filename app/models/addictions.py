import uuid
from sqlalchemy import Column, String, Enum as SQLEnum
from app.database import Base
from app.schemas.addictions import AddictionCategory, SeverityLevel


class Addictions(Base):
    """
    Database model for addictions table.
    Each attribute = one column in the table.
    """

    __tablename__ = "addictions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, index= True)
    description = Column(String(500), nullable=False)
    category = Column(SQLEnum(AddictionCategory), nullable=False)
    severity = Column(SQLEnum(SeverityLevel), nullable=False)

    