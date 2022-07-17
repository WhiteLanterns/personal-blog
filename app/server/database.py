import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

MONGO_DETAILS = config("MONGO_DETAILS")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.posts

post_collection = database.get_collection("posts_collection")

# helpers

def post_helper(post) -> dict:
    return {
        "id": str(post["_id"]),
        "title": post["title"],
        "content": post["content"],
        "date": post["date"]
    }


# Retrieve all posts in the DB
async def retrieve_posts():
    posts = []
    async for post in post_collection.find():
        posts.append(post_helper(post))
    return posts

# Add new post into DB
async def add_post(post_data: dict) -> dict:
    post = await post_collection.insert_one(post_data)
    new_post = await post_collection.find_one({"_id": post.inserted_id})
    return post_helper(new_post)

# Retrieve specific post in DB
async def retrieve_post(id: str) -> dict:
    post = await post_collection.find_one({"_id": ObjectId(id)})
    if post:
        return post_helper(post)

# Update a post with a matching ID
async def update_post(id: str, data: dict):
    # Return false if an empty request is sent
    if len(data) < 1:
        return False
    post = await post_collection.find_one({"_id": ObjectId(id)})
    if post:
        updated_post = await post_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if update_post:
            return True
        return False

# Delete a post from the DB
async def delete_post(id: str):
    post = await post_collection.find_one({"_id": ObjectId(id)})
    if post:
        await post_collection.delete_one({"_id": ObjectId(id)})
        return True