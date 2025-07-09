# Contenu EXACT pour app/crud.py

import fitz  # PyMuPDF
from sqlalchemy.orm import Session
from . import models, schemas
import os
from fastapi import UploadFile

UPLOADS_DIR = "uploads"

# --- CRUD pour les Matières ---

def get_matiere(db: Session, matiere_id: int):
    return db.query(models.Matiere).filter(models.Matiere.id == matiere_id).first()

# CETTE FONCTION EST PROBABLEMENT CELLE QUI MANQUE
def get_matieres(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Matiere).order_by(models.Matiere.nom).offset(skip).limit(limit).all()

def create_matiere(db: Session, matiere: schemas.MatiereCreate):
    db_matiere = models.Matiere(nom=matiere.nom, description=matiere.description)
    db.add(db_matiere)
    db.commit()
    db.refresh(db_matiere)
    return db_matiere

# AJOUTER CETTE FONCTION DANS app/crud.py

def delete_matiere(db: Session, matiere_id: int):
    db_matiere = db.query(models.Matiere).filter(models.Matiere.id == matiere_id).first()
    if db_matiere:
        db.delete(db_matiere)
        db.commit()
    return db_matiere

# AJOUTER CETTE FONCTION DANS app/crud.py

def update_matiere(db: Session, matiere_id: int, nom: str, description: str):
    db_matiere = db.query(models.Matiere).filter(models.Matiere.id == matiere_id).first()
    if db_matiere:
        db_matiere.nom = nom
        db_matiere.description = description
        db.commit()
        db.refresh(db_matiere)
# --- Logique pour les Documents ---

def save_document_and_extract_text(db: Session, matiere_id: int, file: UploadFile):
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    
    file_path = os.path.join(UPLOADS_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        # Important: il faut rembobiner le fichier avant de le lire pour le sauvegarder
        file.file.seek(0)
        buffer.write(file.file.read())

    extracted_text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                extracted_text += page.get_text("text")
    except Exception as e:
        print(f"Erreur d'extraction de texte pour {file.filename}: {e}")

    db_document = models.Document(
        nom_fichier=file.filename,
        contenu_extrait=extracted_text,
        id_matiere=matiere_id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document