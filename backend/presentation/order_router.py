from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

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


def _finalize_commande(db: Session, id_commande: int):
    # For each ligne in the commande, finalize reserved stock into sold stock
    lignes = db.query(models.LigneCommande).filter(models.LigneCommande.id_commande == id_commande).all()
    for l in lignes:
        # find stock rows for the article
        stocks = (
            db.query(models.Stock)
            .filter(models.Stock.id_article == l.id_article)
            .order_by(models.Stock.id_stock.asc())
            .with_for_update()
            .all()
        )
        if not stocks:
            # nothing to do if no stock rows exist
            continue
        remaining = l.quantite
        # first reduce reserved counts where possible
        for s in stocks:
            if remaining <= 0:
                break
            reserve = s.quantite_reservee or 0
            take_from_reserve = min(reserve, remaining)
            if take_from_reserve > 0:
                s.quantite_reservee = reserve - take_from_reserve
                remaining -= take_from_reserve
        # if still remaining, deduct from available quantities
        for s in stocks:
            if remaining <= 0:
                break
            avail = s.quantite_disponible or 0
            take = min(avail, remaining)
            if take <= 0:
                continue
            s.quantite_disponible = avail - take
            remaining -= take
    # mark articles inactive if no stock left
    art_ids = [a.id_article for a in db.query(models.Article).all()]
    for aid in art_ids:
        total_left = (
            db.query(models.Stock)
            .filter(models.Stock.id_article == aid)
            .with_entities(func.sum(models.Stock.quantite_disponible))
            .scalar()
        )
        if not total_left:
            art = db.query(models.Article).filter(models.Article.id_article == aid).first()
            if art:
                art.actif = False


def _refund_commande(db: Session, id_commande: int):
    # When refunding, return sold quantities back to stock
    lignes = db.query(models.LigneCommande).filter(models.LigneCommande.id_commande == id_commande).all()
    for l in lignes:
        stocks = (
            db.query(models.Stock)
            .filter(models.Stock.id_article == l.id_article)
            .order_by(models.Stock.id_stock.asc())
            .with_for_update()
            .all()
        )
        if not stocks:
            continue
        remaining = l.quantite
        # add back to first stock rows
        for s in stocks:
            if remaining <= 0:
                break
            s.quantite_disponible = (s.quantite_disponible or 0) + remaining
            remaining = 0
    # reactivate articles that have stock
    for aid in {l.id_article for l in lignes}:
        total_left = (
            db.query(models.Stock)
            .filter(models.Stock.id_article == aid)
            .with_entities(func.sum(models.Stock.quantite_disponible))
            .scalar()
        )
        if total_left and total_left > 0:
            art = db.query(models.Article).filter(models.Article.id_article == aid).first()
            if art:
                art.actif = True


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
    try:
        # Lock stock rows for this article to prevent concurrent reservations
        stocks = (
            db.query(models.Stock)
            .filter(models.Stock.id_article == payload.id_article)
            .order_by(models.Stock.id_stock.asc())
            .with_for_update()
            .all()
        )

        if stocks:
            # compute total available (available = quantite_disponible - quantite_reservee)
            total_available = sum((s.quantite_disponible or 0) - (s.quantite_reservee or 0) for s in stocks)
            if payload.quantite > total_available:
                raise HTTPException(status_code=400, detail="Not enough stock")

            # reserve across stock sources
            remaining = payload.quantite
            for s in stocks:
                if remaining <= 0:
                    break
                avail = (s.quantite_disponible or 0) - (s.quantite_reservee or 0)
                take = min(avail, remaining)
                if take <= 0:
                    continue
                s.quantite_reservee = (s.quantite_reservee or 0) + take
                remaining -= take

        # create the ligne and commit once (for articles without stock rows, we allow creation)
        obj = models.LigneCommande(**payload.model_dump())
        db.add(obj)

        # If article now out of stock, mark inactive
        if stocks:
            total_left = sum((s.quantite_disponible or 0) - (s.quantite_reservee or 0) for s in stocks)
            if total_left <= 0:
                art = db.query(models.Article).filter(models.Article.id_article == payload.id_article).first()
                if art:
                    art.actif = False

        db.commit()
        db.refresh(obj)
        return obj
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not create ligne") from e


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
    created = paiement_crud.create(db, obj)
    # finalize immediately if payment is captured/paid
    try:
        if created.statut and created.statut.upper() in ("CAPTURED", "PAID", "COMPLETED"):
            _finalize_commande(db, created.id_commande)
            db.commit()
    except Exception:
        # don't fail payment creation on finalization errors
        db.rollback()
    return created


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
    prev_stat = obj.statut
    for k, v in data.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    # handle statut transitions
    new_stat = getattr(obj, "statut", None)
    try:
        if prev_stat is None or prev_stat.upper() not in ("CAPTURED", "PAID", "COMPLETED"):
            if new_stat and new_stat.upper() in ("CAPTURED", "PAID", "COMPLETED"):
                _finalize_commande(db, obj.id_commande)
                db.commit()
        # refund transition
        if prev_stat and prev_stat.upper() in ("CAPTURED", "PAID", "COMPLETED") and new_stat and new_stat.upper() == "REFUNDED":
            _refund_commande(db, obj.id_commande)
            db.commit()
    except Exception:
        db.rollback()

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

