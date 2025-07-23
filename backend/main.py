import os
import uuid
import tempfile
import shutil
import time

from typing import Annotated, List

import uvicorn
import polars as pl
import pandas as pd

from fastapi.responses import FileResponse
from fastapi import Body, FastAPI, File, Request, HTTPException, UploadFile, APIRouter, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# from ArpY.rainbow.cst.excel import process_results_file
# from ArpY.rainbow.project.data_fetcher import get_client_data, get_statements_data

from functions.scoreCalculating import cronbach_alpha


project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
runs_directory = os.path.join(project_directory, "runs")

app = FastAPI(root_path="/cronBach")
api = APIRouter(prefix="/api")


templates = Jinja2Templates(directory=os.path.join(project_directory, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(project_directory, "frontend", "dist")), name="static")
# app.mount("/static", StaticFiles(directory=r"frontend\dist"), name="static")

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


class FunctionCallRequest(BaseModel):
    """
    Request model for generic function calls.
    
    Attributes:
        function_name: Name of the function to call
        parameters: Dictionary of parameters to pass to the function
    """
    function_name: str
    parameters: dict


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

    statements = tuple(s for s in df.columns if s.endswith("*"))

    while True:
        task_id = str(uuid.uuid4())
        path = os.path.join(runs_directory, f"{task_id}.csv")
        if not os.path.exists(path):
            break

    df.select(statements).cast(pl.UInt8).write_csv(path, separator=";")

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

    # Test data since the code below cannot be run by Lucas at this point
    # @Lucas-vanerven: change the data is needed, please test with reduced number of statements
    response = [
        DisplayDataResponse(
            original_statement="The checkout process on the website was easy to navigate.",
            aliasses="",
            factor_groups=1
        ),
        DisplayDataResponse(
            original_statement="Customer service responded quickly to my inquiry.",
            aliasses="Quick support response",
            factor_groups=2
        ),
        DisplayDataResponse(
            original_statement="The product met my expectations based on the description.",
            aliasses="Product as described",
            factor_groups=3
        ),
        DisplayDataResponse(
            original_statement="I found it easy to locate what I was looking for on the site.",
            aliasses="Easy to find products",
            factor_groups=1
        ),
        DisplayDataResponse(
            original_statement="The delivery was faster than I expected.",
            aliasses="Fast delivery",
            factor_groups=4
        ),
        DisplayDataResponse(
            original_statement="I felt valued as a customer during the interaction.",
            aliasses="Felt valued",
            factor_groups=2
        ),
        DisplayDataResponse(
            original_statement="The website loaded quickly on my device.",
            aliasses="Fast website load",
            factor_groups=1
        ),
        DisplayDataResponse(
            original_statement="I was able to return the item without any issues.",
            aliasses="Easy return process",
            factor_groups=3
        ),
        DisplayDataResponse(
            original_statement="The pricing felt fair for the quality of the product.",
            aliasses="Fair pricing",
            factor_groups=3
        ),
        DisplayDataResponse(
            original_statement="I would recommend this company to others.",
            aliasses="Would recommend",
            factor_groups=4
        ),
        DisplayDataResponse(
            original_statement="I felt the company cared about my satisfaction.",
            aliasses="Company cares",
            factor_groups=2
        ),
        DisplayDataResponse(
            original_statement="There were multiple payment options available at checkout.",
            aliasses="Multiple payment options",
            factor_groups=1
        ),
        DisplayDataResponse(
            original_statement="The support staff was polite and helpful.",
            aliasses="Polite support",
            factor_groups=2
        ),
        DisplayDataResponse(
            original_statement="I received regular updates on my order status.",
            aliasses="Order updates",
            factor_groups=4
        ),
        DisplayDataResponse(
            original_statement="The product packaging was secure and undamaged.",
            aliasses="Secure packaging",
            factor_groups=4
        ),
        DisplayDataResponse(
            original_statement="I could easily access help or support when I needed it.",
            aliasses="Accessible support",
            factor_groups=2
        ),
        DisplayDataResponse(
            original_statement="The mobile experience was as good as the desktop version.",
            aliasses="Good mobile experience",
            factor_groups=1
        ),
        DisplayDataResponse(
            original_statement="The product quality exceeded my expectations.",
            aliasses="Great product quality",
            factor_groups=3
        ),
        DisplayDataResponse(
            original_statement="I trust this company to handle my personal information securely.",
            aliasses="Trust with data",
            factor_groups=4
        ),
        DisplayDataResponse(
            original_statement="The return policy was clearly explained and easy to understand.",
            aliasses="Clear return policy",
            factor_groups=3
        ),
    ]

    return response
    
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
def calculate_cronbach_alpha_endpoint(data: ScoreCalculationRequest) -> dict[int, float]:
    """
    Calculate Cronbach's alpha for all groups.
    This is done in one go to avoid multiple reads.
    
    Args:
        data: Score calculation request containing task_id and groups
            groups are the names of the statements
        
    Returns:
        dict[int, float]: A dictionary with group indices as keys and Cronbach's alpha values as values
    """
    path = os.path.join(project_directory, "runs", f"{data.task_id}.csv")
    df = pl.read_csv(path, separator=";")

    new_scores = {}

    for i, statements in enumerate(data.groups):
        new_scores[i] = cronbach_alpha(df.select(statements).to_pandas())
        
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
    
    """
    client: str
    statements: Annotated[list[str], "Original statements"]
    factor_groups: list[int]


@api.post("/save-factor-groups")
def save_factor_groups(request: SaveFactorGroupsRequest) -> dict[str, str]:
    """
    Save the factor groups to the database.
    """
    print("Going to save factor groups")
    return {"message": "Factor groups saved"}


# Dynamic function registry for backend/functions
class FunctionRegistry:
    def __init__(self):
        self.functions = {}
        self._register_functions()
    
    def _register_functions(self):
        """Register all available functions from backend/functions modules"""
        # Register scoreCalculating functions
        self.functions['cronbach_alpha'] = {
            'module': 'functions.scoreCalculating',
            'function': cronbach_alpha,
            'description': 'Calculate Cronbach\'s alpha for reliability analysis'
        }
    
    def get_function(self, function_name: str):
        """Get a function by name"""
        if function_name in self.functions:
            return self.functions[function_name]['function']
        raise ValueError(f"Function '{function_name}' not found")
    
    def list_functions(self):
        """List all available functions"""
        return {name: details['description'] for name, details in self.functions.items()}


function_registry = FunctionRegistry()

@app.post("/api/call-function")
def call_function(request: FunctionCallRequest):
    """Generic endpoint to call any function from backend/functions modules"""
    try:
        func = function_registry.get_function(request.function_name)
        
        # Handle specific function calls with their required parameters
        if request.function_name == 'cronbach_alpha':
            # Extract parameters for cronbach_alpha
            if 'group_data' in request.parameters:
                df = pd.DataFrame(request.parameters['group_data']).T
                print(func)
                result = func(df)
                return {
                    "function_name": request.function_name,
                    "result": result,
                    "parameters": request.parameters
                }
        
        raise ValueError(f"Function '{request.function_name}' requires specific parameter handling")
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calling function '{request.function_name}': {str(e)}")


app.include_router(api)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
