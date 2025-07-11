from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import polars as pl
import pandas as pd
import os
import uuid

from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from pydantic import BaseModel
import uvicorn
# Import calculation functions
from functions.scoreCalculating import cronbach_alpha
from functions.statisticalAnalysis import descriptive_statistics, correlation_matrix, item_analysis

# Define request models
class StatementsRequest(BaseModel):
    statements: list[str]

class ScoreCalculationRequest(BaseModel):
    task_id: str  # Unique identifier for the task
    group_data: list[list[float]]  # 2D array where each inner list represents a statement's scores
    group_index: int

class GroupsScoreRequest(BaseModel):
    task_id: str  # Unique identifier for the task
    groups: list[list[list[float]]]  # Array of groups, each containing statement scores

class FunctionCallRequest(BaseModel):
    function_name: str
    parameters: dict

project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(project_directory, "templates"))
# app.mount("/static", StaticFiles(directory=os.path.join(project_directory, "static")), name="static")

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

# API endpoints
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount the compiled Vue app
# TODO: CHANGE FOR PORTABILITY - Use os.path.join for cross-platform compatibility
# Recommended: app.mount("/static", StaticFiles(directory=os.path.join(project_directory, "frontend", "dist")), name="static")
app.mount("/static", StaticFiles(directory=r"frontend\dist"), name="static")


# Serve the Vue app for all non-API routes
@app.get("/creating-factor-groups/{task_id}")
async def serve_vue_app(task_id: str):
    # Serve API routes normally
    
    # For all other routes, serve the Vue app
    # TODO: CHANGE FOR PORTABILITY - Use os.path.join for cross-platform file paths
    # Recommended: return FileResponse(os.path.join(project_directory, "frontend", "dist", "index.html"))
    return FileResponse("frontend/dist/index.html")



@app.post("/api/calculate-cronbach-alpha")
def calculate_cronbach_alpha_endpoint(data: ScoreCalculationRequest):
    """Calculate Cronbach's alpha for a single group"""
    print(data.task_id)
    try:
        # Convert the group data to a pandas DataFrame
        # Each row represents an observation, each column represents a statement
        df = pd.DataFrame(data.group_data).T  # Transpose to get correct orientation
        
        # Calculate Cronbach's alpha
        alpha_score = cronbach_alpha(df)
        
        return {
            "cronbach_alpha": alpha_score,
            "group_index": data.group_index,
            "items_count": len(data.group_data)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculating Cronbach's alpha: {str(e)}")

@app.post("/api/calculate-all-groups-scores")
def calculate_all_groups_scores(request: GroupsScoreRequest):
    """Calculate Cronbach's alpha for multiple groups"""
    print(request.task_id)
    try:
        results = []
        for i, group_data in enumerate(request.groups):
            if len(group_data) > 1:  # Need at least 2 items for Cronbach's alpha
                df = pd.DataFrame(group_data).T
                alpha_score = cronbach_alpha(df)
                results.append({
                    "group_index": i,
                    "cronbach_alpha": alpha_score,
                    "items_count": len(group_data)
                })
            else:
                results.append({
                    "group_index": i,
                    "cronbach_alpha": None,
                    "items_count": len(group_data),
                    "message": "Not enough items for calculation"
                })
        
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calculating scores: {str(e)}")

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
        
        # Register statisticalAnalysis functions
        self.functions['descriptive_statistics'] = {
            'module': 'functions.statisticalAnalysis',
            'function': descriptive_statistics,
            'description': 'Calculate descriptive statistics (mean, median, std, etc.)'
        }
        
        self.functions['correlation_matrix'] = {
            'module': 'functions.statisticalAnalysis',
            'function': correlation_matrix,
            'description': 'Calculate correlation matrix and related statistics'
        }
        
        self.functions['item_analysis'] = {
            'module': 'functions.statisticalAnalysis',
            'function': item_analysis,
            'description': 'Perform item analysis including item-total correlations'
        }
        
        # Add more functions as they are created
        # Example: self.functions['new_function'] = {
        #     'module': 'backend.functions.new_module', 
        #     'function': function_reference,
        #     'description': 'Description of what the function does'
        # }
    
    def get_function(self, function_name: str):
        """Get a function by name"""
        if function_name in self.functions:
            return self.functions[function_name]['function']
        raise ValueError(f"Function '{function_name}' not found")
    
    def list_functions(self):
        """List all available functions"""
        return {name: details['description'] for name, details in self.functions.items()}

# Initialize function registry
function_registry = FunctionRegistry()

@app.get("/api/functions")
def list_available_functions():
    """List all available functions from backend/functions modules"""
    print(9)
    return function_registry.list_functions()

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
        
        elif request.function_name in ['descriptive_statistics', 'correlation_matrix', 'item_analysis']:
            # Extract parameters for statistical analysis functions
            if 'group_data' in request.parameters:
                df = pd.DataFrame(request.parameters['group_data']).T
                result = func(df)
                return {
                    "function_name": request.function_name,
                    "result": result,
                    "parameters": request.parameters
                }
        
        # For other functions, you can add more specific handling here
        # or implement a more generic parameter passing mechanism
        
        raise ValueError(f"Function '{request.function_name}' requires specific parameter handling")
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error calling function '{request.function_name}': {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # TODO: CHANGE FOR PORTABILITY - Use environment variables for host and port configuration
    # Recommended: 
    # HOST = os.getenv("HOST", "127.0.0.1")
    # PORT = int(os.getenv("PORT", 8000))
    # uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
