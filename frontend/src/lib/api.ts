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

    try {
      console.log(`Making request to: ${API_BASE_URL}${endpoint}`);
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
      });

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
      console.error('API request failed:', error);
      throw error;
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
      throw new Error(`Request failed with status ${response.status}`);
    }

    const result = await response.json();
    console.log(`POST response data:`, result);
    return result;
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