from django.urls import path
from . import views


urlpatterns = [
    path('tasks', views.manage_tasks, name='manage_tasks'),  # GET, POST
    path('tasks/<int:task_id>/', views.get_task, name='get_task'),  # GET
    path('tasks/<int:task_id>/update', views.update_task, name='update_task'),  # PUT# noqa: E501
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),  # DELETE# noqa: E501
]
