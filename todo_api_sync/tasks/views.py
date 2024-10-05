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


@api_view(['GET', 'PUT', 'DELETE'])
def manage_task_by_id(request, task_id):
    global tasks
    task = next((task for task in tasks if task['id'] == task_id), None)

    if not task:
        return Response(
            {'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Получение одной задачи по ID
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Обновление задачи по ID
        serializer = TaskSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            task.update(serializer.validated_data)
            return Response(task)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Удаление задачи по ID
        tasks.remove(task)
        return Response(
            {'message': 'Task deleted'}, status=status.HTTP_204_NO_CONTENT)
