from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import polars as pl
import os
import uuid

from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from pydantic import BaseModel
import uvicorn

# Define request models
class StatementsRequest(BaseModel):
    statements: list[str]

# Placeholder for Cronbach's alpha calculation
def cronbach_function(df: pl.DataFrame) -> float:
    # Implement Cronbach's alpha calculation here
    return 0.0

project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(project_directory, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(project_directory, "static")), name="static")

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

@app.get("/")
def home(request: Request):
    #zodra er een file is geupload, en client name is ingevuld, dan wordt de gebruiker doorgestuurd naar de  prepare task endpoint.
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/job/create/{id}")
def /api/job/create(id: str):
    #schrap alles behalve de daadwerkelijke statements uit de data file.
    #Uniek id voor de task, zodat de data file kan worden opgeslagen en later gebruikt.
    ...

@app.get("/api/factorization/{id}")
def factorization(id: str):
    #haal de aliassen op
    #laat de frontend API calls maken naar deze endpoints
    ...

@app.post("/api/calculate_score/{id}")
async def calculate_score(id: str, request: StatementsRequest):
    # Retrieve file from task folder
    path = f"tasks/{id}/data.xlsx"
    
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Task data file not found")
    
    try:
        df = pl.read_excel(path)
        columns = request.statements
        df = df.select(columns)
        return {"score": cronbach_function(df)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")


if __name__ == "__main__":
    bigapp = FastAPI()
    bigapp.mount("/cronBach", app)

    uvicorn.run(bigapp, port=8000)
