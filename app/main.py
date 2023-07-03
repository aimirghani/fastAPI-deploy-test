from fastapi import FastAPI
from app.routers import posts, users, auth


app = FastAPI()


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)



@app.get("/")
def home():
    return {"message": "Social media API under Dev..."}