'use client'

import { useEffect, useState } from 'react'
import { apiFetch } from '@/services/api'
import { useAuth } from '@/components/auth/AuthProvider'

type Categorie = { id_categorie: number; libelle: string; description?: string }

export default function CategoriesAdmin() {
  const { isLoggedIn } = useAuth()
  const [list, setList] = useState<Categorie[]>([])
  const [libelle, setLibelle] = useState('')
  const [description, setDescription] = useState('')

  async function load() {
    try {
      const r = await apiFetch<Categorie[]>('/catalog/categories')
      setList(r)
    } catch (e) {
      console.error(e)
    }
  }

  useEffect(() => {
    load()
  }, [])

  async function createOne(e: React.FormEvent) {
    e.preventDefault()
    try {
      await apiFetch('/catalog/categories', { method: 'POST', auth: true, body: JSON.stringify({ libelle, description }) })
      setLibelle('')
      setDescription('')
      await load()
    } catch (err) {
      console.error(err)
    }
  }

  async function remove(id: number) {
    if (!confirm('Supprimer cette catégorie ?')) return
    try {
      await apiFetch(`/catalog/categories/${id}`, { method: 'DELETE', auth: true })
      await load()
    } catch (err) {
      console.error(err)
    }
  }

  if (!isLoggedIn) return <div className="card">Connexion requise</div>

  return (
    <div style={{ display: 'grid', gap: 12 }}>
      <h2>Catégories</h2>
      <form onSubmit={createOne} style={{ display: 'flex', gap: 8 }}>
        <input placeholder="Libellé" value={libelle} onChange={(e) => setLibelle(e.target.value)} />
        <input placeholder="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
        <button className="btn btnPrimary" type="submit">Créer</button>
      </form>
      <div style={{ display: 'grid', gap: 8 }}>
        {list.map((c) => (
          <div key={c.id_categorie} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <div style={{ fontWeight: 700 }}>{c.libelle}</div>
              <div className="muted">{c.description}</div>
            </div>
            <div>
              <button className="btn" onClick={() => remove(c.id_categorie)}>Supprimer</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
