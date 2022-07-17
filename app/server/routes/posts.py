from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_post,
    delete_post,
    retrieve_post,
    retrieve_posts,
    update_post
)
from server.models.posts import (
    ErrorResponseModel,
    ResponseModel,
    PostSchema,
    UpdatePostSchema
)

router = APIRouter()

@router.post("/", response_description="Posted successfully!")
async def add_post_data(post: PostSchema = Body(...)):
    post = jsonable_encoder(post)
    new_post = await add_post(post)
    return ResponseModel(new_post, "Posted successfully!")

@router.get("/", response_description="Posts retrieved.")
async def get_posts():
    posts = await retrieve_posts()
    if posts:
        return ResponseModel(posts, "Posts data retrieved successfully")
    return ResponseModel(posts, "Empty list returned")

@router.get("/{id}", response_description="Post retrieved")
async def get_post_data(id):
    post = await retrieve_post(id)
    if post:
        return ResponseModel(post, "Post data retrieved successfully")
    return ErrorResponseModel("An error occured.", 404, "Post doesn't exist.")

@router.put("/{id}")
async def update_post_data(id: str, req: UpdatePostSchema = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_post = await update_post(id, req)
    if update_post:
        return ResponseModel(
            "Post with ID: {} name update is successful".format(id),
            "Post updated successfully"
        )
    return ErrorResponseModel(
        "An error occured",
        404,
        "There was an error updating the post data"
    )

@router.delete("/{id}", response_description="Post data deleted from the database")
async def delete_post_data(id: str):
    deleted_post = await delete_post(id)
    if deleted_post:
        return ResponseModel(
            "Post with ID: {} removed".format(id), "Post deleted successfully."
        )
    return ErrorResponseModel(
        "An error occured.", 404, "Post with id {0} doesn't exist".format(id)
    )