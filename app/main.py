from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.routes_posts import router as posts_router

app = FastAPI(title="Posts Service")

# Маршруты апишки и фронта
app.include_router(posts_router)

# Статика
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Шаблоны
templates = Jinja2Templates(directory="app/templates")

# Главная страница — перенаправление на список постов
from fastapi.responses import RedirectResponse
@app.get("/")
async def root():
    return RedirectResponse("/posts/")