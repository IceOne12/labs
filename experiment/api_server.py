from fastapi import FastAPI
from pymongo import MongoClient
import psycopg2
import psycopg2.extras

app = FastAPI()

# Конфигурация подключения
POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "social_network",
    "user": "postgres",
    "password": "postgres"   
}
MONGO_URI = "mongodb://localhost:27017/"


@app.get("/api/posts/{post_id}")
async def get_post(post_id: int):
    """Гибридная модель: получение поста с комментариями из MongoDB"""
    client = MongoClient(MONGO_URI)
    post = client.social_network.posts.find_one({"post_id": post_id}, {"_id": 0})
    client.close()
    return {"data": post}


@app.get("/api/posts/{post_id}/relational")
async def get_post_relational(post_id: int):
    """
    Реляционная модель: получение поста с комментариями через JOIN
    """
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()
    
    try:
        # Получаем пост
        cursor.execute("""
            SELECT id, author_id, content, created_at 
            FROM posts_relational 
            WHERE id = %s
        """, (post_id,))
        post = cursor.fetchone()
        
        if not post:
            return {"error": "Post not found"}
        
        # Получаем комментарии с именами авторов
        cursor.execute("""
            SELECT c.id, c.content, c.created_at, u.name as author_name
            FROM comments_relational c
            JOIN users u ON c.author_id = u.id
            WHERE c.post_id = %s
            ORDER BY c.created_at DESC
            LIMIT 50
        """, (post_id,))
        comments = cursor.fetchall()
        
        return {
            "post": {
                "id": post[0],
                "author_id": post[1],
                "content": post[2],
                "created_at": str(post[3])
            },
            "comments": [
                {
                    "id": c[0],
                    "content": c[1],
                    "created_at": str(c[2]),
                    "author_name": c[3]
                }
                for c in comments
            ]
        }
        
    finally:
        cursor.close()
        conn.close()


@app.get("/api/feed")
async def get_feed(user_id: int = 1, limit: int = 20):
    """Получение ленты (посты друзей)"""
    # Получаем друзей из PostgreSQL
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT friend_id FROM friends WHERE user_id = %s
        UNION
        SELECT user_id FROM friends WHERE friend_id = %s
    """, (user_id, user_id))
    friends = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    
    if not friends:
        return {"posts": []}
    
    # Получаем посты друзей из MongoDB
    client = MongoClient(MONGO_URI)
    posts = list(client.social_network.posts.find(
        {"author_id": {"$in": friends}},
        {"_id": 0}
    ).sort("created_at", -1).limit(limit))
    client.close()
    
    return {"posts": posts}


@app.get("/api/users/{user_id}/friends")
async def get_friends(user_id: int):
    """Получение списка друзей (реляционная модель)"""
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT friend_id FROM friends WHERE user_id = %s
        UNION
        SELECT user_id FROM friends WHERE friend_id = %s
    """, (user_id, user_id))
    friends = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return {"friends": friends}


@app.post("/api/posts/{post_id}/like")
async def like_post(post_id: int, user_id: int = 1):
    """Добавление лайка"""
    client = MongoClient(MONGO_URI)
    result = client.social_network.posts.update_one(
        {"post_id": post_id},
        {"$addToSet": {"likes": user_id}}
    )
    client.close()
    return {"success": result.modified_count > 0}


@app.get("/api/health")
async def health():
    return {"status": "ok"}
