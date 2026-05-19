'use client'

import { AuthProvider } from '@/components/auth/AuthProvider'
import { CartProvider } from '@/components/cart/CartProvider'
import type { ReactNode } from 'react'

export function Providers({ children }: { children: ReactNode }) {
  return (
    <AuthProvider>
      <CartProvider>{children}</CartProvider>
    </AuthProvider>
  )
}
