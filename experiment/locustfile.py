from locust import HttpUser, task, between
import random

class SocialNetworkUser(HttpUser):
    wait_time = between(1, 3)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = random.randint(1, 5000)
    
    @task(3)
    def get_post_hybrid(self):
        """Гибридная модель: пост из MongoDB"""
        post_id = random.randint(1, 100000)
        self.client.get(f"/api/posts/{post_id}", name="GET /api/posts/[id] (гибрид)")
    
    @task(3)
    def get_post_relational(self):
        """Реляционная модель: пост через JOIN"""
        post_id = random.randint(1, 100000)
        self.client.get(f"/api/posts/{post_id}/relational", name="GET /api/posts/[id]/relational (реляционная)")
    
    @task(2)
    def get_feed(self):
        """Получение ленты"""
        self.client.get(f"/api/feed?user_id={self.user_id}&limit=20", name="GET /api/feed")
    
    @task(1)
    def like_post(self):
        """Постановка лайка"""
        post_id = random.randint(1, 100000)
        self.client.post(f"/api/posts/{post_id}/like?user_id={self.user_id}", name="POST /api/posts/[id]/like")
    
    @task(1)
    def get_friends(self):
        """Получение списка друзей"""
        self.client.get(f"/api/users/{self.user_id}/friends", name="GET /api/users/[id]/friends")
