import React from 'react';
import TaskForm from './TaskForm';

function TaskList({ tasks, onUpdate, onDelete }) {
  return (
    <ul className="task-list">
      {tasks.map((task) => (
        <li key={task.id} className={`task-item ${task.completed ? 'completed' : ''}`}>
          <div className="task-details">
            <h3 className={`task-title ${task.completed ? 'task-completed-text' : ''}`}>{task.title}</h3>
            <p className="task-priority">Priority: {task.priority}</p>
            <p className="task-completed">Completed: {task.completed ? 'Yes' : 'No'}</p>
          </div>
          <div className="task-actions">
            <TaskForm
              initialTask={task}
              onSubmit={(updatedTask) => onUpdate({ ...task, ...updatedTask })}
            />
            <button className="delete-button" onClick={() => onDelete(task.id)}>Delete</button>
          </div>
        </li>
      ))}
    </ul>
  );
}

export default TaskList;
