# Contenu CORRIGÉ et COMPLET pour app/routers/api.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.responses import RedirectResponse

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api",
    tags=["API (JSON)"],
)

# Route pour créer une matière (depuis le formulaire web)
@router.post(
    "/matieres/",
    response_model=schemas.Matiere,
    include_in_schema=False,
    name="create_matiere_from_web_form" # Nom ajouté pour url_for
)
def create_matiere_from_web_form(
    nom: str = Form(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    matiere_create = schemas.MatiereCreate(nom=nom, description=description)
    crud.create_matiere(db=db, matiere=matiere_create)
    # On redirige vers la page d'accueil de l'interface web
    return RedirectResponse(url="/web", status_code=303)


# --- Les routes pour l'API "pure" (pour Postman, etc.) ---

@router.get("/matieres/", response_model=List[schemas.Matiere])
def read_matieres_api(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère la liste de toutes les matières."""
    return crud.get_matieres(db, skip=skip, limit=limit)

@router.get("/matieres/{matiere_id}", response_model=schemas.Matiere)
def read_matiere_api(matiere_id: int, db: Session = Depends(get_db)):
    """Récupère une matière par son ID."""
    db_matiere = crud.get_matiere(db, matiere_id=matiere_id)
    if db_matiere is None:
        raise HTTPException(status_code=404, detail="Matière non trouvée")
    return db_matiere


# --- LA ROUTE CORRIGÉE POUR L'UPLOAD ---
# C'est la fusion de vos deux tentatives
@router.post(
    "/matieres/{matiere_id}/documents/",
    response_model=schemas.Document,
    include_in_schema=False,
    name="upload_document_from_web_form" # Nom ajouté pour url_for
)
def upload_document_from_web_form(
    matiere_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Gère l'upload d'un fichier PDF depuis le formulaire web."""
    db_matiere = crud.get_matiere(db, matiere_id=matiere_id)
    if not db_matiere:
        raise HTTPException(status_code=404, detail="Matière non trouvée pour l'upload")
    
    if not file.filename or not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers PDF sont autorisés")
    
    crud.save_document_and_extract_text(db=db, matiere_id=matiere_id, file=file)
    # On redirige vers la page de détail de la matière après l'upload
    return RedirectResponse(url=f"/web/matieres/{matiere_id}", status_code=303)