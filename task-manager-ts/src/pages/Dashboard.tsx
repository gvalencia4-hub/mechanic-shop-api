import { Link } from "react-router-dom";
import { useTasks } from "../context/TaskContext";

export default function Dashboard() {
  const { tasks, deleteTask } = useTasks();

  return (
    <div style={{ padding: 24 }}>
      <h2>Dashboard</h2>

      {tasks.length === 0 ? (
        <p>No tasks yet. Click “Create”.</p>
      ) : (
        <ul>
          {tasks.map((t) => (
            <li key={t.id} style={{ marginBottom: 14 }}>
              <b>{t.title}</b> — {t.status}
              <div style={{ display: "flex", gap: 10 }}>
                <Link to={`/tasks/${t.id}`}>View</Link>
                <Link to={`/tasks/${t.id}/edit`}>Edit</Link>
                <button onClick={() => deleteTask(t.id)}>Delete</button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
