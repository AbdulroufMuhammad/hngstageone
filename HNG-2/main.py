from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# Enable CORS (allow all origins, methods, and headers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {
        "email": "abdulraufmuhammad28@gmail.com",
        "current_datetime": datetime.utcnow().isoformat() + "Z",  # ISO 8601 in UTC
        "github_url": "https://github.com/AbdulroufMuhammad/HNG-2.git"
    }
