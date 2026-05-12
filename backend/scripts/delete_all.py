"""
Delete all data from all main tables (for dev/test reset only!).
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from  infrastructure.db import SessionLocal
from sqlalchemy import text as string

def delete_all():
    db = SessionLocal()
    db.execute(string("SET FOREIGN_KEY_CHECKS=0;")) # type: ignore
    db.execute(string("DELETE FROM scan_isbn;")) # type: ignore
    db.execute(string("DELETE FROM paiement;")) # type: ignore
    db.execute(string("DELETE FROM ligne_commande;")) # type: ignore
    db.execute(string("DELETE FROM commande;")) # type: ignore
    db.execute(string("DELETE FROM stock;")) # type: ignore
    db.execute(string("DELETE FROM article_categorie;")) # type: ignore
    db.execute(string("DELETE FROM livre;")) # type: ignore
    db.execute(string("DELETE FROM article;")) # type: ignore
    db.execute(string("DELETE FROM utilisateur;")) # type: ignore
    db.execute(string("DELETE FROM source_stock;")) # type: ignore
    db.execute(string("DELETE FROM categorie;")) # type: ignore
    db.execute(string("DELETE FROM etat_usure;")) # type: ignore
    db.execute(string("DELETE FROM type_objet;")) # type: ignore
    db.execute(string("SET FOREIGN_KEY_CHECKS=1;")) # type: ignore
    db.commit()
    db.close()

if __name__ == "__main__":
    delete_all()
