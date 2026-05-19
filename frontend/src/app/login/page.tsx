'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/components/auth/AuthProvider'
import { ApiError } from '@/services/api'
import { login } from '@/services/auth'

export default function LoginPage() {
  const router = useRouter()
  const { setToken } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const token = await login({ username: email, password })
      setToken(token.access_token)
      router.push('/')
    } catch (e) {
      const err = e as unknown
      setError(err instanceof ApiError ? err.message : 'Connexion impossible')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: 520, margin: '0 auto', display: 'grid', gap: 14 }}>
      <h1 style={{ margin: 0 }}>Connexion</h1>
      <form className="card" style={{ padding: 16, display: 'grid', gap: 12 }} onSubmit={onSubmit}>
        <input className="input" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <input
          className="input"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Mot de passe"
          type="password"
        />
        {error ? <div className="muted">{error}</div> : null}
        <button className="btn btnPrimary" type="submit" disabled={loading}>
          {loading ? 'Connexion…' : 'Se connecter'}
        </button>
        <div className="muted">
          Pas de compte ? <Link href="/register">Créer un compte</Link>
        </div>
      </form>
    </div>
  )
}
