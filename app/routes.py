from fastapi import APIRouter, HTTPException
from app.models import UserModel
from app.database import db
from app.schemas import UserSchema
from .tasks import send_welcome_email
from bson import ObjectId

router = APIRouter()


@router.get("/")
async def read_main():
    return {"msg": "Hello World"}


# Add a new user
@router.post("/users", response_model=UserSchema)
async def create_user(user: UserModel):
    user_dict = user.model_dump()
    result = db.users.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)

    # Trigger the background task (send welcome email)
    send_welcome_email.delay(user.email)

    return user_dict


# Get a user by ID
@router.get("/users/{user_id}", response_model=UserSchema)
async def get_user(user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return user
    raise HTTPException(status_code=404, detail="User not found")
