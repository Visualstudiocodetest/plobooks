'use client'

import { useCart } from './CartProvider'

export function AddToCartButton(props: {
  id_article: number
  titre: string
  prix_chf: number
  image_link?: string | null
}) {
  const { addItem } = useCart()
  return (
    <button
      type="button"
      className="btn btnPrimary"
      onClick={() =>
        addItem({
          id_article: props.id_article,
          titre: props.titre,
          prix_chf: props.prix_chf,
          image_link: props.image_link,
        })
      }
    >
      Ajouter au panier
    </button>
  )
}
