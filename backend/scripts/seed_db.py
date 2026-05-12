#Seed Db

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from  infrastructure.db import SessionLocal
from  infrastructure.models import Article, Livre
from datetime import date

def seed_db():
    db = SessionLocal()
    article1 = Article(
        id_type_objet=1,
        id_etat_usure=1,
        sku="1234567890",
        titre="Seed Book 1",
        description="Description for Seed Book 1",
        image_link="http://example.com/seed_book_1.jpg",
        prix_chf=10.0,
        actif=True,
    )
    db.add(article1)
    db.flush()  # Get id_article
    livre1 = Livre(
        id_article=article1.id_article,
        isbn="1234567890",
        auteur="Seed Author 1",
        editeur="Seed Editor 1",
        date_publication=date(2020, 1, 1),
        langue="FR",
    )
    db.add(livre1)
    db.commit()
    db.close()