'use client'

import Link from 'next/link'
import { useAuth } from '@/components/auth/AuthProvider'

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const { isLoggedIn, isAdmin } = useAuth()

  if (!isLoggedIn) {
    return (
      <div className="card" style={{ padding: 16, display: 'grid', gap: 10 }}>
        <div style={{ fontWeight: 900 }}>Connexion requise</div>
        <div className="muted">Connectez-vous avec un compte admin pour accéder au back-office.</div>
        <Link className="btn btnPrimary" href="/login">
          Se connecter
        </Link>
      </div>
    )
  }

  if (!isAdmin) {
    return (
      <div className="card" style={{ padding: 16, display: 'grid', gap: 10 }}>
        <div style={{ fontWeight: 900 }}>Accès refusé</div>
        <div className="muted">Ce back-office est réservé aux administrateurs.</div>
        <Link className="btn" href="/">
          Retour à l’accueil
        </Link>
      </div>
    )
  }

  return <>{children}</>
}
