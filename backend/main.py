from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse


app = FastAPI()

# Allow Vue.js frontend to communicate with FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:443"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/backend")
def read_root():
    return {"message": "Hello from FastAPI!"} 


@app.get("/backend/test")
def read_root():
    return RedirectResponse(url="http://localhost:5173")
