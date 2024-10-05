from django.urls import path
from . import views


urlpatterns = [
    path('tasks',
         views.manage_tasks,
         name='manage_tasks'),  # GET, POST
    path('tasks/<int:task_id>/',
         views.manage_task_by_id,
         name='manage_task_by_id'),  # GET, PUT, DELETE
]
