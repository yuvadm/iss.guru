from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .predictions import Predictions

app = FastAPI()

app.mount("/static", StaticFiles(directory="iss/static"), name="static")

templates = Jinja2Templates(directory="iss/templates")


@app.get("/")
async def home(request: Request):
    preds = Predictions(34.7641, 32.0669, altitude=10).get_predictions()
    return templates.TemplateResponse(
        "index.html", {"request": request, "predictions": preds}
    )
