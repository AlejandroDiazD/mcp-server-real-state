# domain/models.py
from sqlalchemy import Column, Integer, String, Float, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
import enum


Base = declarative_base()

class PropertyStatus(enum.Enum):
    available = "available"
    sold = "sold"

class Property(Base):
    """
    Represents a real estate property in the system.
    """
    __tablename__ = "properties"

    id = Column(String, primary_key=True, index=True)
    city = Column(String, index=True)
    price = Column(Float)
    rooms = Column(Integer)
    status = Column(SQLEnum(PropertyStatus), default=PropertyStatus.available)
    description = Column(String)
    features = Column(String)