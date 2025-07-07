# Backend Function Integration Guide

This guide explains how to add new functions to the backend and make them accessible via API calls from the frontend.

## Architecture Overview

The system is designed to be extensible, allowing you to easily add new statistical or analytical functions to the `backend/functions/` folder and automatically expose them via API endpoints.

### Components:

1. **Function Modules**: Python files in `backend/functions/` containing your analytical functions
2. **Function Registry**: Automatically registers and manages available functions
3. **API Endpoints**: Generic endpoints that can call any registered function
4. **Frontend Service**: Centralized API service for calling backend functions

## Adding a New Function

### Step 1: Create Your Function

Create a new Python file in `backend/functions/` or add to an existing one:

```python
# backend/functions/myNewAnalysis.py
import pandas as pd
import numpy as np
from typing import Dict, Any

def my_new_function(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Description of what your function does.
    
    Args:
        df (pd.DataFrame): Input data with variables as columns, observations as rows
        
    Returns:
        Dict[str, Any]: Results dictionary
    """
    # Your analysis logic here
    result = {
        "analysis_result": df.mean().to_dict(),
        "additional_data": "some_value"
    }
    return result
```

### Step 2: Register the Function

In `backend/main.py`, add your function to the imports and registry:

```python
# Add to imports at the top
from backend.functions.myNewAnalysis import my_new_function

# Add to the _register_functions method in FunctionRegistry class
self.functions['my_new_function'] = {
    'module': 'backend.functions.myNewAnalysis',
    'function': my_new_function,
    'description': 'Description of what my function does'
}
```

### Step 3: Update the Function Call Handler

In the `call_function` endpoint, add handling for your new function:

```python
elif request.function_name == 'my_new_function':
    if 'group_data' in request.parameters:
        df = pd.DataFrame(request.parameters['group_data']).T
        result = func(df)
        return {
            "function_name": request.function_name,
            "result": result,
            "parameters": request.parameters
        }
```

### Step 4: Use in Frontend

Call your function from Vue.js components:

```javascript
import apiService from '../services/apiService.js';

// Call your function
const result = await apiService.callFunction('my_new_function', {
  group_data: sampleData
});

console.log('Result:', result);
```

## Available API Endpoints

### 1. List Available Functions
```javascript
GET /api/functions
```
Returns all registered functions with descriptions.

### 2. Calculate Cronbach's Alpha (Specific)
```javascript
POST /api/calculate-cronbach-alpha
{
  "group_data": [[5,4,3,5], [4,5,4,4], [3,4,5,3]],
  "group_index": 0
}
```

### 3. Calculate All Groups (Specific)
```javascript
POST /api/calculate-all-groups-scores
{
  "groups": [
    [[5,4,3,5], [4,5,4,4]],
    [[3,4,5,3], [5,3,4,5]]
  ]
}
```

### 4. Generic Function Call
```javascript
POST /api/call-function
{
  "function_name": "cronbach_alpha",
  "parameters": {
    "group_data": [[5,4,3,5], [4,5,4,4], [3,4,5,3]]
  }
}
```

## Frontend API Service Methods

### Generic Methods
```javascript
// List all available functions
const functions = await apiService.listAvailableFunctions();

// Call any function
const result = await apiService.callFunction('function_name', parameters);
```

### Specific Methods
```javascript
// Cronbach's Alpha specific methods
const result1 = await apiService.calculateCronbachAlpha(groupData, groupIndex);
const result2 = await apiService.callCronbachAlpha(groupData);
```

## Data Format

### Expected Input Format
Functions expect data in this format:
- **group_data**: Array of arrays where each inner array represents responses to one statement
- Example: `[[5,4,3,5,4], [4,5,4,4,3], [3,4,5,3,4]]`
  - First array: responses to statement 1
  - Second array: responses to statement 2
  - etc.

### DataFrame Conversion
The backend automatically converts this to a pandas DataFrame where:
- Rows = observations/respondents
- Columns = variables/statements

## Example Functions

### Current Available Functions:

1. **cronbach_alpha**: Calculate Cronbach's alpha reliability coefficient
2. **descriptive_statistics**: Mean, median, std dev, variance, etc.
3. **correlation_matrix**: Correlation matrix and related statistics
4. **item_analysis**: Item-total correlations and item statistics

### Function Template:

```python
def new_analysis_function(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Template for new analysis functions.
    
    Args:
        df (pd.DataFrame): Data with variables as columns, observations as rows
        
    Returns:
        Dict[str, Any]: Analysis results
    """
    # Ensure data is clean
    data = df.dropna()
    
    # Perform your analysis
    result = {
        "main_result": "your_calculation",
        "additional_info": "supplementary_data",
        "metadata": {
            "n_observations": len(data),
            "n_variables": len(data.columns)
        }
    }
    
    return result
```

## Testing Your Functions

Use the FunctionTester component (included in FactorCalculator page) to test your new functions:

1. Navigate to the Factor Calculator page
2. Use the "Function Tester" section to test different functions
3. Check browser console for detailed logs
4. Verify results in the UI

## Error Handling

The system includes comprehensive error handling:
- Invalid function names return appropriate error messages
- Missing parameters are caught and reported
- Backend exceptions are properly formatted and returned to frontend
- Frontend displays errors in a user-friendly way

## Best Practices

1. **Function Names**: Use descriptive, lowercase names with underscores
2. **Documentation**: Always include docstrings with Args and Returns
3. **Error Handling**: Handle edge cases (empty data, insufficient data, etc.)
4. **Return Format**: Always return dictionaries for consistency
5. **Data Validation**: Validate input data before processing
6. **Testing**: Test functions with various data scenarios

## Development Workflow

1. Create function in `backend/functions/`
2. Register function in `backend/main.py`
3. Update call handler if needed
4. Test using FunctionTester component
5. Integrate into your Vue.js components
6. Deploy and test in production environment
