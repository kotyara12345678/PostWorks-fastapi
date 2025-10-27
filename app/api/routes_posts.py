from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.post_service import create_post
from app.core.database import posts_collection
from app.models.post_model import Post
from bson.objectid import ObjectId

router = APIRouter(prefix="/posts", tags=["Posts"])
templates = Jinja2Templates(directory="app/templates")


#страница создания поста
@router.get("/create")
async def create_post_page(request: Request):
    return templates.TemplateResponse("create_post.html", {"request": request})


#обработка формы создания поста
@router.post("/create")
async def create_post_form(
    request: Request,
    user_id: str = Form(...),
    title: str = Form(...),
    content: str = Form(...)
):
    post_data = {"user_id": user_id, "title": title, "content": content}
    post: Post = await create_post(post_data)
    if not post:
        return templates.TemplateResponse(
            "create_post.html",
            {
                "request": request,
                "error": "Пользователь не найден",
                "user_id": user_id,
                "title": title,
                "content": content
            }
        )
    return RedirectResponse("/posts/", status_code=303)


#список ВСЕХ постов
@router.get("/")
async def list_posts(request: Request):
    posts_cursor = posts_collection.find().sort("created_at", -1)
    posts_list = await posts_cursor.to_list(length=100)

    # Преобразуем монго документы в объекты Post
    posts = []
    for p in posts_list:
        post_dict = {
            "id": str(p["_id"]),
            "user_id": p.get("user_id"),
            "title": p.get("title"),
            "content": p.get("content"),
            "created_at": p.get("created_at")
        }
        posts.append(Post(**post_dict))

    return templates.TemplateResponse("posts_list.html", {"request": request, "posts": posts})


#страница ОТДЕЛЬНОГО поста по ID
@router.get("/{post_id}")
async def post_detail(request: Request, post_id: str):
    try:
        post_data = await posts_collection.find_one({"_id": ObjectId(post_id)})
        if not post_data:
            raise ValueError("Пост не найден")

        post_dict = {
            "id": str(post_data["_id"]),
            "user_id": post_data.get("user_id"),
            "title": post_data.get("title"),
            "content": post_data.get("content"),
            "created_at": post_data.get("created_at")
        }
        post = Post(**post_dict)

    except Exception:
        return templates.TemplateResponse(
            "posts_list.html",
            {"request": request, "posts": [], "error": "Пост не найден"}
        )

    return templates.TemplateResponse("post_detail.html", {"request": request, "post": post})