from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from .models import PriorityEnum
from .database import get_db
from .schemas import TaskCreate, TaskUpdate, TaskResponse
from .crud import (create_task, get_tasks,
                   get_task_by_id, update_task, delete_task)


app = FastAPI()


# Разрешаем доступ с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Адрес фронтенда React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# POST /tasks - добавление новой задачи
@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
    )
async def add_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await create_task(db, task.title, task.priority)


# GET /tasks - получение списка всех задач (с фильтрацией по статусу)
@app.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(
    completed: Optional[bool] = None,
    priority: Optional[PriorityEnum] = None,
    db: AsyncSession = Depends(get_db)
):
    return await get_tasks(db, completed, priority)


# GET /tasks/{task_id} - получение задачи по её ID
@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await get_task_by_id(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# PUT /tasks/<task_id> - обновление задачи
@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_existing_task(
        task_id: int,
        task: TaskUpdate,
        db: AsyncSession = Depends(get_db)):

    updated_task = await update_task(
        db, task_id, task.title, task.priority, task.completed)

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


# DELETE /tasks/<task_id> - удаление задачи
@app.delete(
    "/tasks/{task_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT
    )
async def delete_existing_task(
        task_id: int,
        db: AsyncSession = Depends(get_db)):

    deleted_task = await delete_task(db, task_id)

    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return None
