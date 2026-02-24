from fastapi import APIRouter, Response, status

# from schemas.models import User, Post, Category, Location, Comment

router = APIRouter()


@router.get('/hello-world')
async def get_hello_world():
    return Response(content='Hello, World!', status_code=status.HTTP_200_OK)

# @router.post('/test-json', status_code=status.HTTP_200_OK)
# async def test_json(post: Post) -> dict:
#     response = {
#         "post_title": post.title,
#         "author": post.author
#     }

#     return response
