from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from  infrastructure import models
from  infrastructure.crud_base import CrudBase
from  presentation.deps import get_current_user, get_db
from  presentation.schemas import (
    CommandeCreate,
    CommandeRead,
    CommandeUpdate,
    LigneCommandeCreate,
    LigneCommandeRead,
    LigneCommandeUpdate,
    PaiementCreate,
    PaiementRead,
    PaiementUpdate,
)

router = APIRouter(prefix="/orders", tags=["orders"])

commande_crud = CrudBase[models.Commande](models.Commande, "id_commande")
ligne_crud = CrudBase[models.LigneCommande](models.LigneCommande, "id_ligne_commande")
paiement_crud = CrudBase[models.Paiement](models.Paiement, "id_paiement")


def _get_commande_owned(db: Session, id_commande: int, id_utilisateur: int) -> models.Commande | None:
    return (
        db.query(models.Commande)
        .filter(models.Commande.id_commande == id_commande, models.Commande.id_utilisateur == id_utilisateur)
        .first()
    )


@router.get("/commandes", response_model=list[CommandeRead])
def list_commandes(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(models.Commande).filter(models.Commande.id_utilisateur == current_user.id_utilisateur).all()


@router.get("/commandes/{id_commande}", response_model=CommandeRead)
def get_commande(id_commande: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = _get_commande_owned(db, id_commande, int(current_user.id_utilisateur))
    if obj is None:
        raise HTTPException(status_code=404, detail="Commande not found")
    return obj


@router.post("/commandes", response_model=CommandeRead, status_code=status.HTTP_201_CREATED)
def create_commande(payload: CommandeCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = models.Commande(id_utilisateur=current_user.id_utilisateur, **payload.model_dump())
    return commande_crud.create(db, obj)


@router.put("/commandes/{id_commande}", response_model=CommandeRead)
def update_commande(
    id_commande: int,
    payload: CommandeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    obj = _get_commande_owned(db, id_commande, int(current_user.id_utilisateur))
    if obj is None:
        raise HTTPException(status_code=404, detail="Commande not found")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/commandes/{id_commande}", status_code=status.HTTP_204_NO_CONTENT)
def delete_commande(id_commande: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = _get_commande_owned(db, id_commande, int(current_user.id_utilisateur))
    if obj is None:
        raise HTTPException(status_code=404, detail="Commande not found")
    db.delete(obj)
    db.commit()
    return None


@router.get("/lignes", response_model=list[LigneCommandeRead])
def list_lignes(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return (
        db.query(models.LigneCommande)
        .join(models.Commande, models.LigneCommande.id_commande == models.Commande.id_commande)
        .filter(models.Commande.id_utilisateur == current_user.id_utilisateur)
        .all()
    )


@router.get("/lignes/{id_ligne_commande}", response_model=LigneCommandeRead)
def get_ligne(id_ligne_commande: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = (
        db.query(models.LigneCommande)
        .join(models.Commande, models.LigneCommande.id_commande == models.Commande.id_commande)
        .filter(
            models.LigneCommande.id_ligne_commande == id_ligne_commande,
            models.Commande.id_utilisateur == current_user.id_utilisateur,
        )
        .first()
    )
    if obj is None:
        raise HTTPException(status_code=404, detail="LigneCommande not found")
    return obj


@router.post("/lignes", response_model=LigneCommandeRead, status_code=status.HTTP_201_CREATED)
def create_ligne(payload: LigneCommandeCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if _get_commande_owned(db, payload.id_commande, int(current_user.id_utilisateur)) is None:
        raise HTTPException(status_code=404, detail="Commande not found")
    obj = models.LigneCommande(**payload.model_dump())
    return ligne_crud.create(db, obj)


@router.put("/lignes/{id_ligne_commande}", response_model=LigneCommandeRead)
def update_ligne(
    id_ligne_commande: int,
    payload: LigneCommandeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    obj = (
        db.query(models.LigneCommande)
        .join(models.Commande, models.LigneCommande.id_commande == models.Commande.id_commande)
        .filter(
            models.LigneCommande.id_ligne_commande == id_ligne_commande,
            models.Commande.id_utilisateur == current_user.id_utilisateur,
        )
        .first()
    )
    if obj is None:
        raise HTTPException(status_code=404, detail="LigneCommande not found")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/lignes/{id_ligne_commande}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ligne(id_ligne_commande: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = (
        db.query(models.LigneCommande)
        .join(models.Commande, models.LigneCommande.id_commande == models.Commande.id_commande)
        .filter(
            models.LigneCommande.id_ligne_commande == id_ligne_commande,
            models.Commande.id_utilisateur == current_user.id_utilisateur,
        )
        .first()
    )
    if obj is None:
        raise HTTPException(status_code=404, detail="LigneCommande not found")
    db.delete(obj)
    db.commit()
    return None


@router.get("/paiements", response_model=list[PaiementRead])
def list_paiements(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return (
        db.query(models.Paiement)
        .join(models.Commande, models.Paiement.id_commande == models.Commande.id_commande)
        .filter(models.Commande.id_utilisateur == current_user.id_utilisateur)
        .all()
    )


@router.get("/paiements/{id_paiement}", response_model=PaiementRead)
def get_paiement(id_paiement: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = (
        db.query(models.Paiement)
        .join(models.Commande, models.Paiement.id_commande == models.Commande.id_commande)
        .filter(models.Paiement.id_paiement == id_paiement, models.Commande.id_utilisateur == current_user.id_utilisateur)
        .first()
    )
    if obj is None:
        raise HTTPException(status_code=404, detail="Paiement not found")
    return obj


@router.post("/paiements", response_model=PaiementRead, status_code=status.HTTP_201_CREATED)
def create_paiement(payload: PaiementCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if _get_commande_owned(db, payload.id_commande, int(current_user.id_utilisateur)) is None:
        raise HTTPException(status_code=404, detail="Commande not found")
    obj = models.Paiement(**payload.model_dump())
    return paiement_crud.create(db, obj)


@router.put("/paiements/{id_paiement}", response_model=PaiementRead)
def update_paiement(
    id_paiement: int,
    payload: PaiementUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    obj = (
        db.query(models.Paiement)
        .join(models.Commande, models.Paiement.id_commande == models.Commande.id_commande)
        .filter(models.Paiement.id_paiement == id_paiement, models.Commande.id_utilisateur == current_user.id_utilisateur)
        .first()
    )
    if obj is None:
        raise HTTPException(status_code=404, detail="Paiement not found")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/paiements/{id_paiement}", status_code=status.HTTP_204_NO_CONTENT)
def delete_paiement(id_paiement: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = (
        db.query(models.Paiement)
        .join(models.Commande, models.Paiement.id_commande == models.Commande.id_commande)
        .filter(models.Paiement.id_paiement == id_paiement, models.Commande.id_utilisateur == current_user.id_utilisateur)
        .first()
    )
    if obj is None:
        raise HTTPException(status_code=404, detail="Paiement not found")
    db.delete(obj)
    db.commit()
    return None

