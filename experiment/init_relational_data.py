"""
Генерация реляционных данных (посты и комментарии в отдельных таблицах)
для сравнения с гибридной моделью.
"""

import random
import psycopg2
from datetime import datetime

# Конфигурация
POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "social_network",
    "user": "postgres",
    "password": "postgres"
}

# Параметры
POSTS_COUNT = 100000
COMMENTS_PER_POST_WEIGHTS = [30, 25, 20, 10, 5, 3, 2, 2, 1, 1, 1]  # от 0 до 10 комментов


def setup_relational_tables(conn):
    """Создание реляционных таблиц для постов и комментариев."""
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS comments_relational CASCADE")
    cursor.execute("DROP TABLE IF EXISTS posts_relational CASCADE")
    
    cursor.execute("""
        CREATE TABLE posts_relational (
            id INTEGER PRIMARY KEY,
            author_id INTEGER REFERENCES users(id),
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    cursor.execute("""
        CREATE TABLE comments_relational (
            id SERIAL PRIMARY KEY,
            post_id INTEGER REFERENCES posts_relational(id) ON DELETE CASCADE,
            author_id INTEGER REFERENCES users(id),
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    cursor.execute("CREATE INDEX idx_comments_post_id ON comments_relational(post_id)")
    cursor.execute("CREATE INDEX idx_posts_author_id ON posts_relational(author_id)")
    
    conn.commit()
    cursor.close()
    print(" Реляционные таблицы созданы")


def generate_posts_relational(conn, users):
    """Генерация постов в реляционной таблице."""
    cursor = conn.cursor()
    
    print(f"  Создание {POSTS_COUNT} постов в PostgreSQL...")
    
    batch = []
    batch_size = 5000
    
    for i in range(POSTS_COUNT):
        author_id = random.choice(users)
        content = f"Пост {i + 1}: Содержимое от пользователя {author_id}"
        batch.append((i + 1, author_id, content))
        
        if len(batch) >= batch_size:
            cursor.executemany(
                "INSERT INTO posts_relational (id, author_id, content) VALUES (%s, %s, %s)",
                batch
            )
            conn.commit()
            print(f"    {i + 1}/{POSTS_COUNT}")
            batch = []
    
    if batch:
        cursor.executemany(
            "INSERT INTO posts_relational (id, author_id, content) VALUES (%s, %s, %s)",
            batch
        )
        conn.commit()
    
    cursor.close()
    print(f"   Создано {POSTS_COUNT} постов")


def generate_comments_relational(conn, users):
    """Генерация комментариев в реляционной таблице."""
    cursor = conn.cursor()
    
    print("  Создание комментариев в PostgreSQL...")
    
    # Получаем все ID постов
    cursor.execute("SELECT id FROM posts_relational")
    post_ids = [row[0] for row in cursor.fetchall()]
    
    comments_count = 0
    batch = []
    batch_size = 10000
    
    for post_id in post_ids:
        num_comments = random.choices(range(0, 11), weights=COMMENTS_PER_POST_WEIGHTS)[0]
        
        for j in range(num_comments):
            comment_author = random.choice(users)
            content = f"Комментарий {j + 1} к посту {post_id}"
            batch.append((post_id, comment_author, content))
            comments_count += 1
            
            if len(batch) >= batch_size:
                cursor.executemany(
                    "INSERT INTO comments_relational (post_id, author_id, content) VALUES (%s, %s, %s)",
                    batch
                )
                conn.commit()
                print(f"    {comments_count} комментариев")
                batch = []
        
        if post_id % 10000 == 0:
            print(f"    Обработано постов: {post_id}/{POSTS_COUNT}")
    
    if batch:
        cursor.executemany(
            "INSERT INTO comments_relational (post_id, author_id, content) VALUES (%s, %s, %s)",
            batch
        )
        conn.commit()
    
    cursor.close()
    print(f"   Создано {comments_count} комментариев")


def main():
    print("=" * 60)
    print("ГЕНЕРАЦИЯ РЕЛЯЦИОННЫХ ДАННЫХ (посты + комментарии)")
    print("=" * 60)
    
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        
        # Получаем список пользователей
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users")
        users = [row[0] for row in cursor.fetchall()]
        cursor.close()
        
        setup_relational_tables(conn)
        generate_posts_relational(conn, users)
        generate_comments_relational(conn, users)
        
        conn.close()
        
        print("\n" + "=" * 60)
        print(" ГЕНЕРАЦИЯ ЗАВЕРШЕНА")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n Ошибка: {e}")


if __name__ == "__main__":
    main()
