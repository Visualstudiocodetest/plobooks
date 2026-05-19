'use client'

import Link from 'next/link'
import { useAuth } from '@/components/auth/AuthProvider'

export default function AdminHomePage() {
  const { isLoggedIn } = useAuth()

  return (
    <div style={{ display: 'grid', gap: 16 }}>
      <h1 style={{ margin: 0 }}>Interface admin</h1>
      <div className="card" style={{ padding: 16, display: 'grid', gap: 10 }}>
        <div style={{ fontWeight: 800 }}>Accès</div>
        <div className="muted">
          {isLoggedIn
            ? 'Connecté. Vous pouvez gérer le catalogue.'
            : 'Connectez-vous pour créer / modifier des livres (endpoints protégés).'}
        </div>
        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
          <Link className="btn btnPrimary" href="/admin/books">
            Gérer les livres
          </Link>
          <Link className="btn" href="/admin/lists">
            Gérer les listes
          </Link>
          <Link className="btn" href="/login">
            Connexion
          </Link>
        </div>
      </div>
    </div>
  )
}
