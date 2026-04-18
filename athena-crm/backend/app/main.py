from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
import os

from app.core.config import settings
from app.core.logging import logger
from app.infrastructure.database.connection import create_tables
from app.api.v1.routers import cards, clients, actions, dashboard, performance, etl, sellers, cycles

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Athena CRM — Churn Management Suite\n\n"
        "API para controle de fluxo de churn, gestão de cards Kanban, "
        "indicadores de risco e ingestão de dados via ETL.\n\n"
        "Desenvolvido pela **O2 Data**."
    ),
    docs_url="/docs",
    redoc_url=None,   # disable default — we serve a custom one below
)

# ── CORS — all origins ────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(sellers.router, prefix="/api/v1")
app.include_router(clients.router, prefix="/api/v1")
app.include_router(cards.router, prefix="/api/v1")
app.include_router(actions.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(performance.router, prefix="/api/v1")
app.include_router(etl.router, prefix="/api/v1")
app.include_router(cycles.router, prefix="/api/v1")

# ── Custom ReDoc (self-contained, no external CDN dependency) ─────────────────
@app.get("/redoc", include_in_schema=False)
def redoc_html():
    return HTMLResponse("""<!DOCTYPE html>
<html>
<head>
  <title>Athena CRM — API Docs</title>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
  <style>body { margin: 0; padding: 0; }</style>
</head>
<body>
  <redoc spec-url='/openapi.json'></redoc>
  <script src="https://cdn.jsdelivr.net/npm/redoc@2.1.3/bundles/redoc.standalone.js"></script>
</body>
</html>""")

# ── Static Frontend ───────────────────────────────────────────────────────────
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/", include_in_schema=False)
    def serve_frontend():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# ── Startup ───────────────────────────────────────────────────────────────────
@app.on_event("startup")
def on_startup():
    logger.info("Starting Athena CRM...")
    create_tables()
    logger.info("Database tables ready.")
    logger.info(f"Docs:   http://localhost:8000/docs")
    logger.info(f"ReDoc:  http://localhost:8000/redoc")
    logger.info(f"OpenAPI: http://localhost:8000/openapi.json")


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}
