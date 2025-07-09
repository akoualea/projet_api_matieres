# Contenu DÉFINITIF et SIMPLIFIÉ pour app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# On récupère l'URL de la base de données DEPUIS la variable d'environnement.
# C'est Render qui va fournir cette variable.
# Si la variable n'existe pas, le programme plantera, ce qui est MIEUX
# que d'essayer de se connecter à une mauvaise base de données.
DATABASE_URL = os.environ.get("DATABASE_URL")

# On s'assure de remplacer le préfixe de Heroku/Render pour SQLAlchemy
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Si DATABASE_URL n'a pas été trouvé, le create_engine plantera, ce qui est bien.
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()