/**
 * API Service for Backend Communication
 * 
 * This service centralizes all HTTP communication between the Vue.js frontend
 * and the FastAPI backend server. It provides a clean, consistent interface
 * for all API operations related to Cronbach's alpha calculations and 
 * factor analysis.
 * 
 * Key Features:
 * - Centralized error handling with detailed logging
 * - Consistent request/response formatting
 * - Type-safe method signatures with JSDoc
 * - Singleton pattern for application-wide usage
 * 
 * Available Operations:
 * - Calculate Cronbach's alpha reliability for factor groups
 * - Upload and process data files
 * - Retrieve display data for factor analysis
 * - Save factor group configurations
 * - Get factorization results (future implementation)
 * 
 * Configuration:
 * - Base URL currently hardcoded (TODO: make configurable via environment variables)
 * - JSON content type default with FormData support for uploads
 * - Automatic response parsing and error extraction
 * 
 * Usage:
 * - Import as default: `import apiService from '@/services/apiService.js'`
 * - Use methods: `await apiService.calculateCronbachAlpha(taskId, groups)`
 * - Named exports available for convenience
 */

// API Service for backend communication
// This service centralizes all API calls to the backend


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
   * Calculate Cronbach's alpha for a single group
   * @param {string} taskId - Task ID
   * @param {Array<Array<string>>} groups - Array of groups with statement names
   * @returns {Promise<object>} - Cronbach's alpha result
   */
  async calculateCronbachAlpha(taskId, groups) {
    return this.makeRequest('/api/calculate-cronbach-alpha', {
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
   * Save factor groups to the backend
   * @param {string} taskId - Task ID
   * @param {string} client - Client name
   * @param {Array<Array<object>>} groups - Four groups containing statement objects
   * @returns {Promise<object>} - Save result
   */
  async saveFactorGroups(taskId, client, groups) {
    return this.makeRequest('/api/save-factor-groups', {
      method: 'POST',
      body: JSON.stringify({
        task_id: taskId,
        client: client,
        groups: groups
      })
    });
  }

}

// Create and export a singleton instance
const apiService = new ApiService();
export default apiService;

// Named exports for convenience
export const {
  calculateCronbachAlpha,
  uploadFiles,
  getFactorization,
  healthCheck,
  getDisplayData,
  saveFactorGroups
} = apiService;
