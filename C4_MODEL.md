# C4 Model for Cronbach's Alpha Web Application

This document presents the C4 model for the Cronbach's Alpha Web Application, providing a comprehensive architectural overview at different levels of abstraction.

## What is the C4 Model?

The C4 model is a lean graphical notation technique for modeling the architecture of software systems. It consists of four hierarchical levels:

1. **System Context** - Shows how the software system fits into the world around it
2. **Container** - Shows the high-level technology choices and how responsibilities are distributed
3. **Component** - Shows how a container is made up of components and their interactions
4. **Code** - Shows how a component is implemented (optional)

## System Overview

The Cronbach's Alpha Web Application is a statistical analysis tool designed to calculate Cronbach's alpha reliability coefficients for survey data. It provides a web-based interface for researchers and analysts to upload data, organize items into factor groups, and compute reliability statistics.

---

## Level 1: System Context Diagram

```plantuml
@startuml C4_Context
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

title System Context Diagram for Cronbach's Alpha Web Application

Person(researcher, "Researcher/Analyst", "Uses the application to analyze survey data and calculate Cronbach's alpha reliability coefficients")
Person(admin, "System Administrator", "Manages the application deployment and monitors system health")

System(cronbach_app, "Cronbach's Alpha Web Application", "Provides web-based interface for statistical reliability analysis of survey data")

System_Ext(file_system, "File System", "Stores uploaded data files and analysis results")
System_Ext(arpy_system, "ArpY Data System", "External data processing and storage system for research data")
System_Ext(redis, "Redis Cache", "Caches session data and temporary analysis results")
System_Ext(mongodb, "MongoDB Database", "Stores persistent data and analysis history")

Rel(researcher, cronbach_app, "Uploads data files, creates factor groups, analyzes reliability", "HTTPS")
Rel(admin, cronbach_app, "Monitors and maintains", "HTTPS")
Rel(cronbach_app, file_system, "Reads/writes data files", "File I/O")
Rel(cronbach_app, arpy_system, "Fetches research data", "HTTP/REST")
Rel(cronbach_app, redis, "Caches session data", "Redis Protocol")
Rel(cronbach_app, mongodb, "Stores analysis data", "MongoDB Protocol")

@enduml
```

### Key External Actors and Systems:

- **Researchers/Analysts**: Primary users who upload survey data and perform reliability analysis
- **System Administrators**: Manage and maintain the application
- **File System**: Local storage for uploaded files and results
- **ArpY Data System**: External research data management system
- **Redis**: Caching layer for performance optimization
- **MongoDB**: Primary database for persistent storage

---

## Level 2: Container Diagram

```plantuml
@startuml C4_Container
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

title Container Diagram for Cronbach's Alpha Web Application

Person(user, "User", "Researcher or Analyst")

Container_Boundary(webapp, "Cronbach's Alpha Web Application") {
    Container(spa, "Single Page Application", "Vue.js 3", "Provides the user interface for data upload, factor grouping, and analysis visualization")
    Container(api, "API Server", "FastAPI/Python", "Handles HTTP requests, file uploads, statistical calculations, and data management")
    Container(static_files, "Static File Server", "FastAPI StaticFiles", "Serves built frontend assets and uploaded data files")
}

ContainerDb(file_storage, "File Storage", "Local Filesystem", "Stores uploaded Excel/CSV files and generated reports")
ContainerDb(redis_cache, "Cache", "Redis", "Stores session data and temporary calculation results")
ContainerDb(database, "Database", "MongoDB", "Stores analysis metadata, factor groups, and historical results")

Container_Ext(arpy, "ArpY Module", "Python Package", "External data processing library for research data")

Rel(user, spa, "Uses", "HTTPS")
Rel(spa, api, "Makes API calls", "JSON/HTTPS")
Rel(spa, static_files, "Loads assets", "HTTPS")
Rel(api, file_storage, "Reads/writes files", "File I/O")
Rel(api, redis_cache, "Caches data", "Redis Protocol")
Rel(api, database, "Stores/retrieves data", "MongoDB Wire Protocol")
Rel(api, arpy, "Processes research data", "Python imports")

@enduml
```

### Container Descriptions:

- **Single Page Application (Vue.js)**: Frontend interface providing drag-and-drop factor grouping and real-time analysis
- **API Server (FastAPI)**: Backend service handling business logic, statistical calculations, and data persistence
- **Static File Server**: Serves the built frontend and manages file uploads
- **File Storage**: Local filesystem for temporary and permanent file storage
- **Cache (Redis)**: High-performance caching for session management and intermediate results
- **Database (MongoDB)**: Document database for flexible storage of analysis metadata
- **ArpY Module**: External Python package for specialized research data processing

---

## Level 3: Component Diagrams

### Frontend Components (Vue.js SPA)

```plantuml
@startuml C4_Component_Frontend
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

title Component Diagram - Vue.js Frontend

Container(api, "API Server", "FastAPI")

Container_Boundary(spa, "Single Page Application") {
    Component(router, "Vue Router", "Vue.js Plugin", "Handles client-side routing between pages")
    Component(upload_page, "Upload Page", "Vue Component", "File upload interface for Excel/CSV data")
    Component(factor_calc, "Factor Calculator", "Vue Component", "Main analysis interface with drag-and-drop grouping")
    Component(home_page, "Home Page", "Vue Component", "Landing page and navigation")
    Component(db_combiner, "Database Combiner", "Vue Component", "Interface for combining multiple data sources")
    Component(api_service, "API Service", "JavaScript Module", "Centralized HTTP client for backend communication")
    Component(draggable, "Vue Draggable", "Third-party Component", "Drag-and-drop functionality for factor grouping")
    Component(bootstrap, "Bootstrap UI", "CSS Framework", "Responsive UI components and styling")
}

Rel(router, upload_page, "Routes to")
Rel(router, factor_calc, "Routes to")
Rel(router, home_page, "Routes to")
Rel(router, db_combiner, "Routes to")
Rel(upload_page, api_service, "Uploads files")
Rel(factor_calc, api_service, "Calculates statistics")
Rel(factor_calc, draggable, "Uses for grouping")
Rel(db_combiner, api_service, "Fetches data")
Rel(api_service, api, "HTTP requests", "JSON/HTTPS")

@enduml
```

### Backend Components (FastAPI API Server)

```plantuml
@startuml C4_Component_Backend
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

title Component Diagram - FastAPI Backend

ContainerDb(file_storage, "File Storage")
ContainerDb(redis_cache, "Redis Cache")
ContainerDb(database, "MongoDB")
Container_Ext(arpy, "ArpY Module")

Container_Boundary(api, "API Server") {
    Component(main_app, "FastAPI Application", "FastAPI", "Main application instance with middleware and routing")
    Component(api_router, "API Router", "FastAPI Router", "Groups all API endpoints under /api prefix")
    Component(cors_middleware, "CORS Middleware", "FastAPI Middleware", "Handles cross-origin requests from frontend")
    Component(static_middleware, "Static Files Middleware", "FastAPI", "Serves frontend assets and uploaded files")
    Component(upload_handler, "File Upload Handler", "FastAPI Endpoint", "Processes Excel/CSV file uploads")
    Component(factor_endpoints, "Factor Group Endpoints", "FastAPI Endpoints", "Manages factor group creation and storage")
    Component(calc_endpoints, "Calculation Endpoints", "FastAPI Endpoints", "Handles Cronbach's alpha calculations")
    Component(data_fetcher, "Data Fetcher", "ArpY Integration", "Retrieves data from external research systems")
    Component(score_calculator, "Score Calculator", "Python Module", "Statistical calculation functions")
    Component(upload_functions, "Upload Functions", "Python Module", "File processing and validation utilities")
    Component(templates, "Jinja2 Templates", "Template Engine", "Server-side HTML templating")
}

Rel(main_app, api_router, "Includes")
Rel(main_app, cors_middleware, "Uses")
Rel(main_app, static_middleware, "Uses")
Rel(main_app, templates, "Uses")
Rel(api_router, upload_handler, "Routes to")
Rel(api_router, factor_endpoints, "Routes to")
Rel(api_router, calc_endpoints, "Routes to")
Rel(upload_handler, upload_functions, "Uses")
Rel(upload_handler, file_storage, "Saves files to")
Rel(factor_endpoints, database, "Stores groups in")
Rel(calc_endpoints, score_calculator, "Uses")
Rel(calc_endpoints, redis_cache, "Caches results in")
Rel(data_fetcher, arpy, "Fetches data from")
Rel(data_fetcher, database, "Queries")

@enduml
```

### Statistical Functions Component

```plantuml
@startuml C4_Component_Statistics
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

title Component Diagram - Statistical Functions

Container(api_endpoints, "API Endpoints")

Container_Boundary(stats, "Statistical Functions") {
    Component(cronbach_alpha, "Cronbach's Alpha Calculator", "Python Function", "Calculates reliability coefficient for item groups")
    Component(descriptive_stats, "Descriptive Statistics", "Python Function", "Computes mean, variance, std deviation")
    Component(correlation_matrix, "Correlation Matrix", "Python Function", "Calculates inter-item correlations")
    Component(item_analysis, "Item Analysis", "Python Function", "Item-total correlations and item statistics")
    Component(data_validator, "Data Validator", "Python Function", "Validates input data quality and format")
    Component(result_formatter, "Result Formatter", "Python Function", "Formats statistical output for API response")
}

ComponentDb(pandas, "Pandas", "Python Library", "Data manipulation and analysis")
ComponentDb(numpy, "NumPy", "Python Library", "Numerical computing and statistics")
ComponentDb(polars, "Polars", "Python Library", "High-performance data processing")

Rel(api_endpoints, cronbach_alpha, "Calls")
Rel(api_endpoints, descriptive_stats, "Calls")
Rel(api_endpoints, correlation_matrix, "Calls")
Rel(api_endpoints, item_analysis, "Calls")
Rel(cronbach_alpha, data_validator, "Validates input")
Rel(cronbach_alpha, result_formatter, "Formats output")
Rel(cronbach_alpha, pandas, "Uses")
Rel(cronbach_alpha, numpy, "Uses")
Rel(descriptive_stats, polars, "Uses")
Rel(correlation_matrix, pandas, "Uses")

@enduml
```

---

## Level 4: Code Diagram (Example)

```plantuml
@startuml C4_Code_CronbachAlpha
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

title Code Diagram - Cronbach's Alpha Function

Container_Boundary(cronbach_function, "cronbach_alpha Function") {
    Component(input_validation, "Input Validation", "Python Code", "Validates DataFrame has >= 2 columns and sufficient data")
    Component(variance_calculation, "Variance Calculation", "Python Code", "Calculates item variances and total variance")
    Component(alpha_formula, "Alpha Formula", "Python Code", "Applies Cronbach's alpha mathematical formula")
    Component(error_handling, "Error Handling", "Python Code", "Handles edge cases and returns appropriate errors")
    Component(result_rounding, "Result Rounding", "Python Code", "Rounds result to 3 decimal places")
}

ComponentDb(pandas_df, "pandas.DataFrame", "Data Structure", "Input data with items as columns, observations as rows")
ComponentDb(numpy_calc, "numpy calculations", "Mathematical Operations", "Statistical computations")

Rel(pandas_df, input_validation, "Input")
Rel(input_validation, variance_calculation, "Valid data")
Rel(variance_calculation, alpha_formula, "Variance values")
Rel(alpha_formula, result_rounding, "Raw alpha value")
Rel(result_rounding, "Float", "Final result")
Rel(variance_calculation, numpy_calc, "Uses")
Rel(alpha_formula, numpy_calc, "Uses")
Rel(input_validation, error_handling, "On validation failure")

@enduml
```

---

## Technology Stack Summary

### Frontend Technologies
- **Vue.js 3**: Progressive JavaScript framework for building user interfaces
- **Vue Router**: Client-side routing for single-page application navigation
- **Bootstrap 5**: CSS framework for responsive design and UI components
- **Vue Draggable**: Drag-and-drop functionality for factor grouping
- **Vite**: Build tool and development server
- **Vitest**: Unit testing framework

### Backend Technologies
- **FastAPI**: Modern Python web framework for building APIs
- **Python 3.13+**: Core programming language
- **Uvicorn**: ASGI server for FastAPI applications
- **Pydantic**: Data validation using Python type annotations
- **Jinja2**: Template engine for server-side rendering

### Data Processing
- **Pandas**: Data manipulation and analysis library
- **Polars**: High-performance DataFrame library
- **NumPy**: Numerical computing library
- **OpenPyXL**: Excel file reading/writing

### Infrastructure
- **Redis**: In-memory caching and session storage
- **MongoDB**: Document database for persistent storage
- **ArpY**: Custom research data processing module

### Development Tools
- **ESLint**: JavaScript linting
- **Prettier**: Code formatting
- **UV**: Python dependency management
- **Git**: Version control

---

## API Endpoints Overview

### File Upload Endpoints
- `POST /api/upload` - Upload Excel/CSV files
- `GET /api/files/{file_id}` - Download uploaded files

### Factor Analysis Endpoints
- `POST /api/save-factor-groups` - Save factor group configurations
- `GET /api/get-display-data` - Retrieve factor group data
- `POST /api/calculate-cronbach-alpha` - Calculate Cronbach's alpha for specific groups
- `POST /api/calculate-all-groups-scores` - Calculate statistics for all groups

### Generic Function Endpoints
- `GET /api/functions` - List available statistical functions
- `POST /api/call-function` - Execute any registered statistical function

### Static Content
- `/static/*` - Serve frontend application assets
- `/staticFirstPage/*` - Serve landing page assets
- `/creating-factor-groups` - Serve Vue.js application

---

## Data Flow

1. **File Upload**: User uploads Excel/CSV data through Vue.js frontend
2. **Data Processing**: FastAPI processes and validates the uploaded data
3. **Factor Grouping**: User organizes survey items into factor groups using drag-and-drop interface
4. **Statistical Analysis**: Backend calculates Cronbach's alpha and other statistics
5. **Results Display**: Computed statistics are displayed in the frontend interface
6. **Data Persistence**: Factor groups and results are stored in MongoDB
7. **Caching**: Frequently accessed data is cached in Redis for performance

---

## Security Considerations

- **CORS Configuration**: Restricts frontend origins for API access
- **Input Validation**: Pydantic models validate all API inputs
- **File Upload Security**: File type and size restrictions on uploads
- **Error Handling**: Secure error messages without sensitive information exposure

---

## Deployment Architecture

The application is designed for local development with considerations for portability:

- **Development**: Local servers (Vue dev server + FastAPI)
- **Production**: Static frontend served by FastAPI with reverse proxy support
- **Database**: External MongoDB and Redis instances
- **File Storage**: Local filesystem with potential for cloud storage migration

This C4 model provides a comprehensive view of the Cronbach's Alpha Web Application architecture, from high-level system context down to specific code implementations, facilitating understanding for developers, architects, and stakeholders.