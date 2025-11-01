import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/auth/login';
    }
    return Promise.reject(error);
  }
);

// User services
export const userService = {
  register: (data: { email: string; username: string; password: string; full_name?: string }) =>
    apiClient.post('/users/register', data),
  login: (email: string, password: string) =>
    apiClient.post('/users/login', { email, password }),
  getCurrentUser: () => apiClient.get('/users/me'),
  updateProfile: (data: any) => apiClient.put('/users/me', data),
};

// Deployment services
export const deploymentService = {
  create: (data: any) => apiClient.post('/deployments', data),
  list: (skip = 0, limit = 10) =>
    apiClient.get('/deployments', { params: { skip, limit } }),
  get: (deploymentId: number) => apiClient.get(`/deployments/${deploymentId}`),
  delete: (deploymentId: number) => apiClient.delete(`/deployments/${deploymentId}`),
  rollback: (deploymentId: number) => apiClient.post(`/deployments/${deploymentId}/rollback`),
};

// Subdomain services
export const subdomainService = {
  checkAvailability: (subdomain: string) =>
    apiClient.post('/subdomains/check-availability', { subdomain }),
  get: (deploymentId: number) => apiClient.get(`/subdomains/${deploymentId}`),
};

// Monitoring services
export const monitoringService = {
  getUptime: (deploymentId: number) =>
    apiClient.get(`/monitoring/deployments/${deploymentId}/uptime`),
  getHealthChecks: (deploymentId: number, limit = 50) =>
    apiClient.get(`/monitoring/deployments/${deploymentId}/health-checks`, {
      params: { limit },
    }),
  getPerformance: (deploymentId: number, limit = 50) =>
    apiClient.get(`/monitoring/deployments/${deploymentId}/performance`, {
      params: { limit },
    }),
  triggerHealthCheck: (deploymentId: number) =>
    apiClient.post(`/monitoring/deployments/${deploymentId}/check`),
};

export default apiClient;
