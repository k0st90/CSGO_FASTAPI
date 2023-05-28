from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import config
from .routers import account, faceit, tracker_gg

#models.Base.metadata.create_all(bind=engine)

password = config.database_password.get_secret_value()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(account.router)
app.include_router(faceit.router)
app.include_router(tracker_gg.router)

@app.get("/")
def root():
    return {"message": "Hello world"}