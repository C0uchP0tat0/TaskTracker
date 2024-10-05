from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer


tasks = []
task_id_counter = 1


@api_view(['GET', 'POST'])
def manage_tasks(request):
    global task_id_counter

    if request.method == 'POST':
        # Добавление новой задачи
        serializer = TaskSerializer(data=request.data)  # Используем сериализатор для валидации данных# noqa: E501
        if serializer.is_valid():
            task_data = serializer.validated_data
            task_data['id'] = task_id_counter
            task_data['completed'] = False
            tasks.append(task_data)
            task_id_counter += 1
            return Response(task_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        # Получение списка всех задач
        serializer = TaskSerializer(tasks, many=True)  # Используем сериализатор для сериализации списка задач# noqa: E501
        return Response(serializer.data)


# Получение одной задачи по ID
@api_view(['GET'])
def get_task(request, task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)

    if task is None:
        return Response(
            {'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task)  # Используем сериализатор для сериализации одной задачи# noqa: E501
    return Response(serializer.data)


# PUT /tasks/<task_id> - обновление задачи
@api_view(['PUT'])
def update_task(request, task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)

    if not task:
        return Response(
            {'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(data=request.data, partial=True)  # Позволяем частичное обновление  # noqa: E501
    if serializer.is_valid():
        task.update(serializer.validated_data)  # Обновляем задачу с помощью валидированных данных  # noqa: E501
        return Response(task)
    return Response(
        serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE /tasks/<task_id> - удаление задачи
@api_view(['DELETE'])
def delete_task(request, task_id):
    global tasks
    task = next((task for task in tasks if task['id'] == task_id), None)

    if task:
        tasks.remove(task)
        return Response(
            {'message': 'Task deleted'}, status=status.HTTP_204_NO_CONTENT)
    return Response(
        {'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
