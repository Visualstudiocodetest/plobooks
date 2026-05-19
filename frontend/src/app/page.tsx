import Link from 'next/link'
import { listBooks } from '@/services/books'
import { BookGrid } from '@/components/books/BookGrid'

export const dynamic = 'force-dynamic'

export default async function HomePage() {
  const books = await listBooks().catch(() => [])

  return (
    <div style={{ display: 'grid', gap: 24 }}>
      <section className="card" style={{ padding: 20 }}>
        <div
          style={{
            display: 'grid',
            gap: 12,
          }}
        >
          <h1 style={{ margin: 0, fontSize: 34, lineHeight: 1.1 }}>PLOBOOKS</h1>
          <p className="muted" style={{ margin: 0, maxWidth: 720 }}>
            Une sélection de livres de seconde main. Les bénéfices soutiennent la réinsertion
            professionnelle via Caritas.
          </p>
          <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
            <Link className="btn btnPrimary" href="/catalog">
              Voir le catalogue
            </Link>
            <Link className="btn btnGhost" href="/login">
              Se connecter
            </Link>
          </div>
        </div>
      </section>

      <section style={{ display: 'grid', gap: 12 }}>
        <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between' }}>
          <h2 style={{ margin: 0 }}>Derniers livres</h2>
          <Link className="muted" href="/catalog">
            Tout voir →
          </Link>
        </div>
        <BookGrid books={books.slice(0, 8)} />
      </section>
    </div>
  )
}
