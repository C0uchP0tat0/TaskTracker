from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import PriorityEnum, Task


async def create_task(db: AsyncSession, title: str, priority: str):
    new_task = Task(title=title, priority=priority)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


async def get_tasks(
        db: AsyncSession,
        completed: bool = None,
        priority: PriorityEnum = None):
    query = select(Task)

    # Фильтр по статусу
    if completed is not None:
        query = query.where(Task.completed == completed)

    # Фильтр по приоритету
    if priority is not None:
        query = query.where(Task.priority == priority.value)

    result = await db.execute(query)
    return result.scalars().all()


async def get_task_by_id(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalars().first()


async def update_task(
        db: AsyncSession,
        task_id: int,
        title: str,
        priority: str,
        completed: bool):
    task = await get_task_by_id(db, task_id)

    if task:
        task.title = title
        task.priority = priority
        task.completed = completed
        await db.commit()
        return task
    return None


async def delete_task(db: AsyncSession, task_id: int):
    task = await get_task_by_id(db, task_id)

    if task:
        await db.delete(task)
        await db.commit()
        return task
    return None
