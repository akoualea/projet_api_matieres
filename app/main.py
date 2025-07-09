# Contenu pour app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from .database import engine, Base
from .routers import api, web

# Crée les tables dans la base de données au démarrage (si elles n'existent pas)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gestion de Matières Scolaires",
    description="Une API pour gérer des matières et leurs documents PDF, avec une interface web.",
    version="1.0.0"
)

# Monter le dossier static pour servir le CSS, JS, etc.

app.mount("/static", StaticFiles(directory="static"), name="static")

# Inclure les routeurs de l'API et de l'interface web
app.include_router(api.router)
app.include_router(web.router)

# Route racine qui redirige vers l'interface web
@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/web")