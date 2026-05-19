'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'
import type { BookRead } from '@/types/api'
import { listBooks } from '@/services/books'
import { ApiError } from '@/services/api'

export default function AdminBooksPage() {
  const [books, setBooks] = useState<BookRead[]>([])
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let mounted = true
    setLoading(true)
    listBooks()
      .then((b) => {
        if (!mounted) return
        setBooks(b)
      })
      .catch((e: unknown) => {
        if (!mounted) return
        setError(e instanceof ApiError ? e.message : 'Erreur de chargement')
      })
      .finally(() => {
        if (!mounted) return
        setLoading(false)
      })
    return () => {
      mounted = false
    }
  }, [])

  return (
    <div style={{ display: 'grid', gap: 14 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', gap: 10, flexWrap: 'wrap' }}>
        <h1 style={{ margin: 0 }}>Livres</h1>
        <Link className="btn btnPrimary" href="/admin/books/new">
          Nouveau livre
        </Link>
      </div>

      {loading ? <div className="muted">Chargement…</div> : null}
      {error ? <div className="muted">{error}</div> : null}

      <div className="card" style={{ padding: 12, display: 'grid', gap: 10 }}>
        {books.map((b) => (
          <div
            key={b.id_article}
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              gap: 10,
              borderBottom: '1px solid var(--color-border)',
              paddingBottom: 10,
              alignItems: 'center',
            }}
          >
            <div style={{ display: 'grid' }}>
              <div style={{ fontWeight: 800 }}>{b.titre}</div>
              <div className="muted" style={{ fontSize: 13 }}>
                ISBN {b.isbn} · id {b.id_article}
              </div>
            </div>
            <Link className="btn" href={`/admin/books/${b.id_article}`}>
              Modifier
            </Link>
          </div>
        ))}
        {!books.length && !loading ? <div className="muted">Aucun livre.</div> : null}
      </div>
    </div>
  )
}
