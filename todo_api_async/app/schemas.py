from pydantic import BaseModel
from enum import Enum


class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCreate(BaseModel):
    title: str
    priority: PriorityEnum


class TaskUpdate(BaseModel):
    title: str
    priority: PriorityEnum
    completed: bool


class TaskResponse(BaseModel):
    id: int
    title: str
    priority: PriorityEnum
    completed: bool

    class Config:
        from_attributes = True
