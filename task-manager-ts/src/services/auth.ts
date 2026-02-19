const USER_KEY = "tm_user";
const AUTH_KEY = "tm_isLoggedIn";

export type StoredUser = { email: string; password: string };

export function register(email: string, password: string) {
  const user: StoredUser = { email, password };
  localStorage.setItem(USER_KEY, JSON.stringify(user));
  localStorage.setItem(AUTH_KEY, "true");
}

export function login(email: string, password: string) {
  const raw = localStorage.getItem(USER_KEY);
  if (!raw) return false;

  const user = JSON.parse(raw) as StoredUser;
  const ok = user.email === email && user.password === password;

  if (ok) localStorage.setItem(AUTH_KEY, "true");
  return ok;
}

export function logout() {
  localStorage.setItem(AUTH_KEY, "false");
}

export function isLoggedIn() {
  return localStorage.getItem(AUTH_KEY) === "true";
}
