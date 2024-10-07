from fastapi import status

from conftest import client


# Тест получения всех задач
def test_list_tasks():
    # Создание нескольких задач
    task_1 = {"title": "Task 1", "priority": "low"}
    task_2 = {"title": "Task 2", "priority": "high"}

    response_1 = client.post("/tasks", json=task_1)
    response_2 = client.post("/tasks", json=task_2)

    # Проверим, что задачи созданы успешно
    assert response_1.status_code == status.HTTP_201_CREATED
    assert response_2.status_code == status.HTTP_201_CREATED

    # Получение всех задач
    response = client.get("/tasks")

    assert response.status_code == status.HTTP_200_OK
    tasks = response.json()

    # Проверим, что создано как минимум 2 задачи
    assert len(tasks) == 2
    assert any(task["title"] == "Task 1" for task in tasks)
    assert any(task["title"] == "Task 2" for task in tasks)


# Тест создания задачи
def test_create_task():
    task_data = {
        "title": "New Task",
        "priority": "medium"
    }
    response = client.post(
        "/tasks",
        json=task_data
    )

    assert response.status_code == status.HTTP_201_CREATED
    task = response.json()
    assert task["title"] == task_data["title"]
    assert task["priority"] == task_data["priority"]
    assert not task["completed"]


# Тест получения задачи по ID
def test_get_task_by_id():
    task_data = {"title": "Task for ID", "priority": "medium"}
    # Создание задачи
    post_response = client.post("/tasks", json=task_data)
    task_id = post_response.json()["id"]

    # Получение задачи по ID
    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == status.HTTP_200_OK
    task = get_response.json()
    assert task["title"] == task_data["title"]
    assert task["priority"] == task_data["priority"]


# Тест обновления задачи
def test_update_task():
    task_data = {"title": "Original Task", "priority": "low"}
    # Создание задачи
    post_response = client.post("/tasks", json=task_data)
    task_id = post_response.json()["id"]

    # Данные для обновления
    updated_data = {
        "title": "Updated Task", "priority": "high", "completed": True}
    put_response = client.put(f"/tasks/{task_id}", json=updated_data)

    assert put_response.status_code == status.HTTP_200_OK
    updated_task = put_response.json()
    assert updated_task["title"] == "Updated Task"
    assert updated_task["priority"] == "high"
    assert updated_task["completed"] is True


# Тест удаления задачи
def test_delete_task():
    task_data = {"title": "Task to delete", "priority": "low"}
    # Создание задачи
    post_response = client.post("/tasks", json=task_data)
    task_id = post_response.json()["id"]

    # Удаление задачи
    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    # Проверка, что задача удалена
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
