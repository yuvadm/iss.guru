import json

from fastapi import FastAPI, Request, Header
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional

from .geo import get_location
from .predictions import Predictions

app = FastAPI()

app.mount("/static", StaticFiles(directory="iss/static"), name="static")

templates = Jinja2Templates(directory="iss/templates")


@app.get("/")
async def home(request: Request, cf_connecting_ip: Optional[str] = Header(None)):
    client_ip = cf_connecting_ip or request.client.host
    location = get_location(client_ip)
    # preds = Predictions(lat, lng, tz=tz, altitude=0, days=5).get_grouped_predictions()
    return templates.TemplateResponse(
        "index.html", {"request": request, "location": location}
    )


@app.get("/passes/{lat}/{lng}")
async def passes(request: Request, lat: float, lng: float):
    preds = Predictions(lat, lng, altitude=0, days=5).get_predictions()
    return templates.TemplateResponse(
        "passes.html",
        {
            "request": request,
            "predictions_json": json.dumps(preds),
            "location": {"lat": lat, "lng": lng},
        },
    )
