'use client'

import Link from 'next/link'
import { useAuth } from '@/components/auth/AuthProvider'
import { useCart } from '@/components/cart/CartProvider'

export function Header() {
  const { isLoggedIn, isAdmin, setToken } = useAuth()
  const { count } = useCart()

  return (
    <header
      style={{
        position: 'sticky',
        top: 0,
        zIndex: 10,
        background: 'rgba(var(--color-surface-rgb), 0.92)',
        backdropFilter: 'blur(10px)',
        borderBottom: '1px solid var(--color-border)',
      }}
    >
      <div
        className="container"
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '12px 16px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
          <Link href="/" style={{ fontWeight: 900, letterSpacing: 0.3, color: 'var(--color-text)' }}>
            PLOBOOKS
          </Link>
          <nav style={{ display: 'flex', gap: 12, fontWeight: 600 }}>
            <Link className="muted" href="/catalog">
              Catalogue
            </Link>
            {isLoggedIn ? (
              <Link className="muted" href="/scan">
                Scanner
              </Link>
            ) : null}
            {isAdmin ? (
              <Link className="muted" href="/admin">
                Back-office
              </Link>
            ) : null}
          </nav>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <Link className="btn btnGhost" href="/cart">
            Panier ({count})
          </Link>
          {isLoggedIn ? (
            <button className="btn" onClick={() => setToken(null)} type="button">
              Déconnexion
            </button>
          ) : (
            <Link className="btn btnPrimary" href="/login">
              Connexion
            </Link>
          )}
        </div>
      </div>
    </header>
  )
}
