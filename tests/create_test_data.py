import os
import sys
import random
import asyncio
import argparse
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, select
from passlib.context import CryptContext
from datetime import datetime, timedelta

from src.core.config import settings
from src.infrastructure.postgres.models import User, Category, Location, Post, Comment

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TestDataInitializer:
    def __init__(self):
        self.engine = create_async_engine(settings.postgres_url, echo=False)
        self.async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def clear_all_data(self):
        async with self.async_session() as session:
            print("\nClearing existing data...")
            
            await session.execute(text("TRUNCATE TABLE application.comments CASCADE;"))
            await session.execute(text("TRUNCATE TABLE application.posts CASCADE;"))
            await session.execute(text("TRUNCATE TABLE application.categories CASCADE;"))
            await session.execute(text("TRUNCATE TABLE application.locations CASCADE;"))
            await session.execute(text("TRUNCATE TABLE application.users CASCADE;"))
            
            await session.commit()
            print("   All data cleared")

    async def create_test_users(self, start_id=100, count=100):
        print("\nCreating test users...")
        users = []
        
        async with self.async_session() as session:
            for i in range(start_id, start_id + count):
                username = f"user_{i}"
                email = f"{username}@example.com"
                hashed_password = pwd_context.hash("password123")
                
                user = User(
                    id=i,
                    username=username,
                    email=email,
                    password=hashed_password,
                    first_name="Test",
                    last_name="User",
                    is_superuser=False,
                )
                session.add(user)
                users.append(user)
            
            await session.commit()
        
        print(f"   Created {count} users (ids: {start_id}-{start_id + count - 1})")
        return users

    async def create_categories(self):
        print("\nCreating categories...")
        categories_data = [
            {"id": 1, "name": "Технологии", "slug": "technology", "description": "Tech news and reviews", "is_published": True},
            {"id": 2, "name": "Наука", "slug": "science", "description": "Scientific discoveries", "is_published": True},
            {"id": 3, "name": "Искусство", "slug": "art", "description": "Art and culture", "is_published": True},
            {"id": 4, "name": "Спорт", "slug": "sports", "description": "Sports news", "is_published": True},
            {"id": 5, "name": "Музыка", "slug": "music", "description": "Music reviews", "is_published": True},
            {"id": 6, "name": "Фильмы", "slug": "movies", "description": "Movie reviews", "is_published": True},
            {"id": 7, "name": "Книги", "slug": "books", "description": "Book reviews", "is_published": True},
            {"id": 8, "name": "Путешествия", "slug": "travel", "description": "Travel guides", "is_published": True},
            {"id": 9, "name": "Еда", "slug": "food", "description": "Food and recipes", "is_published": True},
            {"id": 10, "name": "Бизнес", "slug": "business", "description": "Business news", "is_published": True}
        ]
        
        categories = []
        async with self.async_session() as session:
            for cat_data in categories_data:
                result = await session.execute(
                    select(Category).where(Category.slug == cat_data["slug"])
                )
                category = result.scalar_one_or_none()
                
                if not category:
                    category = Category(**cat_data)
                    session.add(category)
                    categories.append(category)
                else:
                    categories.append(category)
            
            await session.commit()
        
        print(f"   Created {len(categories)} categories")
        return categories

    async def create_locations(self):
        print("\nCreating locations...")
        locations_data = [
            {"name": "Москва", "is_published": True},
            {"name": "Санкт-Петербург", "is_published": True},
            {"name": "Новосибирск", "is_published": True},
            {"name": "Екатеринбург", "is_published": True},
            {"name": "Казань", "is_published": True},
            {"name": "Нижний Новгород", "is_published": True},
            {"name": "Челябинск", "is_published": True},
            {"name": "Омск", "is_published": True},
            {"name": "Самара", "is_published": True},
            {"name": "Ростов-на-Дону", "is_published": True}
        ]
        
        locations = []
        async with self.async_session() as session:
            for loc_data in locations_data:
                result = await session.execute(
                    select(Location).where(Location.name == loc_data["name"])
                )
                location = result.scalar_one_or_none()
                
                if not location:
                    location = Location(**loc_data)
                    session.add(location)
                    locations.append(location)
                else:
                    locations.append(location)
            
            await session.commit()
        
        print(f"   Created {len(locations)} locations")
        return locations

    async def create_test_posts(self, users, categories, locations, posts_count=200):
        print(f"\nCreating {posts_count} posts...")
        
        async with self.async_session() as session:
            user_ids = [u.id for u in users]
            category_ids = [c.id for c in categories]
            location_ids = [l.id for l in locations]
            
            for i in range(posts_count):
                post_id = 100 + i
                
                post = Post(
                    id=post_id,
                    title=f"Test Post #{post_id}",
                    text=f"This is test post number {post_id}. " * 2,
                    pub_date=datetime.now() - timedelta(days=random.randint(0, 30)),
                    user_id=random.choice(user_ids),
                    category_id=random.choice(category_ids),
                    location_id=random.choice(location_ids),
                    is_published=True
                )
                session.add(post)
            
            await session.commit()
        
        print(f"   Created {posts_count} posts")

    async def create_test_comments(self, users, comments_count=500):
        print(f"\nCreating {comments_count} comments...")
        
        async with self.async_session() as session:
            result = await session.execute(select(Post.id))
            post_ids = [row[0] for row in result.all()]
            
            user_ids = [u.id for u in users]
            
            for i in range(comments_count):
                comment_id = 1 + i
                
                comment = Comment(
                    id=comment_id,
                    text=f"Test comment #{comment_id} from user. " * 3,
                    user_id=random.choice(user_ids),
                    post_id=random.choice(post_ids),
                    created_at=datetime.now() - timedelta(days=random.randint(0, 15))
                )
                session.add(comment)
            
            await session.commit()
        
        print(f"   Created {comments_count} comments")

    async def run(self, clean=False, users_count=100, posts_count=200, comments_count=500):
        print("Starting database initialization with test data")
        
        if clean:
            await self.clear_all_data()
        
        users = await self.create_test_users(count=users_count)
        categories = await self.create_categories()
        locations = await self.create_locations()
        
        await self.create_test_posts(users, categories, locations, posts_count=posts_count)
        await self.create_test_comments(users, comments_count=comments_count)
        
        print("\nDone. Now u can run:")
        print("  locust -f ./tests/locustfile.py")

async def main():
    parser = argparse.ArgumentParser(description="Initialize test data")
    parser.add_argument("--clean", action="store_true", help="Clear existing data before init")
    parser.add_argument("--users", type=int, default=100, help="Number of users to create")
    parser.add_argument("--posts", type=int, default=200, help="Number of posts to create")
    parser.add_argument("--comments", type=int, default=500, help="Number of comments to create")
    
    args = parser.parse_args()
    
    initializer = TestDataInitializer()
    await initializer.run(
        clean=args.clean,
        users_count=args.users,
        posts_count=args.posts,
        comments_count=args.comments
    )

if __name__ == "__main__":
    asyncio.run(main())
