import pytest
from  infrastructure.db import SessionLocal

"""
Functional test: Book CRUD flow via API
"""
from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from  main import app

client = TestClient(app)

def test_book_crud_flow():
    # Register + login (writes require auth)
    user = {
        "nom": "Flow",
        "prenom": "User",
        "email": "flow@example.com",
        "mot_de_passe": "password123",
        "role": "user",
    }
    r = client.post("/auth/register", json=user)
    assert r.status_code in (201, 400), r.text
    token_resp = client.post("/auth/token", json={"username": user["email"], "password": user["mot_de_passe"]})
    assert token_resp.status_code == 200, token_resp.text
    token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create
    import uuid
    uniq = uuid.uuid4().hex[:10]
    payload = { # type: ignore
        "titre": "Flow Book",
        "isbn": f"FLOW_{uniq}",
        "auteur": "Flow Author",
        "editeur": "Flow Editor",
        "langue": "FR",
        "description": "Flow Desc",
        "image_link": "http://img.flow",
        "prix_chf": 30.0,
        "actif": True
    }
    r = client.post("/books/", json=payload, headers=headers)
    assert r.status_code == 201
    book = r.json()
    book_id = book["id_article"]
    # Update
    update = {"titre": "Flow Book Updated"}
    r = client.put(f"/books/{book_id}", json=update, headers=headers)
    assert r.status_code == 200
    assert r.json()["titre"] == "Flow Book Updated"
    # Delete
    r = client.delete(f"/books/{book_id}", headers=headers)
    assert r.status_code == 204
    # Get after delete
    r = client.get(f"/books/{book_id}")
    assert r.status_code == 404
