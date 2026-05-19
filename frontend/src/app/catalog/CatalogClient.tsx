'use client'

import { useMemo, useState } from 'react'
import type { BookRead } from '@/types/api'
import { BookGrid } from '@/components/books/BookGrid'

export function CatalogClient({ books }: { books: BookRead[] }) {
  const [query, setQuery] = useState('')

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return books
    return books.filter((b) => {
      const hay = `${b.titre} ${b.auteur ?? ''} ${b.isbn}`.toLowerCase()
      return hay.includes(q)
    })
  }, [books, query])

  return (
    <div style={{ display: 'grid', gap: 14 }}>
      <div className="card" style={{ padding: 14, display: 'grid', gap: 10 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap' }}>
          <h1 style={{ margin: 0 }}>Catalogue</h1>
          <div className="muted" style={{ alignSelf: 'end' }}>
            {filtered.length} résultat(s)
          </div>
        </div>
        <input
          className="input"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Rechercher par titre, auteur ou ISBN"
        />
      </div>

      <BookGrid books={filtered} />
    </div>
  )
}
