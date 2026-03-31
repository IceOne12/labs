"""
Генерация синтетических данных для эксперимента.
Запускать один раз перед тестированием.
"""

import random
import psycopg2
from pymongo import MongoClient
from datetime import datetime
import os
import sys

# ========== КОНФИГУРАЦИЯ ==========
POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "postgres",  
    "user": "postgres",
    "password": "postgres"
}
MONGO_URI = "mongodb://localhost:27017/"

# Параметры данных
USERS_COUNT = 5000
POSTS_COUNT = 100000
FRIENDS_PER_USER_MIN = 5
FRIENDS_PER_USER_MAX = 100
COMMENTS_PER_POST_WEIGHTS = [30, 25, 20, 10, 5, 3, 2, 2, 1, 1, 1]  # от 0 до 10 комментов


def setup_postgres():
    """Создание таблиц в PostgreSQL."""
    print("Настройка PostgreSQL...")
    
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Создаем базу данных, если её нет
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'social_network'")
    if not cursor.fetchone():
        cursor.execute("CREATE DATABASE social_network")
        print("  База данных social_network создана")
    
    conn.close()
    
    # Подключаемся к новой базе
    POSTGRES_CONFIG["database"] = "social_network"
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()
    
    # Создаем таблицы
    cursor.execute("DROP TABLE IF EXISTS friends CASCADE")
    cursor.execute("DROP TABLE IF EXISTS users CASCADE")
    
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    cursor.execute("""
        CREATE TABLE friends (
            user_id INTEGER REFERENCES users(id),
            friend_id INTEGER REFERENCES users(id),
            created_at TIMESTAMP DEFAULT NOW(),
            PRIMARY KEY (user_id, friend_id)
        )
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("  Таблицы созданы")


def setup_mongo():
    """Создание коллекций в MongoDB."""
    print("Настройка MongoDB...")
    
    client = MongoClient(MONGO_URI)
    db = client['social_network']
    
    # Удаляем старую коллекцию
    if 'posts' in db.list_collection_names():
        db.posts.drop()
    
    db.create_collection('posts')
    
    # Создаем индексы
    db.posts.create_index("post_id", unique=True)
    db.posts.create_index("author_id")
    
    client.close()
    print("  Коллекция posts создана, индексы построены")


def generate_users():
    """Генерация пользователей в PostgreSQL."""
    print("\n Генерация пользователей...")
    
    POSTGRES_CONFIG["database"] = "social_network"
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()
    
    users = []
    batch_size = 1000
    
    for i in range(0, USERS_COUNT, batch_size):
        batch = []
        for j in range(i + 1, min(i + batch_size, USERS_COUNT) + 1):
            user_id = j
            name = f"User_{user_id}"
            email = f"user{user_id}@example.com"
            batch.append((user_id, name, email))
        
        cursor.executemany(
            "INSERT INTO users (id, name, email) VALUES (%s, %s, %s)",
            batch
        )
        users.extend([b[0] for b in batch])
        conn.commit()
        print(f"    {len(users)}/{USERS_COUNT}")
    
    cursor.close()
    conn.close()
    
    print(f"   Создано {len(users)} пользователей")
    return users


def generate_friends(users):
    """Генерация социальных связей."""
    print("\n Генерация социальных связей...")
    
    POSTGRES_CONFIG["database"] = "social_network"
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()
    
    # Активные пользователи (20%) имеют больше связей
    active_users = set(random.sample(users, int(USERS_COUNT * 0.2)))
    
    friends_count = 0
    batch = []
    batch_size = 5000
    
    for user in users:
        if user in active_users:
            num_friends = random.randint(FRIENDS_PER_USER_MIN * 2, FRIENDS_PER_USER_MAX)
        else:
            num_friends = random.randint(FRIENDS_PER_USER_MIN, FRIENDS_PER_USER_MAX // 2)
        
        potential = [u for u in users if u != user]
        friends = random.sample(potential, min(num_friends, len(potential)))
        
        for friend in friends:
            if user < friend:  # только одна связь на пару
                batch.append((user, friend))
                friends_count += 1
                
                if len(batch) >= batch_size:
                    cursor.executemany(
                        "INSERT INTO friends (user_id, friend_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                        batch
                    )
                    conn.commit()
                    batch = []
        
        if user % 500 == 0:
            print(f"    Обработано пользователей: {user}/{USERS_COUNT}")
    
    # Вставка остатка
    if batch:
        cursor.executemany(
            "INSERT INTO friends (user_id, friend_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            batch
        )
        conn.commit()
    
    cursor.close()
    conn.close()
    
    print(f"   Создано {friends_count} социальных связей")


def generate_posts_and_comments(users):
    """Генерация постов и вложенных комментариев в MongoDB."""
    print("\n Генерация постов и комментариев...")
    
    client = MongoClient(MONGO_URI)
    db = client['social_network']
    posts_collection = db['posts']
    
    posts = []
    batch_size = 5000
    
    for i in range(POSTS_COUNT):
        author_id = random.choice(users)
        content = f"Пост {i + 1}: Содержимое поста от пользователя {author_id}"
        
        # Генерация вложенных комментариев
        num_comments = random.choices(range(0, 11), weights=COMMENTS_PER_POST_WEIGHTS)[0]
        comments = []
        
        for j in range(num_comments):
            comment_author = random.choice(users)
            comment_content = f"Комментарий {j + 1} к посту {i + 1}"
            comments.append({
                "comment_id": j + 1,
                "author_id": comment_author,
                "content": comment_content,
                "created_at": datetime.now().isoformat()
            })
        
        # Генерация лайков (0–50)
        num_likes = random.randint(0, 50)
        likes = random.sample(users, min(num_likes, len(users)))
        
        post = {
            "post_id": i + 1,
            "author_id": author_id,
            "content": content,
            "likes": likes,
            "comments": comments,
            "created_at": datetime.now().isoformat()
        }
        posts.append(post)
        
        # Пакетная вставка
        if len(posts) >= batch_size:
            posts_collection.insert_many(posts)
            print(f"    {i + 1}/{POSTS_COUNT}")
            posts = []
    
    # Вставка остатка
    if posts:
        posts_collection.insert_many(posts)
        print(f"    {POSTS_COUNT}/{POSTS_COUNT}")
    
    # Создаем индексы
    posts_collection.create_index("post_id", unique=True)
    posts_collection.create_index("author_id")
    
    client.close()
    print(f"  Создано {POSTS_COUNT} постов с вложенными комментариями")


def main():
    print("=" * 60)
    print("ГЕНЕРАЦИЯ СИНТЕТИЧЕСКИХ ДАННЫХ")
    print("=" * 60)
    print(f"Пользователей: {USERS_COUNT}")
    print(f"Постов: {POSTS_COUNT}")
    print("=" * 60)
    
    try:
        setup_postgres()
        setup_mongo()
        
        users = generate_users()
        generate_friends(users)
        generate_posts_and_comments(users)
        
        print("\n" + "=" * 60)
        print("ГЕНЕРАЦИЯ ЗАВЕРШЕНА")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
