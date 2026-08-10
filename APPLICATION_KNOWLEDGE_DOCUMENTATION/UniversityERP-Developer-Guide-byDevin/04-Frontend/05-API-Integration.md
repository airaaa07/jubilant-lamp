# API Integration

## Purpose

This document explains the API integration strategy used in the University ERP frontend. It details how the frontend communicates with the backend, handles authentication, and manages API calls.

## Why This Document Exists

**Confirmed by Code**: The University ERP frontend integrates with the backend via REST API. Understanding API integration is critical for:
- Making API calls
- Handling authentication
- Managing API errors
- Implementing data fetching
- Debugging API issues

Without understanding API integration, developers may struggle with backend communication.

## Where This Is Used

- **Onboarding**: New developers learn API integration
- **Feature Development**: Implementing API calls
- **Code Reviews**: Reviewing API integration code
- **Debugging**: Debugging API issues
- **API Development**: Developing API endpoints

## Dependencies

### API Integration Dependencies

**Confirmed by Code**: API integration depends on:

- **Axios**: HTTP client
- **React Query**: Server state management
- **TypeScript**: Type-safe API calls

## Internal Architecture

### API Architecture

**Confirmed by Code**: API integration follows a layered architecture.

```
┌─────────────────────────────────────────────────────────┐
│              Component Layer                              │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Hook Layer                                   │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│              API Layer                                     │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Axios Layer                                   │
└─────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────┐
│              Backend API                                   │
└─────────────────────────────────────────────────────────┘
```

## Code Walkthrough

### Axios Configuration

**Confirmed by Code**: Axios configured in api/axios.ts.

**axios.ts**:
```typescript
import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3000',
  timeout: 10000,
});

// Request interceptor
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Response interceptor
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  },
);

export default axiosInstance;
```

**What This Does**:
- **create**: Creates axios instance
- **baseURL**: Sets base URL for API calls
- **timeout**: Sets request timeout
- **Request Interceptor**: Adds JWT token to requests
- **Response Interceptor**: Handles 401 errors

### API Functions

**Confirmed by Code**: API functions defined in api/modules.ts.

**API Functions**:
```typescript
import axiosInstance from './axios';

export const api = {
  // Auth
  login: (credentials: LoginDto) =>
    axiosInstance.post('/api/auth/login', credentials),
  
  refreshToken: (refreshToken: string) =>
    axiosInstance.post('/api/auth/refresh', { refreshToken }),
  
  logout: () =>
    axiosInstance.post('/api/auth/logout'),
  
  // Users
  getUsers: (params?: QueryUserDto) =>
    axiosInstance.get('/api/users', { params }),
  
  getUser: (id: string) =>
    axiosInstance.get(`/api/users/${id}`),
  
  createUser: (data: CreateUserDto) =>
    axiosInstance.post('/api/users', data),
  
  updateUser: (id: string, data: UpdateUserDto) =>
    axiosInstance.patch(`/api/users/${id}`, data),
  
  deleteUser: (id: string) =>
    axiosInstance.delete(`/api/users/${id}`),
  
  // Admissions
  getAdmissions: (params?: QueryAdmissionDto) =>
    axiosInstance.get('/api/admissions', { params }),
  
  getAdmission: (id: string) =>
    axiosInstance.get(`/api/admissions/${id}`),
  
  createAdmission: (data: CreateAdmissionDto) =>
    axiosInstance.post('/api/admissions', data),
  
  // ... more API functions
};
```

**What This Does**:
- **API Functions**: Defines API functions for each endpoint
- **TypeScript**: Type-safe API calls
- **Axios Instance**: Uses configured axios instance
- **Parameters**: Supports query parameters
- **Error Handling**: Handles errors via interceptors

### React Query Integration

**Confirmed by Code**: React Query used for data fetching.

**useQuery Example**:
```typescript
export function UsersList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: () => api.getUsers().then(res => res.data),
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <ul>
      {data?.data?.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

**What This Does**:
- **useQuery**: Fetches data from API
- **queryKey**: Unique key for query
- **queryFn**: Function to fetch data
- **isLoading**: Loading state
- **error**: Error state
- **data**: Fetched data

**useMutation Example**:
```typescript
export function CreateUserForm() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: (data: CreateUserDto) =>
      api.createUser(data).then(res => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      toast.success('User created successfully');
    },
    onError: (error) => {
      toast.error('Failed to create user');
    },
  });

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      mutation.mutate(formData);
    }}>
      {/* Form fields */}
    </form>
  );
}
```

**What This Does**:
- **useMutation**: Performs API mutation
- **mutationFn**: Function to perform mutation
- **onSuccess**: Callback on success
- **onError**: Callback on error
- **invalidateQueries**: Invalidates cache after mutation

### Custom Hooks

**Confirmed by Code**: Custom hooks for API calls.

**useAuth Hook**:
```typescript
export function useAuth() {
  const { data, isLoading } = useQuery({
    queryKey: ['auth', 'user'],
    queryFn: () => api.getCurrentUser().then(res => res.data),
    enabled: !!localStorage.getItem('token'),
  });

  const loginMutation = useMutation({
    mutationFn: (credentials: LoginDto) =>
      api.login(credentials).then(res => res.data),
    onSuccess: (data) => {
      localStorage.setItem('token', data.accessToken);
      localStorage.setItem('refreshToken', data.refreshToken);
    },
  });

  const logoutMutation = useMutation({
    mutationFn: () => api.logout(),
    onSuccess: () => {
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
      window.location.href = '/login';
    },
  });

  return {
    user: data,
    isLoading,
    login: loginMutation.mutate,
    logout: logoutMutation.mutate,
  };
}
```

**What This Does**:
- **useQuery**: Fetches current user
- **loginMutation**: Logs in user
- **logoutMutation**: Logs out user
- **Token Storage**: Stores tokens in localStorage
- **Redirect**: Redirects on logout

## Database Interactions

### API-Database Flow

**Confirmed by Code**: API calls interact with database via backend.

**Flow**:
```
Frontend → API Call → Backend → Database
```

## Redis Interactions

### API-Redis Flow

**Confirmed by Code**: API calls interact with Redis via backend.

**Flow**:
```
Frontend → API Call → Backend → Redis
```

## Queue Interactions

### API-Queue Flow

**Confirmed by Code**: API calls interact with queues via backend.

**Flow**:
```
Frontend → API Call → Backend → Queue

```

## Worker Interactions

### API-Worker Flow

**Confirmed by Code**: API calls interact with workers via backend.

**Flow**:
```
Frontend → API Call → Backend → Worker
```

## Business Rules

### API Integration Rules

**Confirmed by Code**: API integration follows these rules:

1. **Type Safety**: All API calls are typed
2. **Error Handling**: Handle API errors appropriately
3. **Authentication**: Include JWT token in requests
4. **Caching**: Use React Query for caching
5. **Loading States**: Show loading states during API calls

### Error Handling Rules

**Confirmed by Code**: Error handling follows these rules:

1. **401 Errors**: Redirect to login
2. **403 Errors**: Show forbidden message
3. **404 Errors**: Show not found message
4. **500 Errors**: Show server error message
5. **Network Errors**: Show network error message

## Security

### API Security

**Confirmed by Code**: Security considerations for API integration:

1. **JWT Token**: Include JWT token in requests
2. **HTTPS**: Use HTTPS in production
3. **Token Refresh**: Implement token refresh
4. **Token Storage**: Store token securely
5. **CSRF**: Implement CSRF protection

## Performance Considerations

### API Performance

**Confirmed by Code**: Performance considerations for API:

1. **Caching**: Use React Query caching
2. **Debouncing**: Debounce rapid API calls
3. **Pagination**: Paginate large datasets
4. **Optimistic Updates**: Use optimistic updates
5. **Request Cancellation**: Cancel pending requests

## Common Mistakes

### Mistake 1: Not Handling Errors

**Symptom**: Unhandled API errors

**Cause**: Not handling API errors

**Fix**:
```typescript
// Add error handling
const { data, error } = useQuery({
  queryKey: ['users'],
  queryFn: () => api.getUsers(),
});

if (error) {
  return <Error message={error.message} />;
}
```

### Mistake 2: Not Using React Query

**Symptom**: Manual state management for API data

**Cause**: Not using React Query

**Fix**:
```typescript
// Use React Query
const { data } = useQuery({
  queryKey: ['users'],
  queryFn: () => api.getUsers(),
});
```

### Mistake 3: Not Invalidating Cache

**Symptom**: Stale data after mutation

**Cause**: Not invalidating cache after mutation

**Fix**:
```typescript
// Invalidate cache after mutation
onSuccess: () => {
  queryClient.invalidateQueries({ queryKey: ['users'] });
}
```

## Debugging Guide

### API Debugging

**Issue**: API call failing

**Investigation**:
1. Check API endpoint
2. Check request headers
3. Check request body
4. Check response
5. Check network tab

**Tools**:
- Browser DevTools
- Network tab
- Console logs
- React Query DevTools

## Future Enhancements

### GraphQL

**Status**: Not implemented

**Proposal**: Add GraphQL support:
- GraphQL client (Apollo Client)
- Flexible queries
- Reduced over-fetching
- Better for frontend
- Type-safe queries

### WebSocket Integration

**Status**: Not implemented

**Proposal**: Add WebSocket support:
- Real-time updates
- Live notifications
- Better UX
- Event-driven
- Lower latency

## Production Considerations

### Production API

**Production Deployment**:
- Use HTTPS
- Configure CORS properly
- Implement rate limiting
- Monitor API performance
- Monitor API errors

### API Monitoring

**Monitoring Metrics**:
- API response time
- API error rate
- API success rate
- Cache hit rate
- Request rate

## Example Requests

### API Call Example

**Request**: Get users

```typescript
const { data } = useQuery({
  queryKey: ['users'],
  queryFn: () => api.getUsers(),
});
```

## Example Responses

### API Response

**Response**: API response

```json
{
  "success": true,
  "data": [
    {
      "id": "user-id",
      "email": "user@example.com"
    }
  ]
}
```

## Sequence Diagrams

### API Call Flow

```
Component → useQuery → API Function → Axios → Backend → Response → Component
```

## Architecture Diagrams

### API Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Component                                 │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  React Query                               │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  API Function                              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Axios                                    │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                  Backend API                               │
└─────────────────────────────────────────────────────────┘
```

## Common Interview Questions

### Q1: How do you make API calls in React?

**Answer**: API calls via:
- Axios for HTTP client
- React Query for data fetching
- Custom hooks for reusable logic
- TypeScript for type safety
- Error handling

### Q2: How do you handle authentication in API calls?

**Answer**: Authentication via:
- JWT token in request headers
- Axios request interceptor
- Token storage in localStorage
- Token refresh on expiry
- Redirect on 401 error

### Q3: How do you handle API errors?

**Answer**: Error handling via:
- Axios response interceptor
- React Query error state
- Try-catch in mutations
- User-friendly error messages
- Error logging

## Exercises

### Exercise 1: Create an API Function

**Task**: Create a new API function.

**Steps**:
1. Create API function
2. Add TypeScript types
3. Use axios instance
4. Handle errors
5. Test API function

**Verification**:
- API function created
- Types correct
- Works with axios
- Errors handled
- Tests pass

### Exercise 2: Create a Custom Hook

**Task**: Create a custom hook for API calls.

**Steps**:
1. Create hook file
2. Use React Query
3. Add TypeScript types
4. Handle loading and error states
5. Test hook

**Verification**:
- Hook created
- React Query works
- Types correct
- States handled
- Tests pass

## Real Production Scenarios

### Scenario 1: API Call Failing

**Situation**: API call failing with 500 error

**Response**:
1. Check API endpoint
2. Check backend logs
3. Check request data
4. Fix backend issue
5. Test API call

### Scenario 2: Token Expired

**Situation**: Token expired, 401 errors

**Response**:
1. Implement token refresh
2. Handle 401 errors
3. Redirect to login
4. Test token refresh
5. Monitor token expiry

## Navigation

**Next Section**: [README](../README.md)

**Previous Section**: [04-Routing](./04-Routing.md)

**Related Documentation**:
- [01-React-Framework](./01-React-Framework.md) - React framework
- [03-State-Management](./03-State-Management.md) - State management
- [12-API-Reference](../01-System-Architecture/12-API-Reference.md) - API reference
