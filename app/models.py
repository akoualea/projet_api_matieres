# Contenu FINAL et CORRIGÉ pour app/models.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


# --- PREMIÈRE CLASSE : MATIERE ---
class Matiere(Base):
    __tablename__ = "matieres"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    date_creation = Column(DateTime(timezone=True), server_default=func.now()) 

    # --- CORRECTION DE LA FAUTE DE FRAPPE ICI ---
    documents = relationship("Document", back_populates="matiere", cascade="all, delete-orphan")


# --- DEUXIÈME CLASSE : DOCUMENT ---
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    nom_fichier = Column(String(255), nullable=False)
    contenu_extrait = Column(Text, nullable=True)
    date_upload = Column(DateTime(timezone=True), server_default=func.now())
    
    id_matiere = Column(Integer, ForeignKey("matieres.id"), nullable=False)

    matiere = relationship("Matiere", back_populates="documents")