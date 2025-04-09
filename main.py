from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routes import produto_routes, usuario_routes

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(produto_routes.router)
app.include_router(usuario_routes.router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

