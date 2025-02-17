from fastapi import APIRouter, HTTPException
from bson import ObjectId
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from app.models import UserModel
from app.database import db
from app.schemas import UserSchema, PromptRequest
from .tasks import send_welcome_email

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


@router.post("/llm")
async def get_llm_response(request: PromptRequest):

    """FastAPI route to get responses from OpenAI via LangChain."""
    # Create the Groq chat instance
    chat = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")

    template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI bot. Your name is {name}."),
        ("human", "What is the capital of UK?"),
        ("ai", "London, thanks!"),
        ("human", "{user_input}"),
    ])

    chain = template | chat
    response = chain.invoke({
        "name": "GroqBot",
        "user_input": "What is the capital of USA?"
    })
    if not response:
        raise HTTPException(
            status_code=500, detail="Failed to generate response.")
    return {"response": response.content}
