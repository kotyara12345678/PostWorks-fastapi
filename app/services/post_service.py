import httpx
from datetime import datetime
from app.core.database import posts_collection
from app.core.config import settings
from app.models.post_model import Post


async def create_post(post_data: dict) -> Post | None:
    user_id = post_data["user_id"]

    # Проверяем пользователя
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.USERS_SERVICE_URL}/users/{user_id}")
        if response.status_code != 200:
            return None  # пользователя нету

    # Создаём пост
    post_dict = {
        "user_id": user_id,
        "title": post_data["title"],
        "content": post_data["content"],
        "created_at": datetime.utcnow()
    }

    # Вставляем в монгу
    result = await posts_collection.insert_one(post_dict)

    # Преобразуем _id
    post_dict["id"] = str(result.inserted_id)

    # Возвращаем пост
    return Post(**post_dict)