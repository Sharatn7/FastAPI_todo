from fastapi import FastAPI, Request
import uvicorn
from database.connection import Settings
from routes import routelist
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

settings = Settings()
app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.on_event("startup")
async def init_db():
    await settings.initialize_database()

app.include_router(routelist.todo_router)

if __name__ == "__main__":
    uvicorn.run("root:app", host="127.0.0.1", port=8000, reload=True)
