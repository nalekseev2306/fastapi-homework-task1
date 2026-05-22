from locust import HttpUser, task, between
import random


class DjangoUser(HttpUser):
    wait_time = between(0.01, 0.05)
    host = "http://localhost:8000"

    @task(3)
    def get_posts(self):
        self.client.get("/api/v1/posts/", name="/api/v1/posts")

    @task(2)
    def get_post_detail(self):
        post_id = random.randint(100, 299)
        self.client.get(f"/api/v1/posts/{post_id}/", name="/api/v1/posts/{id}")

    @task(2)
    def get_users(self):
        self.client.get("/api/v1/users/", name="/api/v1/users")

    @task(2)
    def get_user_detail(self):
        user_id = random.randint(100, 199)
        self.client.get(f"/api/v1/users/{user_id}/", name="/api/v1/users/{id}")

    @task(2)
    def get_category_by_id(self):
        category_id = random.randint(1, 10)
        self.client.get(f"/api/v1/categories/{category_id}/", name="/api/v1/categories/{id}")

    @task(2)
    def get_comment_detail(self):
        comment_id = random.randint(1, 500)
        self.client.get(f"/api/v1/comments/{comment_id}/", name="/api/v1/comments/{id}")

    @task(2)
    def get_locations(self):
        self.client.get("/api/v1/locations/", name="/api/v1/locations")
