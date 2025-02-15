from fastapi import FastAPI
from dotenv import load_dotenv

from app.routes import router

# Load environment variables from the .env file
load_dotenv()

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
