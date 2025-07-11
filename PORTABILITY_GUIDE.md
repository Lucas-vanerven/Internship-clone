# Portability Guide for Cronbach WebApp

This document outlines the changes needed to make the Cronbach WebApp portable across different environments and organizations.

## 🔧 Required Changes for Portability

### 1. Frontend Configuration (`frontend/`)

#### Environment Variables
Create a `.env.local` file from `.env.example`:
```bash
cp .env.example .env.local
```

#### Update API Service (`src/services/apiService.js`)
- ✅ **COMPLETED**: Added TODO comments for hardcoded localhost URLs
- **Action needed**: Replace hardcoded URL with environment variable:
```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
```

#### Update Vue Components
- ✅ **COMPLETED**: Added TODO comments in `HomePage.vue`
- **Action needed**: Replace direct fetch calls with environment variables

#### Vite Configuration (`vite.config.js`)
- ✅ **COMPLETED**: Added TODO comments for build paths
- **Action needed**: Make build output and base paths configurable

### 2. Backend Configuration (`backend/`)

#### Environment Variables
Create a `.env` file from the root `.env.example`:
```bash
cp .env.example .env
```

#### Update Main Application (`main.py`)
- ✅ **COMPLETED**: Added TODO comments for:
  - CORS origins configuration
  - Static file paths (Windows-specific backslashes)
  - Host/port configuration
  - File path handling

#### Required Changes:
```python
import os
from pathlib import Path

# Use environment variables
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8000))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

# Use cross-platform paths
FRONTEND_DIST = Path(project_directory) / "frontend" / "dist"
```

### 3. ArpY Module Dependencies

The ArpY module requires several environment variables that are currently hardcoded to localhost:

#### Files with localhost references:
- ✅ **IDENTIFIED**: `ArpY/.github/workflows/full-workflow.yml` (line 239-240)
- ✅ **IDENTIFIED**: `ArpY/rainbow/__init__.py` (Redis configuration)
- ✅ **IDENTIFIED**: `ArpY/tests/project/test_data_fetcher.py` (line 18)
- ✅ **IDENTIFIED**: `ArpY/tests/test_init.py` (line 27)

#### Required Environment Variables:
```bash
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
MONGO_CONNECTION_URI=mongodb://localhost:27017/
INTERNAL_DATA_FETCHER_URL=http://localhost:18909
```

### 4. Build Assets

#### Compiled Frontend Assets
- ✅ **IDENTIFIED**: `backend/dist/static/assets/index-DBlrQVjQ.js` contains hardcoded `127.0.0.1`
- **Action needed**: Rebuild frontend after implementing environment variables

## 🚀 Deployment Checklist

### Before Transferring Repository:

- [ ] Update all hardcoded URLs to use environment variables
- [ ] Create comprehensive `.env.example` files
- [ ] Update `vite.config.js` to use environment variables
- [ ] Fix Windows-specific file paths in `backend/main.py`
- [ ] Update CORS configuration to be environment-based
- [ ] Document all required environment variables
- [ ] Test build process in clean environment
- [ ] Update ArpY configuration for new environment

### After Repository Transfer:

- [ ] Create `.env` files from examples
- [ ] Update environment variables for new infrastructure
- [ ] Install dependencies (`npm install`, `pip install -r requirements.txt`)
- [ ] Build frontend with new configuration
- [ ] Test all API endpoints
- [ ] Verify ArpY module functionality (if used)

## 📝 Additional Recommendations

1. **Containerization**: Consider adding Docker configuration for consistent deployment
2. **CI/CD**: Update GitHub Actions workflows for new organization
3. **Documentation**: Create setup instructions for new team members
4. **Testing**: Add environment-specific test configurations
5. **Security**: Review and update any hardcoded credentials or API keys

## 🔍 Quick Search Commands

To find remaining hardcoded references:
```bash
# Search for localhost references
grep -r "localhost" --exclude-dir=node_modules --exclude-dir=.git .

# Search for 127.0.0.1 references  
grep -r "127.0.0.1" --exclude-dir=node_modules --exclude-dir=.git .

# Search for hardcoded ports
grep -r ":8000\|:5173\|:6379\|:27017" --exclude-dir=node_modules --exclude-dir=.git .
```
