import { listBooks } from '@/services/books'
import { CatalogClient } from './CatalogClient'

export const dynamic = 'force-dynamic'

export default async function CatalogPage() {
  const books = await listBooks()
  return <CatalogClient books={books} />
}
