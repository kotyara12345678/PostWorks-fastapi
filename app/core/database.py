import motor.motor_asyncio
from app.core.config import settings

# Подключение к монге
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
db = client.postsdb
posts_collection = db.posts