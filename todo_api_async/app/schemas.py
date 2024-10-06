from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


# Определение приоритетов через Enum
class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


# Модель для создания задачи
class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        max_length=100,
        description="Название задачи, макс. длина - 100 символов")
    priority: PriorityEnum = Field(
        ...,
        description="Приоритет задачи (low, medium, high)")


# Модель для обновления задачи
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        max_length=100,
        description="Название задачи, макс. длина - 100 символов")
    priority: Optional[PriorityEnum] = Field(
        None,
        description="Приоритет задачи (low, medium, high)")
    completed: Optional[bool] = Field(
        None,
        description="Статус выполнения задачи")


# Модель для ответа (свойства задачи)
class TaskResponse(BaseModel):
    id: int
    title: str
    priority: PriorityEnum
    completed: bool

    # Настройки для работы с ORM
    class Config:
        orm_mode = True  # Позволяет работать с ORM моделями
        from_attributes = True  # Для ORM атрибутов (если нужно)
