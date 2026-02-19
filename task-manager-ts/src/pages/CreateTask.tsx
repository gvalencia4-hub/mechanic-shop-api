import { useState } from "react";
import { useNavigate } from "react-router-dom";
import type { TaskStatus } from "../types/task";
import { useTasks } from "../context/TaskContext";

export default function CreateTask() {
  const navigate = useNavigate();
  const { addTask } = useTasks();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState<TaskStatus>("todo");
  const [err, setErr] = useState("");

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErr("");

    if (!title.trim()) {
      setErr("Title is required.");
      return;
    }

    addTask({ title: title.trim(), description: description.trim(), status });
    navigate("/dashboard");
  }

  return (
    <div style={{ padding: 24 }}>
      <h2>Create Task</h2>
      {err && <p style={{ color: "crimson" }}>{err}</p>}

      <form
        onSubmit={onSubmit}
        style={{ display: "grid", gap: 10, maxWidth: 420 }}
      >
        <input
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <textarea
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value as TaskStatus)}
        >
          <option value="todo">Todo</option>
          <option value="in-progress">In Progress</option>
          <option value="done">Done</option>
        </select>
        <button type="submit">Save</button>
      </form>
    </div>
  );
}
