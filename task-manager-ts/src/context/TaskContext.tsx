import React, { createContext, useContext, useMemo, useState } from "react";
import type { Task, TaskStatus } from "../types/task";
import {
  getTasks,
  addTask as storageAddTask,
  updateTask as storageUpdateTask,
  deleteTask as storageDeleteTask,
} from "../services/taskStorage";

type TaskInput = {
  title: string;
  description?: string;
  status: TaskStatus;
};

type TaskContextValue = {
  tasks: Task[];
  refresh: () => void;
  addTask: (input: TaskInput) => Task;
  updateTask: (id: string, patch: Partial<TaskInput>) => Task | null;
  deleteTask: (id: string) => void;
  getTaskById: (id: string) => Task | undefined;
};

const TaskContext = createContext<TaskContextValue | null>(null);

export function TaskProvider({ children }: { children: React.ReactNode }) {
  const [tasks, setTasks] = useState<Task[]>(() => getTasks());

  const refresh = () => setTasks(getTasks());

  const addTask = (input: TaskInput) => {
    const created = storageAddTask(input);
    setTasks(getTasks());
    return created;
  };

  const updateTask = (id: string, patch: Partial<TaskInput>) => {
    const updated = storageUpdateTask(id, patch);
    setTasks(getTasks());
    return updated;
  };

  const deleteTask = (id: string) => {
    storageDeleteTask(id);
    setTasks(getTasks());
  };

  const getTaskById = (id: string) => tasks.find((t) => t.id === id);

  const value = useMemo(
    () => ({ tasks, refresh, addTask, updateTask, deleteTask, getTaskById }),
    [tasks],
  );

  return <TaskContext.Provider value={value}>{children}</TaskContext.Provider>;
}

export function useTasks() {
  const ctx = useContext(TaskContext);
  if (!ctx) throw new Error("useTasks must be used inside <TaskProvider>");
  return ctx;
}
