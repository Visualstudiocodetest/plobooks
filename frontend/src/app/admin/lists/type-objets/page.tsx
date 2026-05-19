'use client'

import { useEffect, useState } from 'react'
import { apiFetch } from '@/services/api'
import { useAuth } from '@/components/auth/AuthProvider'

type TypeObjet = { id_type_objet: number; libelle: string; code?: string; description?: string }

export default function TypeObjetsAdmin() {
  const { isLoggedIn } = useAuth()
  const [list, setList] = useState<TypeObjet[]>([])
  const [libelle, setLibelle] = useState('')
  const [code, setCode] = useState('')

  async function load() {
    try {
      const r = await apiFetch<TypeObjet[]>('/catalog/type-objets')
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
      await apiFetch('/catalog/type-objets', { method: 'POST', auth: true, body: JSON.stringify({ libelle, code }) })
      setLibelle('')
      setCode('')
      await load()
    } catch (err) {
      console.error(err)
    }
  }

  async function remove(id: number) {
    if (!confirm('Supprimer ce type d\'objet ?')) return
    try {
      await apiFetch(`/catalog/type-objets/${id}`, { method: 'DELETE', auth: true })
      await load()
    } catch (err) {
      console.error(err)
    }
  }

  if (!isLoggedIn) return <div className="card">Connexion requise</div>

  return (
    <div style={{ display: 'grid', gap: 12 }}>
      <h2>Types d'objets</h2>
      <form onSubmit={createOne} style={{ display: 'flex', gap: 8 }}>
        <input placeholder="Libellé" value={libelle} onChange={(e) => setLibelle(e.target.value)} />
        <input placeholder="Code" value={code} onChange={(e) => setCode(e.target.value)} />
        <button className="btn btnPrimary" type="submit">Créer</button>
      </form>
      <div style={{ display: 'grid', gap: 8 }}>
        {list.map((c) => (
          <div key={c.id_type_objet} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <div style={{ fontWeight: 700 }}>{c.libelle} <span className="muted">{c.code}</span></div>
              <div className="muted">{c.description}</div>
            </div>
            <div>
              <button className="btn" onClick={() => remove(c.id_type_objet)}>Supprimer</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
