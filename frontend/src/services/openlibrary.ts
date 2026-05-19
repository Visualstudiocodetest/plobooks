export type OpenLibraryBook = {
  title?: string
  authors?: Array<{ name?: string }>
  publishers?: Array<{ name?: string }>
  publish_date?: string
  cover?: { large?: string; medium?: string; small?: string }
  notes?: string
  by_statement?: string
  subtitle?: string
}

export async function lookupIsbn(isbn: string): Promise<OpenLibraryBook | null> {
  const clean = isbn.replace(/[^0-9Xx]/g, '')
  if (!clean) return null
  const url = `https://openlibrary.org/api/books?bibkeys=ISBN:${encodeURIComponent(clean)}&format=json&jscmd=data`
  const res = await fetch(url)
  if (!res.ok) return null
  const json = (await res.json()) as Record<string, OpenLibraryBook>
  return json[`ISBN:${clean}`] ?? null
}
