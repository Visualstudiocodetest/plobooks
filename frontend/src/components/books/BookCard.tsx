import Link from 'next/link'
import type { BookRead } from '@/types/api'
import { Money } from '@/components/ui/Money'

export function BookCard({ book }: { book: BookRead }) {
  return (
    <Link
      href={`/books/${book.id_article}`}
      className="card"
      style={{
        overflow: 'hidden',
        display: 'grid',
        gridTemplateRows: '160px 1fr',
      }}
    >
      <div
        style={{
          background: 'linear-gradient(135deg, var(--color-primary-soft), rgba(0,0,0,0))',
          display: 'grid',
          placeItems: 'center',
        }}
      >
        {book.image_link ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={book.image_link}
            alt={book.titre}
            style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }}
          />
        ) : (
          <div className="muted" style={{ fontWeight: 700 }}>
            Livre
          </div>
        )}
      </div>
      <div style={{ padding: 12, display: 'grid', gap: 6 }}>
        <div style={{ fontWeight: 800, lineHeight: 1.2 }}>{book.titre}</div>
        <div className="muted" style={{ fontSize: 13 }}>
          {book.auteur || '—'}
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: 8 }}>
          <Money amount={book.prix_chf} />
          <span className="muted" style={{ fontSize: 12 }}>
            ISBN {book.isbn}
          </span>
        </div>
      </div>
    </Link>
  )
}
