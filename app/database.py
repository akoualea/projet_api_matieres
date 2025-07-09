# Contenu FINAL et LOCAL pour app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# On remet en dur l'URL de votre base de données MySQL locale.
# Assurez-vous que ces informations sont correctes pour votre XAMPP.
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@127.0.0.1/gestion_matieres_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()