'use client'

import Link from 'next/link'
import { useCart } from '@/components/cart/CartProvider'
import { Money } from '@/components/ui/Money'
import CartItemRow from '@/components/cart/CartItemRow'

export default function CartPage() {
  const { items, total, removeItem, setQuantity } = useCart()

  return (
    <div className="container page-main">
      <div className="content-center">
        <h1 style={{ margin: 0 }}>Panier</h1>

        {items.length === 0 ? (
          <div className="card cardPadding">
            <div className="muted">Votre panier est vide.</div>
            <div style={{ marginTop: 12 }}>
              <Link className="btn btnPrimary" href="/catalog">
                Parcourir le catalogue
              </Link>
            </div>
          </div>
        ) : (
          <>
            <div className="card cardPadding">
              {items.map((it) => (
                <CartItemRow key={it.id_article} item={it} onRemove={removeItem} onSetQuantity={setQuantity} />
              ))}
            </div>

            <div className="card cardPadding" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
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
    </div>
  )
}
