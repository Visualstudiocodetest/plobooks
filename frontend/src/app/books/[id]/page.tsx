import { getBook } from '@/services/books'
import { Money } from '@/components/ui/Money'
import { AddToCartButton } from '@/components/cart/AddToCartButton'

export const dynamic = 'force-dynamic'

export default async function BookDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const book = await getBook(Number(id))

  return (
    <div style={{ display: 'grid', gap: 16 }}>
      <div className="card" style={{ padding: 16, display: 'grid', gap: 14 }}>
        <div style={{ display: 'grid', gridTemplateColumns: '220px 1fr', gap: 16 }}>
          <div
            className="card"
            style={{
              padding: 10,
              display: 'grid',
              placeItems: 'center',
              background: 'linear-gradient(135deg, var(--color-primary-soft), rgba(0,0,0,0))',
            }}
          >
            {book.image_link ? (
              // eslint-disable-next-line @next/next/no-img-element
              <img
                src={book.image_link}
                alt={book.titre}
                style={{ maxWidth: '100%', maxHeight: 240, objectFit: 'contain' }}
              />
            ) : (
              <div className="muted" style={{ fontWeight: 700 }}>
                Pas d'image
              </div>
            )}
          </div>

          <div style={{ display: 'grid', gap: 10 }}>
            <div>
              <h1 style={{ margin: 0 }}>{book.titre}</h1>
              <div className="muted">{book.auteur || '—'}</div>
            </div>

            <div style={{ display: 'flex', gap: 14, alignItems: 'baseline', flexWrap: 'wrap' }}>
              <Money amount={book.prix_chf} />
              <span className="muted">ISBN {book.isbn}</span>
            </div>

            <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
              {book.editeur ? <span className="muted">Éditeur: {book.editeur}</span> : null}
              {book.langue ? <span className="muted">Langue: {book.langue}</span> : null}
              {book.date_publication ? (
                <span className="muted">Publication: {book.date_publication}</span>
              ) : null}
            </div>

            <div className="muted" style={{ lineHeight: 1.55 }}>
              {book.description || 'Aucune description.'}
            </div>

            <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
              <AddToCartButton
                id_article={book.id_article}
                titre={book.titre}
                prix_chf={book.prix_chf}
                image_link={book.image_link}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
