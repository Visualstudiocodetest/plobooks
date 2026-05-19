"use client"

import { useEffect, useState } from 'react'
import { Money } from '@/components/ui/Money'
import type { CartItem } from './CartProvider'
import { getAvailableQuantityForArticle } from '@/services/stocks'

export default function CartItemRow({
  item,
  onRemove,
  onSetQuantity,
}: {
  item: CartItem
  onRemove: (id_article: number) => void
  onSetQuantity: (id_article: number, q: number) => void
}) {
  const [available, setAvailable] = useState<number | null>(null)

  useEffect(() => {
    let mounted = true
    getAvailableQuantityForArticle(item.id_article).then((qty) => {
      if (mounted) setAvailable(qty)
    })
    return () => {
      mounted = false
    }
  }, [item.id_article])

  useEffect(() => {
    if (available !== null && item.quantity > available) {
      onSetQuantity(item.id_article, available)
    }
  }, [available, item.quantity, item.id_article, onSetQuantity])

  const decrease = () => {
    if (item.quantity <= 1) return onRemove(item.id_article)
    onSetQuantity(item.id_article, item.quantity - 1)
  }

  const increase = async () => {
    const qty = available === null ? await getAvailableQuantityForArticle(item.id_article) : available
    if (item.quantity + 1 > qty) return
    onSetQuantity(item.id_article, item.quantity + 1)
  }

  return (
    <div className="cart-item-row">
      <div className="cart-item-info">
        <div style={{ fontWeight: 800 }}>{item.titre}</div>
        <div className="muted">
          <Money amount={item.prix_chf} />
        </div>
      </div>

      <div className="qty-controls">
        <button className="btn" type="button" onClick={decrease} aria-label="decrease">
          −
        </button>
        <div className="cart-qty-count">{item.quantity}</div>
        <button
          className="btn"
          type="button"
          onClick={increase}
          aria-label="increase"
          disabled={available !== null && item.quantity >= available}
        >
          +
        </button>
      </div>
      <div className="remove-wrap">
        <button className="btn" type="button" onClick={() => onRemove(item.id_article)}>
          Retirer
        </button>
      </div>
    </div>
  )
}
