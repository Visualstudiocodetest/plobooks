from __future__ import annotations

import hashlib

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from infrastructure import models
from infrastructure.crud_base import CrudBase
from presentation.deps import get_db, require_admin, require_user


router = APIRouter(prefix="/users", tags=["users"])

user_crud = CrudBase[models.Utilisateur](models.Utilisateur, "id_utilisateur")


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


@router.get("/", response_model=list[dict])
def list_users(db: Session = Depends(get_db), _admin=Depends(require_admin)):
    # Keep output minimal: no password hash
    users = user_crud.list(db)
    return [
        {
            "id_utilisateur": int(u.id_utilisateur),
            "nom": u.nom,
            "prenom": u.prenom,
            "email": u.email,
            "role": u.role,
        }
        for u in users
    ]


@router.get("/{id_utilisateur}", response_model=dict)
def get_user(id_utilisateur: int, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    u = user_crud.get(db, id_utilisateur)
    if u is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id_utilisateur": int(u.id_utilisateur),
        "nom": u.nom,
        "prenom": u.prenom,
        "email": u.email,
        "role": u.role,
    }


@router.delete("/{id_utilisateur}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id_utilisateur: int, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    if not user_crud.delete(db, id_utilisateur):
        raise HTTPException(status_code=404, detail="User not found")
    return None

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: dict, db: Session = Depends(get_db)):
    user = models.Utilisateur(
        nom=user["nom"],
        prenom=user["prenom"],
        email=user["email"],
        mot_de_passe=_hash_password(user["mot_de_passe"]),
        role=user.get("role", "user"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "id_utilisateur": int(user.id_utilisateur),
        "nom": user.nom,
        "prenom": user.prenom,
        "email": user.email,
        "role": user.role,
    }
@router.put("/{id_utilisateur}")
def update_user(id_utilisateur: int, user_update: dict, db: Session = Depends
    (get_db), _admin=Depends(require_user)):
    user = user_crud.get(db, id_utilisateur)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for field in ["nom", "prenom", "email", "role"]:
        if field in user_update:
            setattr(user, field, user_update[field])
    if "mot_de_passe" in user_update:
        user.mot_de_passe = _hash_password(user_update["mot_de_passe"])
    db.commit()
    db.refresh(user)
    return {
        "id_utilisateur": int(user.id_utilisateur),
        "nom": user.nom,
        "prenom": user.prenom,
        "email": user.email,
        "role": user.role,
    }

