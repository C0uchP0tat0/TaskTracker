import React, { useState, useEffect } from 'react';
import TaskForm from './TaskForm';
import TaskList from './TaskList';
import API_URL from './config';
import './styles.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filters, setFilters] = useState({ completed: '', priority: '' }); // Добавляем состояние для фильтров

  // Функция для получения задач с фильтрами
  const fetchTasks = () => {
    setIsLoading(true);
    let url = `${API_URL}/tasks`;

    // Если фильтры выбраны, добавляем их в запрос
    const queryParams = [];
    if (filters.completed !== '') queryParams.push(`completed=${filters.completed}`);
    if (filters.priority !== '') queryParams.push(`priority=${filters.priority}`);
    if (queryParams.length > 0) url += `?${queryParams.join('&')}`;

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        setTasks(data);
        setIsLoading(false);
      });
  };

  // Получение всех задач при монтировании компонента и при изменении фильтров
  useEffect(() => {
    fetchTasks();
  }, [filters]);

  // Функция для добавления новой задачи
  const addTask = (newTask) => {
    fetch(`${API_URL}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newTask),
    })
      .then((response) => response.json())
      .then((task) => {
        setTasks([task, ...tasks]);  // Добавляем новую задачу в начало списка
      });
  };

  // Функция для обновления задачи
  const updateTask = (updatedTask) => {
    fetch(`${API_URL}/tasks/${updatedTask.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updatedTask),
    })
      .then((response) => response.json())
      .then((task) => {
        setTasks(tasks.map((t) => (t.id === task.id ? task : t)));
      });
  };

  // Функция для удаления задачи
  const deleteTask = (id) => {
    fetch(`${API_URL}/tasks/${id}`, {
      method: 'DELETE',
    }).then(() => {
      setTasks(tasks.filter((task) => task.id !== id));
    });
  };

  // Сортируем задачи: выполненные в конце
  const sortedTasks = [...tasks].sort((a, b) => a.completed - b.completed);

  // Функция для обновления фильтров
  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters({ ...filters, [name]: value });
  };

  if (isLoading) return <div className="loading">Loading...</div>;

  return (
    <div className="app-container">
      {/* Заголовок приложения */}
      <header className="app-header">
        
        <div class="header-container">
        <img src="https://rarus.ru/local/templates/rarus.light/front/build/img/header/header-logo-30.svg?202310091052" alt="Company Logo" class="header-logo" />
        <nav class="header-nav">
          <a href="#">Products</a>
          <a href="#">Events</a>
          <a href="#">Support</a>
          <a href="#">About Us</a>
        </nav>
      </div>
      </header>
      <h1 className="app-title">Task Manager</h1>
      

      {/* Форма фильтров */}
      <div className="filters">
        <label>
          Completed:
          <select name="completed" value={filters.completed} onChange={handleFilterChange}>
            <option value="">All</option>
            <option value="true">Completed</option>
            <option value="false">Not Completed</option>
          </select>
        </label>

        <label>
          Priority:
          <select name="priority" value={filters.priority} onChange={handleFilterChange}>
            <option value="">All</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </label>
      </div>

      <TaskForm onSubmit={addTask} />
      <TaskList tasks={sortedTasks} onUpdate={updateTask} onDelete={deleteTask} />
    </div>
  );
}

export default App;
