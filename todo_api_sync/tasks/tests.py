from rest_framework import status
from rest_framework.test import APITestCase


class TaskAPITestCase(APITestCase):
    def setUp(self):
        # Изначальные данные для задач
        self.task_data = {
            'title': 'Test Task',
            'priority': 'medium',
            'completed': False
        }
        self.updated_task_data = {
            'title': 'Updated Task',
            'priority': 'high',
            'completed': True
        }

    def test_create_task(self):
        # Тест создания задачи (POST /tasks)
        response = self.client.post(
            '/api/tasks', self.task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.task_data['title'])
        self.assertEqual(response.data['priority'], self.task_data['priority'])
        self.assertFalse(response.data['completed'])

    def test_get_all_tasks(self):
        # Тест получения всех задач (GET /tasks)
        self.client.post('/api/tasks', self.task_data, format='json')
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], self.task_data['title'])

    def test_get_single_task(self):
        # Тест получения одной задачи по ID (GET /tasks/<id>/)
        response = self.client.post(
            '/api/tasks', self.task_data, format='json')
        task_id = response.data['id']
        response = self.client.get(f'/api/tasks/{task_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task_data['title'])
        self.assertEqual(response.data['priority'], self.task_data['priority'])

    def test_update_task(self):
        # Тест обновления задачи (PUT /tasks/<id>/)
        response = self.client.post(
            '/api/tasks', self.task_data, format='json')
        task_id = response.data['id']
        response = self.client.put(
            f'/api/tasks/{task_id}/', self.updated_task_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['title'], self.updated_task_data['title'])
        self.assertEqual(
            response.data['priority'], self.updated_task_data['priority'])
        self.assertTrue(response.data['completed'])

    def test_delete_task(self):
        # Тест удаления задачи (DELETE /tasks/<id>/)
        response = self.client.post(
            '/api/tasks', self.task_data, format='json')
        task_id = response.data['id']
        response = self.client.delete(f'/api/tasks/{task_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверка, что задача действительно удалена
        response = self.client.get(f'/api/tasks/{task_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
