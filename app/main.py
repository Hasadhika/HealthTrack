
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from app.database import Base, engine
from app.routes import symptoms, insights

BASE_DIR = Path(__file__).resolve().parent

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HealthTrack API",
    description="Patient Symptom Tracking and AI-Assisted Insights",
    version="1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)

app.include_router(symptoms.router)
app.include_router(insights.router)



@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )



@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "HealthTrack"
    }
