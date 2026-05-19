'use client'

import Link from 'next/link'
import { useCart } from '@/components/cart/CartProvider'
import { Money } from '@/components/ui/Money'

export default function CartPage() {
  const { items, total, removeItem, setQuantity } = useCart()

  return (
    <div style={{ display: 'grid', gap: 16 }}>
      <h1 style={{ margin: 0 }}>Panier</h1>

      {items.length === 0 ? (
        <div className="card" style={{ padding: 16 }}>
          <div className="muted">Votre panier est vide.</div>
          <div style={{ marginTop: 12 }}>
            <Link className="btn btnPrimary" href="/catalog">
              Parcourir le catalogue
            </Link>
          </div>
        </div>
      ) : (
        <>
          <div className="card" style={{ padding: 16, display: 'grid', gap: 12 }}>
            {items.map((it) => (
              <div
                key={it.id_article}
                style={{
                  display: 'grid',
                  gridTemplateColumns: '1fr auto auto',
                  gap: 10,
                  alignItems: 'center',
                  borderBottom: '1px solid var(--color-border)',
                  paddingBottom: 10,
                }}
              >
                <div style={{ display: 'grid', gap: 4 }}>
                  <div style={{ fontWeight: 800 }}>{it.titre}</div>
                  <div className="muted">
                    <Money amount={it.prix_chf} />
                  </div>
                </div>

                <input
                  className="input"
                  style={{ width: 90, textAlign: 'center' }}
                  inputMode="numeric"
                  value={String(it.quantity)}
                  onChange={(e) => {
                    const n = Number(e.target.value)
                    if (!Number.isFinite(n)) return
                    setQuantity(it.id_article, Math.max(0, Math.min(99, Math.floor(n))))
                  }}
                />

                <button className="btn" type="button" onClick={() => removeItem(it.id_article)}>
                  Retirer
                </button>
              </div>
            ))}
          </div>

          <div className="card" style={{ padding: 16, display: 'flex', justifyContent: 'space-between' }}>
            <div style={{ fontWeight: 900 }}>Total</div>
            <Money amount={total} />
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
            <Link className="btn btnPrimary" href="/checkout">
              Passer commande
            </Link>
          </div>
        </>
      )}
    </div>
  )
}
