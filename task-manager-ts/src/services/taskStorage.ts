import type { Task } from "../types/task";

const KEY = "tasks";

export function getTasks(): Task[] {
  const raw = localStorage.getItem(KEY);
  if (!raw) return [];
  try {
    return JSON.parse(raw) as Task[];
  } catch {
    return [];
  }
}

export function saveTasks(tasks: Task[]) {
  localStorage.setItem(KEY, JSON.stringify(tasks));
}

export function addTask(task: Task) {
  const tasks = getTasks();
  tasks.push(task);
  saveTasks(tasks);
}

export function updateTask(id: string, updates: Partial<Task>) {
  const tasks = getTasks().map((t) => (t.id === id ? { ...t, ...updates } : t));
  saveTasks(tasks);
}

export function deleteTask(id: string) {
  const tasks = getTasks().filter((t) => t.id !== id);
  saveTasks(tasks);
}

export function getTaskById(id: string) {
  return getTasks().find((t) => t.id === id);
}
