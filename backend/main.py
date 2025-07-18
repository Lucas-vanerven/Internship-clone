import os
import uuid
import tempfile
import shutil
import time

from typing import Annotated, List

import uvicorn
import polars as pl

from fastapi.responses import FileResponse
from fastapi import Body, FastAPI, File, Request, HTTPException, UploadFile, APIRouter, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ArpY.rainbow.cst.excel import process_results_file

from functions.scoreCalculating import cronbach_alpha


project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
runs_directory = os.path.join(project_directory, "runs")

app = FastAPI(root_path="/cronBach")
api = APIRouter(prefix="/api")


templates = Jinja2Templates(directory=os.path.join(project_directory, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(project_directory, "static")), name="static")
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
    groups: dict[Annotated[int, "Group index"], list[Annotated[str, "Statements"]]]


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
    hour_24_ago = time.time() - 60 * 60 * 24
    for file in os.listdir(runs_directory):
        if not file.endswith(".csv"):
            continue
        
        # Get the file's creation time
        creation_time = os.path.getctime(os.path.join(runs_directory, file))
        if creation_time < hour_24_ago:
            os.remove(os.path.join(runs_directory, file))


@app.get("/")
def read_root(request: Request):
    """
    Serve the main application page.
    
    Args:
        request: The incoming HTTP request
        
    Returns:
        Rendered HTML template with client information
    """
    delete_old_runs()
    
    test_clients = [
        "PPG",
        "SAP"
    ]
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "clients": test_clients
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
        df = process_results_file(tmp.name, return_polars=True)

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
    return FileResponse("frontend/dist/index.html")


@api.get("/get-factor-groups")
def get_factor_groups(request: Request):
    """
    Get the factor groups for a given task and client.
    """

    task_id = request.query_params.get("task_id")
    client = request.query_params.get("client")
    
    path = os.path.join(project_directory, "runs", f"{task_id}.csv")
    df = pl.read_csv(path, separator=";")
    
    statements_data = get_statements_data(client)

    


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

    for group_index, statements in data.groups.items():
        new_scores[group_index] = cronbach_alpha(df.select(statements).to_pandas())
        
    return new_scores


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
