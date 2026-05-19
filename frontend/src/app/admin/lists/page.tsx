'use client'

import Link from 'next/link'
import { useAuth } from '@/components/auth/AuthProvider'

export default function AdminListsIndex() {
  const { isLoggedIn } = useAuth()

  return (
    <div style={{ display: 'grid', gap: 16 }}>
      <h1 style={{ margin: 0 }}>Gérer les listes</h1>
      <div className="card" style={{ padding: 16, display: 'grid', gap: 10 }}>
        <div style={{ fontWeight: 800 }}>Listes</div>
        <div className="muted">Gérez les catégories, états d'usure, et types d'objet.</div>
        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
          <Link className="btn" href="/admin/lists/type-objets">
            Types d'objets
          </Link>
          <Link className="btn" href="/admin/lists/etat-usures">
            États d'usure
          </Link>
          <Link className="btn" href="/admin/lists/categories">
            Catégories
          </Link>
          <Link className="btn" href="/admin/lists/article-categories">
            Article categories
          </Link>
        </div>
      </div>
    </div>
  )
}
