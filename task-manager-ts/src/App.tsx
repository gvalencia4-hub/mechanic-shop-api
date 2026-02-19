import { BrowserRouter, Routes, Route, Link, Navigate } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import TaskDetails from "./pages/TaskDetails";
import CreateTask from "./pages/CreateTask";
import EditTask from "./pages/EditTask";
import Login from "./pages/Login";
import Register from "./pages/Register";

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ padding: 24 }}>
        <h1>Task Manager</h1>

        <nav style={{ display: "flex", gap: 12, marginBottom: 16 }}>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/tasks/new">Create</Link>
          <Link to="/login">Login</Link>
          <Link to="/register">Register</Link>
        </nav>

        <h2 style={{ color: "lime" }}>App is rendering ✅</h2>

        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />

          {/* Tasks */}
          <Route path="/tasks/new" element={<CreateTask />} />
          <Route path="/tasks/:id" element={<TaskDetails />} />
          <Route path="/tasks/:id/edit" element={<EditTask />} />

          {/* Auth */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Fallback */}
          <Route path="*" element={<div>404 - Page not found</div>} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}
