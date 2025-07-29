import os
import uuid
import tempfile
import shutil
import time
import sys

from typing import Annotated, List

import uvicorn
import polars as pl
import pandas as pd

from fastapi.responses import FileResponse
from fastapi import Body, FastAPI, File, Request, HTTPException, UploadFile, APIRouter, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
runs_directory = os.path.join(project_directory, "runs")

load_dotenv(os.path.join(project_directory, ".env"))
sys.path.append(project_directory)

# from ArpY.rainbow.cst.excel import process_results_file
# from ArpY.rainbow.project.data_fetcher import get_client_data, get_statements_data

from ArpY.rainbow.project.data_fetcher import get_statements_data

from functions.scoreCalculating import cronbach_alpha

app = FastAPI(root_path="/cronBach")
api = APIRouter(prefix="/api")


templates = Jinja2Templates(directory=os.path.join(project_directory, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(project_directory, "frontend", "dist")), name="static")
app.mount("/staticFirstPage", StaticFiles(directory=r"staticFirstPage"), name="staticFirstPage")

# Allow Vue.js frontend to communicate with FastAPI backend
app.add_middleware(
    CORSMiddleware,
    # TODO: CHANGE FOR PORTABILITY - Replace hardcoded localhost URLs with environment variables
    # Recommended: allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:443"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


class ScoreCalculationRequest(BaseModel):
    """
    Request model for calculating Cronbach's alpha scores.
    
    Attributes:
        task_id: Unique identifier for the task
        groups: Dictionary mapping group indices to lists of statement identifiers
    """
    task_id: str  # Unique identifier for the task
    groups: list[list[str]]  # every list is a group of statements
    #groups being the original statements

def delete_old_runs():
    """
    Delete CSV files in the runs directory that are older than 24 hours.
    This helps maintain storage space by removing temporary data.
    This is done during accessing the main page.(since the loading is instant) 
    """
    # Create runs directory if it doesn't exist
    if not os.path.exists(runs_directory):
        os.makedirs(runs_directory)
        return  # No files to delete if directory was just created
    
    hour_24_ago = time.time() - 60 * 60 * 24
    for file in os.listdir(runs_directory):
        if not file.endswith(".csv"):
            continue
        
        # Get the file's creation time
        creation_time = os.path.getctime(os.path.join(runs_directory, file))
        if creation_time < hour_24_ago:
            os.remove(os.path.join(runs_directory, file))


@app.get("/")
async def read_root(request: Request):
    """
    Serve the main application page.
    
    Args:
        request: The incoming HTTP request
        
    Returns:
        Rendered HTML template with client information
    """

    # @Lucas-vanerven: I've added a test in the root directory `test.xlsx`
    delete_old_runs()

    # client_data = await get_client_data()
    # clients = sorted(client_data["Client"].unique())
    
    clients = [
        "PPG",
        "SAP"
    ]
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "clients": clients
        }
    )


@api.post("/job/create")
def create_task(
    request: Request,
    files: List[UploadFile] = File(...),
    client: str = Form(...)
):
    """
    Create a new analysis task from uploaded Excel file.
    
    Args:
        request: The incoming HTTP request
        files: List of uploaded files (expecting one Excel file)
        client: Client identifier
        
    Returns:
        Dictionary with redirect URL to the factor group creation page
        
    Raises:
        HTTPException: If client is not provided
    """
    if client is None:
        raise HTTPException(status_code=400, detail="Client is required")

    # Here we need to simulate a file on the disk
    with tempfile.NamedTemporaryFile(suffix=".xlsx") as tmp:
        shutil.copyfileobj(files[0].file, tmp)
        tmp.seek(0)
        df = pl.read_excel(tmp.name)  # process_results_file(tmp.name, return_polars=True)

    while True:
        task_id = str(uuid.uuid4())
        path = os.path.join(runs_directory, f"{task_id}.csv")
        if not os.path.exists(path):
            break

    statements = tuple(s for s in df.columns if s.endswith("*"))
    statements_mapping = {s: s.removesuffix("*") for s in statements}

    df.select(statements).cast(pl.UInt8).rename(statements_mapping).write_csv(path, separator=";")

    base_url = str(request.base_url).rstrip('/')
    path = "/creating-factor-groups"
    params = f"?task_id={task_id}&client={client}"

    return {"redirect_url": f"{base_url}{path}{params}"}


@app.get("/creating-factor-groups")
async def serve_vue_app(request: Request):
    """
    Serve the Vue.js application for factor group creation.

    The frontend VUE is expecting `task_id` and `client` as query parameters.
    These are being used to correctly request the data from the backend in 
    separate requests.
    
    Args:
        request: The incoming HTTP request
        
    Returns:
        The Vue.js application HTML file
    """
    return FileResponse(os.path.join(project_directory, "frontend", "dist", "index.html"))


class DisplayDataResponse(BaseModel):
    original_statement: str
    aliasses: str
    factor_groups: int


@api.get("/get-display-data")
async def get_display_data(request: Request) -> list[DisplayDataResponse]:
    """
    Get the factor groups for a given task and client.
    This should be called from the VUE frontend to get the data for the display.
    
    Args:
        request: The incoming HTTP request
        
    Returns:
        List of DisplayDataResponse objects
    """

    task_id = request.query_params.get("task_id")
    client = request.query_params.get("client")

    if task_id is None or client is None:
        raise HTTPException(status_code=400, detail="Task ID and client are required as query parameters")
    
    response = []
    path = os.path.join(project_directory, "runs", f"{task_id}.csv")
    columns_in_df = pl.read_csv(path, separator=";").columns
    
    statements_data = await get_statements_data(client)
    
    # Loop over rows
    for statement in columns_in_df:
        row = statements_data.filter(pl.col("Originele statement") == statement)

        # We append the statemnet regardless of whether it is in the database or not
        if row.is_empty():
            response.append(DisplayDataResponse(
                original_statement=statement,
                aliasses="",
                factor_groups=-1
            ))
            continue

        factor_value = row["Factor"].item()
        factor_group = int(factor_value[1:]) if factor_value != "" and factor_value is not None else -1

        original_statement = row["Originele statement"].item()
        alias = row["Aliassen"].item()
        
        response.append(DisplayDataResponse(
            original_statement=original_statement,
            aliasses=alias,
            factor_groups=factor_group
        ))

    return response


@api.post("/calculate-cronbach-alpha")
def calculate_cronbach_alpha_endpoint(data: ScoreCalculationRequest) -> dict[int, float | None]:
    """
    Calculate Cronbach's alpha for all groups.
    This is done in one go to avoid multiple reads.
    
    Args:
        data: Score calculation request containing task_id and groups
            groups are the names of the statements
        
    Returns:
        dict[int, float | None]: A dictionary with group indices as keys and Cronbach's alpha values as values
                         Groups with less than 2 statements will have null values
    """
    path = os.path.join(project_directory, "runs", f"{data.task_id}.csv")
    df = pl.read_csv(path, separator=";")

    new_scores = {}

    for i, statements in enumerate(data.groups):
        # Check if group has less than 2 statements (source group limitation)
        if len(statements) < 2:
            new_scores[i] = None  # Return None for groups with insufficient statements
        else:
            try:
                new_scores[i] = cronbach_alpha(df.select(statements).to_pandas())
            except ValueError as e:
                # Handle cases where calculation fails due to insufficient data
                print(f"Warning: Could not calculate Cronbach's alpha for group {i}: {e}")
                new_scores[i] = None
        
    return new_scores


class DragDropCronbachRequest(BaseModel):
    """
    Request model for calculating Cronbach's alpha with drag-and-drop data.
    """
    group_data: list[list[float]]  # 2D array of statement scores
    group_index: int


@api.post("/calculate-cronbach-alpha-dragdrop")
def calculate_cronbach_alpha_dragdrop(data: DragDropCronbachRequest) -> dict:
    """
    Calculate Cronbach's alpha for drag-and-drop data.
    
    Args:
        data: DragDropCronbachRequest containing group_data (2D array) and group_index
        
    Returns:
        dict: Cronbach's alpha result with value and group_index
    """
    import pandas as pd
    
    # Convert the 2D array to a DataFrame where each row is a statement's responses
    # Transpose so each column represents a statement
    df = pd.DataFrame(data.group_data).T
    
    # Calculate Cronbach's alpha
    alpha_value = cronbach_alpha(df)
    
    return {
        "cronbach_alpha": alpha_value,
        "group_index": data.group_index,
        "num_statements": len(data.group_data),
        "num_responses": len(data.group_data[0]) if data.group_data else 0
    }


class SaveFactorGroupsRequest(BaseModel):
    """
    Request model for saving factor groups.
    
    Attributes:
        task_id: Unique identifier for the task
        client: Client identifier
        groups: List of four groups, each containing statements with their information
    """
    task_id: str
    client: str
    groups: list[list[dict]]  # Four groups, each containing statement objects


@api.post("/save-factor-groups")
def save_factor_groups(request: SaveFactorGroupsRequest) -> dict:
    """
    Save the factor groups to the database.
    
    Args:
        request: SaveFactorGroupsRequest containing task_id, client, and four groups
        
    Returns:
        dict: Success message with details about what was saved
    """
    print(f"Saving factor groups for task_id: {request.task_id}, client: {request.client}")
    print(f"Number of groups: {len(request.groups)}")
    
    # Log the structure of what we're receiving
    for i, group in enumerate(request.groups):
        print(f"Group {i+1} has {len(group)} statements:")
        for statement in group:
            original = statement.get('original_statement', 'N/A')
            print(f"  - {original}")

    total_statements = sum(len(group) for group in request.groups)
    
    return {
        "message": "Factor groups saved successfully",
        "task_id": request.task_id,
        "client": request.client,
        "total_statements": total_statements,
        "groups_count": len(request.groups)
    }


app.include_router(api)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
