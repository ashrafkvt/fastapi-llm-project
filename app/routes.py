from fastapi import APIRouter, HTTPException
from app.models import UserModel
from app.database import db
from app.schemas import UserSchema
from bson import ObjectId

router = APIRouter()


# Add a new user
@router.post("/users", response_model=UserSchema)
async def create_user(user: UserModel):
    user_dict = user.model_dump()
    result = db.users.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)
    return user_dict


# Get a user by ID
@router.get("/users/{user_id}", response_model=UserSchema)
async def get_user(user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return user
    raise HTTPException(status_code=404, detail="User not found")
