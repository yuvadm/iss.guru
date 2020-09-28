from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .predictions import Predictions
from .utils import normalize_lat_lng

app = FastAPI()

app.mount("/static", StaticFiles(directory="iss/static"), name="static")

templates = Jinja2Templates(directory="iss/templates")


@app.get("/")
async def home(request: Request):
    preds = Predictions(34.7641, 32.0669, altitude=0, days=5).get_grouped_predictions()
    return templates.TemplateResponse(
        "index.html", {"request": request, "predictions": preds}
    )


@app.get("/passes/{lat}/{lng}")
async def passes(request: Request, lat: str, lng: str):
    lat, lng = normalize_lat_lng(lat, lng)
    preds = Predictions(lat, lng, altitude=0, days=5).get_grouped_predictions()
    return templates.TemplateResponse(
        "passes.html",
        {
            "request": request,
            "predictions": preds,
            "location": {"lat": lat, "lng": lng},
        },
    )
