import { apiFetch } from './api'
import type { LoginRequest, Token, UserCreate, UserRead } from '@/types/api'

export async function login(payload: LoginRequest): Promise<Token> {
  return apiFetch<Token>('/auth/token', { method: 'POST', body: JSON.stringify(payload) })
}

export async function register(payload: UserCreate): Promise<UserRead> {
  return apiFetch<UserRead>('/auth/register', { method: 'POST', body: JSON.stringify(payload) })
}

export function persistToken(token: string) {
  window.localStorage.setItem('plobooks_token', JSON.stringify(token))
}

export function clearToken() {
  window.localStorage.removeItem('plobooks_token')
}

export function readToken(): string | null {
  const raw = window.localStorage.getItem('plobooks_token')
  if (!raw) return null
  try {
    const parsed = JSON.parse(raw) as unknown
    return typeof parsed === 'string' ? parsed : raw
  } catch {
    return raw
  }
}
