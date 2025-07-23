// API Service for backend communication
// This service centralizes all API calls to the backend

// TODO: CHANGE FOR PORTABILITY - Replace hardcoded localhost URL with environment variable
// Possibly: const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
// Create .env.example with: VITE_API_BASE_URL=http://localhost:8000
const API_BASE_URL = 'http://127.0.0.1:8000';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  /**
   * Generic method to make API calls
   * @param {string} endpoint - The API endpoint
   * @param {object} options - Fetch options (method, body, headers, etc.)
   * @returns {Promise} - Promise that resolves to the response data
   */
  async makeRequest(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    };

    const requestOptions = { ...defaultOptions, ...options };

    try {
      const response = await fetch(url, requestOptions);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API Error (${endpoint}):`, error);
      throw error;
    }
  }

  /**
   * Calculate Cronbach's alpha for a single group (drag-and-drop version)
   * @param {Array<Array<number>>} groupData - 2D array of statement scores
   * @param {number} groupIndex - Index of the group
   * @returns {Promise<object>} - Cronbach's alpha result
   */
  async calculateCronbachAlpha(groupData, groupIndex) {
    //TODO: Change the data structure to match the ScoreCalculationRequest's - use the same method as you did to retrieve the data for the drag-and-drop
    return this.makeRequest('/api/calculate-cronbach-alpha-dragdrop', {
      method: 'POST',
      body: JSON.stringify({
        group_data: groupData,
        group_index: groupIndex
      })
    });
  }

  /**
   * Calculate Cronbach's alpha for all groups
   * @param {Array<Array<Array<number>>>} groups - Array of groups with statement scores
   * @returns {Promise<object>} - Results for all groups
   */
  async calculateAllGroupsScores(groups) {
    const taskId = document.location.href
      .split('/')
      .pop()

    return this.makeRequest('/api/calculate-all-groups-scores', {
      method: 'POST',
      body: JSON.stringify({
        task_id: taskId,
        groups: groups
      })
    });
  }

  /**
   * Upload files (existing functionality)
   * @param {FormData} formData - Form data containing files
   * @returns {Promise<object>} - Upload result
   */
  async uploadFiles(formData) {
    return this.makeRequest('/databaseCombiner/api/job/create', {
      method: 'POST',
      body: formData,
      headers: {} // Don't set Content-Type for FormData, let browser set it
    });
  }

  /**
   * Get factorization data (placeholder for future implementation)
   * @param {string} id - Job/analysis ID
   * @returns {Promise<object>} - Factorization data
   */
  async getFactorization(id) {
    return this.makeRequest(`/api/factorization/${id}`, {
      method: 'GET'
    });
  }

  /**
   * Health check endpoint
   * @returns {Promise<object>} - Health status
   */
  async healthCheck() {
    return this.makeRequest('/', {
      method: 'GET'
    });
  }

  /**
   * List all available functions from backend/functions modules
   * @returns {Promise<object>} - Available functions
   */
  async listAvailableFunctions() {
    return this.makeRequest('/api/functions', {
      method: 'GET'
    });
  }

  /**
   * Call any function from backend/functions modules
   * @param {string} functionName - Name of the function to call
   * @param {object} parameters - Parameters to pass to the function
   * @returns {Promise<object>} - Function result
   */

  /** how to call a function when creating a new one */
  async callFunction(functionName, parameters) {
    return this.makeRequest('/api/call-function', {
      method: 'POST',
      body: JSON.stringify({
        function_name: functionName,
        parameters: parameters
      })
    });
  }

  /**
   * Get display data from the backend
   * @param {string} taskId - Task ID
   * @param {string} client - Client name
   * @returns {Promise<Array>} - Array of DisplayDataResponse objects
   */
  async getDisplayData(taskId, client) {
    return this.makeRequest(`/api/get-display-data?task_id=${taskId}&client=${client}`, {
      method: 'GET'
    });
  }

  /**
   * Convenience method to call cronbach_alpha specifically
   * @param {Array<Array<number>>} groupData - 2D array of statement scores
   * @returns {Promise<object>} - Cronbach's alpha result
   */
  async callCronbachAlpha(groupData) {
    return this.callFunction('cronbach_alpha', {
      group_data: groupData
    });
  }
}

// Create and export a singleton instance
const apiService = new ApiService();
export default apiService;

// Named exports for convenience
export const {
  calculateCronbachAlpha,
  calculateAllGroupsScores,
  uploadFiles,
  getFactorization,
  healthCheck,
  listAvailableFunctions,
  callFunction,
  callCronbachAlpha,
  getDisplayData
} = apiService;
