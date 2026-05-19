'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { ApiError } from '@/services/api'
import { createBook } from '@/services/books'
import { lookupIsbn } from '@/services/openlibrary'

export default function AdminNewBookPage() {
  const router = useRouter()
  const [titre, setTitre] = useState('')
  const [isbn, setIsbn] = useState('')
  const [auteur, setAuteur] = useState('')
  const [prix, setPrix] = useState('5.00')
  const [imageLink, setImageLink] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [autofillLoading, setAutofillLoading] = useState(false)

  async function autofill(isbnValue: string) {
    setError(null)
    setAutofillLoading(true)
    try {
      const data = await lookupIsbn(isbnValue)
      if (!data) {
        setError('Aucune donnée trouvée sur OpenLibrary pour cet ISBN.')
        return
      }
      const title = [data.title, data.subtitle].filter(Boolean).join(' — ')
      if (title) setTitre(title)
      const author = data.authors?.map((a) => a.name).filter(Boolean).join(', ')
      if (author) setAuteur(author)
      const cover = data.cover?.large || data.cover?.medium || data.cover?.small
      if (cover) setImageLink(cover)
      const desc = typeof data.notes === 'string' ? data.notes : ''
      if (desc) setDescription(desc)
    } catch {
      setError('Impossible de contacter OpenLibrary.')
    } finally {
      setAutofillLoading(false)
    }
  }

  async function onAutofill() {
    await autofill(isbn)
  }

  useEffect(() => {
    if (typeof window === 'undefined') return
    const param = new URLSearchParams(window.location.search).get('isbn')
    const raw = (param || '').trim()
    if (!raw) return

    setIsbn(raw)
    void autofill(raw)
    // run once on mount
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const created = await createBook({
        id_type_objet: 1,
        id_etat_usure: 1,
        titre,
        isbn,
        auteur: auteur || null,
        editeur: null,
        date_publication: null,
        langue: null,
        description: description || null,
        image_link: imageLink || null,
        prix_chf: Number(prix),
        actif: true,
      })
      router.push(`/admin/books/${created.id_article}`)
    } catch (e) {
      const err = e as unknown
      setError(err instanceof ApiError ? err.message : 'Création impossible')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: 720, margin: '0 auto', display: 'grid', gap: 14 }}>
      <h1 style={{ margin: 0 }}>Nouveau livre</h1>
      <form className="card" style={{ padding: 16, display: 'grid', gap: 12 }} onSubmit={onSubmit}>
        <input className="input" value={titre} onChange={(e) => setTitre(e.target.value)} placeholder="Titre" />
        <div style={{ display: 'grid', gridTemplateColumns: '1fr auto', gap: 10 }}>
          <input className="input" value={isbn} onChange={(e) => setIsbn(e.target.value)} placeholder="ISBN" />
          <button className="btn" type="button" onClick={onAutofill} disabled={autofillLoading}>
            {autofillLoading ? 'Recherche…' : 'OpenLibrary'}
          </button>
        </div>
        <input className="input" value={auteur} onChange={(e) => setAuteur(e.target.value)} placeholder="Auteur (optionnel)" />
        <input className="input" value={prix} onChange={(e) => setPrix(e.target.value)} placeholder="Prix CHF" />
        <input
          className="input"
          value={imageLink}
          onChange={(e) => setImageLink(e.target.value)}
          placeholder="Image URL (optionnel)"
        />
        <textarea
          className="card"
          style={{ borderRadius: 14, padding: 12, borderColor: 'var(--color-border)', minHeight: 120 }}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Description (optionnel)"
        />
        {error ? <div className="muted">{error}</div> : null}
        <button className="btn btnPrimary" type="submit" disabled={loading}>
          {loading ? 'Création…' : 'Créer'}
        </button>
      </form>
    </div>
  )
}
