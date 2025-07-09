# Contenu EXACT pour app/schemas.py

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# --- Schémas pour Document ---
class DocumentBase(BaseModel):
    nom_fichier: str

class Document(DocumentBase):
    id: int
    date_upload: datetime
    contenu_extrait: Optional[str] = None

    class Config:
        # Cette ligne est ancienne, Pydantic v2 utilise `from_attributes`
        # mais `orm_mode` est gardé pour la compatibilité.
        # Remplaçons par la nouvelle syntaxe pour être plus propre.
        from_attributes = True


# --- Schémas pour Matière ---
# La classe que l'erreur recherche est ICI
class MatiereBase(BaseModel):
    nom: str
    description: Optional[str] = None

class MatiereCreate(MatiereBase):
    pass

# ET SURTOUT CELLE-CI
class Matiere(MatiereBase):
    id: int
    date_creation: datetime
    documents: List[Document] = [] # Utilise la classe Document définie plus haut

    class Config:
        from_attributes = True