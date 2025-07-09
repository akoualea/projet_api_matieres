# Contenu COMPLET et VÉRIFIÉ pour app/routers/web.py

# --- Imports ---
from fastapi import APIRouter, Depends, Request, HTTPException, Form 
from typing import Optional
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .. import crud
from ..database import get_db

# --- Configuration ---
# C'est ici qu'on crée la variable "router" que l'erreur recherche
router = APIRouter(
    prefix="/web",
    tags=["Interface Web (HTML)"],
    include_in_schema=False 
)

templates = Jinja2Templates(directory="templates")

# --- Routes ---

@router.get("/", response_class=HTMLResponse, name="home")
def home(request: Request, db: Session = Depends(get_db)):
    matieres = crud.get_matieres(db)
    return templates.TemplateResponse("index.html", {"request": request, "matieres": matieres})

@router.get("/matieres/{matiere_id}", response_class=HTMLResponse, name="matiere_detail")
def matiere_detail(request: Request, matiere_id: int, db: Session = Depends(get_db)):
    matiere = crud.get_matiere(db, matiere_id=matiere_id)
    if not matiere:
        raise HTTPException(status_code=404, detail="Matière non trouvée")
    return templates.TemplateResponse("matiere_detail.html", {"request": request, "matiere": matiere})

@router.get("/matieres/{matiere_id}/edit", response_class=HTMLResponse, name="update_matiere_form")
def show_update_matiere_form(request: Request, matiere_id: int, db: Session = Depends(get_db)):
    matiere = crud.get_matiere(db, matiere_id=matiere_id)
    if not matiere:
        raise HTTPException(status_code=404, detail="Matière non trouvée")
    return templates.TemplateResponse("update_matiere.html", {"request": request, "matiere": matiere})

@router.post("/matieres/{matiere_id}/edit", name="update_matiere_submit")
def handle_update_matiere_form(
    request: Request,
    matiere_id: int,
    nom: str = Form(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    crud.update_matiere(db=db, matiere_id=matiere_id, nom=nom, description=description)
    return RedirectResponse(url=router.url_path_for("matiere_detail", matiere_id=matiere_id), status_code=303)

@router.post("/matieres/{matiere_id}/delete", name="delete_matiere_web")
def delete_matiere_web(matiere_id: int, db: Session = Depends(get_db)):
    crud.delete_matiere(db, matiere_id=matiere_id)
    return RedirectResponse(url=router.url_path_for("home"), status_code=303)