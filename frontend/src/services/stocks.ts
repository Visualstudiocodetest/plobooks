import { apiFetch } from './api'

export async function listStocks() {
  return apiFetch('/stock/')
}

export async function decrementStock(id_stock: number, qty: number) {
  return apiFetch(`/stock/${id_stock}/decrement`, {
    method: 'POST',
    body: JSON.stringify({ qty }),
  })
}

export async function getAvailableQuantityForArticle(id_article: number) {
  const stocks: any[] = await listStocks()
  return stocks
    .filter((s) => s.id_article === id_article)
    .reduce((acc, s) => acc + (s.quantite_disponible || 0), 0)
}
