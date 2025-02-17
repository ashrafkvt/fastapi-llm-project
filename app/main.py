import os

from fastapi import FastAPI
from dotenv import load_dotenv

from app.routes import router

# Load environment variables from the .env file
load_dotenv()

app = FastAPI()

app.include_router(router)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
