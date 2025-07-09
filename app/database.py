# Contenu pour app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ATTENTION : Mettez à jour cette ligne avec vos propres informations de connexion MySQL
# Format : "mysql+pymysql://UTILISATEUR:MOT_DE_PASSE@HOTE:PORT/NOM_DE_LA_BDD"
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/gestion_matieres_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dépendance pour obtenir une session de BDD dans les routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()