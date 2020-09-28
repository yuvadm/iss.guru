from fastapi import FastAPI, Request, Response, Header
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional

from .predictions import Predictions

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
async def passes(request: Request, lat: float, lng: float):
    preds = Predictions(lat, lng, altitude=0, days=5).get_grouped_predictions()
    return templates.TemplateResponse(
        "passes.html",
        {
            "request": request,
            "predictions": preds,
            "location": {"lat": lat, "lng": lng},
        },
    )


@app.get("/ip")
async def ip(request: Request, cf_connecting_ip: Optional[str] = Header(None)):
    return Response(cf_connecting_ip or request.client.host)
