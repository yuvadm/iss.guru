from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="iss/templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})
