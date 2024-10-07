from sqlalchemy import Column, Integer, String, Boolean, Enum
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
import enum


Base = declarative_base()


class PriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    priority = Column(Enum(PriorityEnum))
    completed = Column(Boolean, default=False)
