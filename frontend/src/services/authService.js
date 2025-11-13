import api from './api';

const TOKEN_KEY = 'auth.token';
const USER_KEY = 'auth.user';

export async function login(username, password) {
  const res = await api.post('/auth/login', { username, password });
  const { access_token, user } = res.data;
  window.localStorage.setItem(TOKEN_KEY, access_token);
  window.localStorage.setItem(USER_KEY, JSON.stringify(user));
  return user;
}

export function logout() {
  window.localStorage.removeItem(TOKEN_KEY);
  window.localStorage.removeItem(USER_KEY);
}

export function getCurrentUser() {
  const raw = window.localStorage.getItem(USER_KEY);
  return raw ? JSON.parse(raw) : null;
}

export function isAuthenticated() {
  return !!window.localStorage.getItem(TOKEN_KEY);
}