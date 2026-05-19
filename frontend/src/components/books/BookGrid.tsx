import type { BookRead } from '@/types/api'
import { BookCard } from './BookCard'

export function BookGrid({ books }: { books: BookRead[] }) {
  if (!books.length) {
    return <div className="muted">Aucun livre pour le moment.</div>
  }

  return (
    <div className="book-grid">
      {books.map((b) => (
        <BookCard key={b.id_article} book={b} />
      ))}
    </div>
  )
}
