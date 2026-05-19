import Link from 'next/link'
import { listBooks } from '@/services/books'
import { BookGrid } from '@/components/books/BookGrid'

export const dynamic = 'force-dynamic'

export default async function HomePage() {
  const books = await listBooks().catch(() => [])

  return (
    <div className="content-center">
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
