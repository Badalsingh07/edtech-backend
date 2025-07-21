from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import models
from database import engine
from routes import router

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# Enable CORS (for JS fetch requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
#app.mount("/static", StaticFiles(directory="frontend"), name="static")
