// src/lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = {
  async request(endpoint: string, options: RequestInit = {}) {
    const token = localStorage.getItem('token');

    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...options.headers,
    };

    // Set default timeout of 30 seconds if not specified
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000);

    try {
      console.log(`Making request to: ${API_BASE_URL}${endpoint}`);

      const requestOptions: RequestInit = {
        ...options,
        headers,
        signal: controller.signal // Add abort signal for timeout
      };

      const response = await fetch(`${API_BASE_URL}${endpoint}`, requestOptions);

      clearTimeout(timeoutId);
      console.log(`Response status: ${response.status}`);

      // If response is 401, redirect to login
      if (response.status === 401) {
        localStorage.removeItem('token');
        window.location.href = '/login';
        return null; // Return null to indicate unauthorized
      }

      // Return the response object so the caller can handle it appropriately
      return response;
    } catch (error) {
      clearTimeout(timeoutId);

      if ((error as Error).name === 'AbortError') {
        console.error('API request timed out:', endpoint);
        throw new Error(`Request to ${endpoint} timed out`);
      }

      console.error('API request failed:', error);
      throw error;
    } finally {
      // Cleanup: Ensure timeout is cleared even if there are other issues
      clearTimeout(timeoutId);
    }
  },

  async get(endpoint: string) {
    const response = await this.request(endpoint, { method: 'GET' });
    if (!response) return null; // Handle unauthorized case

    if (!response.ok) {
      console.error(`GET request failed with status: ${response.status}`);
      throw new Error(`Request failed with status ${response.status}`);
    }

    const data = await response.json();
    console.log(`GET response data:`, data);
    return data;
  },

  async post(endpoint: string, data: any) {
    console.log(`POST request to ${endpoint} with data:`, data);
    const response = await this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
    if (!response) return null; // Handle unauthorized case

    if (!response.ok) {
      console.error(`POST request failed with status: ${response.status}`);
      const errorText = await response.text();
      console.error('Error response:', errorText);
      throw new Error(`Request failed with status ${response.status}: ${errorText}`);
    }

    // Check if response body is empty
    const responseBody = await response.text();
    console.log(`Raw POST response text:`, responseBody);

    if (!responseBody || responseBody.trim() === '') {
      console.warn(`Empty response body for POST request to ${endpoint}`);
      return {}; // Return empty object for empty responses
    }

    try {
      const result = JSON.parse(responseBody);
      console.log(`POST parsed response data:`, result);
      return result;
    } catch (parseError) {
      console.error(`Failed to parse JSON response:`, parseError);
      console.error(`Raw response:`, responseBody);

      // If we can't parse the JSON, return the raw text as an error response
      throw new Error(`Invalid JSON response from server: ${responseBody}`);
    }
  },

  async put(endpoint: string, data: any) {
    const response = await this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
    if (!response) return null; // Handle unauthorized case

    if (!response.ok) {
      console.error(`PUT request failed with status: ${response.status}`);
      const errorText = await response.text();
      console.error('Error response:', errorText);
      throw new Error(`Request failed with status ${response.status}`);
    }

    const result = await response.json();
    console.log(`PUT response data:`, result);
    return result;
  },

  async patch(endpoint: string, data: any) {
    const response = await this.request(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
    if (!response) return null; // Handle unauthorized case

    if (!response.ok) {
      console.error(`PATCH request failed with status: ${response.status}`);
      const errorText = await response.text();
      console.error('Error response:', errorText);
      throw new Error(`Request failed with status ${response.status}`);
    }

    const result = await response.json();
    console.log(`PATCH response data:`, result);
    return result;
  },

  async delete(endpoint: string) {
    const response = await this.request(endpoint, { method: 'DELETE' });
    if (!response) return null; // Handle unauthorized case

    if (!response.ok) {
      console.error(`DELETE request failed with status: ${response.status}`);
      const errorText = await response.text();
      console.error('Error response:', errorText);
      throw new Error(`Request failed with status ${response.status}`);
    }

    // DELETE requests typically don't return JSON, so just return success
    console.log(`DELETE request successful`);
    return { success: true };
  },
};