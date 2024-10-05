import React, { useState } from 'react';

function TaskForm({ onSubmit, initialTask = { title: '', priority: 'low', completed: false } }) {
  const [task, setTask] = useState(initialTask);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setTask({ ...task, [name]: type === 'checkbox' ? checked : value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(task);
    setTask({ title: '', priority: 'low', completed: false });
  };

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <div className="form-group">
        <label className="form-label">Task Title</label>
        <input
          type="text"
          name="title"
          className="form-input"
          value={task.title}
          onChange={handleChange}
        />
      </div>
      <div className="form-group">
        <label className="form-label">Priority</label>
        <select
          name="priority"
          className="form-select"
          value={task.priority}
          onChange={handleChange}
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>
      <div className="form-group checkbox-group">
        <label className="form-checkbox">
          <input
            type="checkbox"
            name="completed"
            checked={task.completed}
            onChange={handleChange}
          />
          Completed
        </label>
      </div>
      <button type="submit" className="submit-button">Submit</button>
    </form>
  );
}

export default TaskForm;
