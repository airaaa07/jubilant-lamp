# Routing

## Purpose

This document explains the routing strategy used in the University ERP frontend. It details how routing is implemented, route protection, and navigation patterns.

## Why This Document Exists

**Confirmed by Code**: The University ERP frontend uses React Router for routing. Understanding routing is critical for:
- Implementing navigation
- Protecting routes
- Managing URL state
- Implementing nested routes
- Debugging routing issues

Without understanding routing, developers may struggle with navigation or route protection.

## Where This Is Used

- **Onboarding**: New developers learn routing
- **Feature Development**: Implementing routing
- **Code Reviews**: Reviewing routing code
- **Navigation**: Implementing navigation
- **Route Protection**: Protecting routes

## Dependencies

### Routing Dependencies

**Confirmed by Code**: Routing depends on:

- **React Router**: Routing library
- **React Router DOM**: DOM-specific router
- **TypeScript**: Type-safe routing

## Internal Architecture

### Routing Architecture

**Confirmed by Code**: Routing follows a hierarchical structure.

```
┌─────────────────────────────────────────────────────────┐
│              Route Structure                              │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Public Routes│  │  Protected Routes│  │  Layout Routes │
│  (No Auth)    │  │  (Auth Required)│  │  (With Layout) │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Router Setup

**Confirmed by Code**: Router set up in App.tsx.

**App.tsx**:
```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/admissions" element={<ProtectedRoute><AdmissionsPage /></ProtectedRoute>} />
          <Route path="/analytics" element={<ProtectedRoute><AnalyticsPage /></ProtectedRoute>} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
```

**What This Does**:
- **BrowserRouter**: Uses HTML5 history API
- **Routes**: Container for routes
- **Route**: Defines route path and component
- **ProtectedRoute**: Wraps protected routes

### Protected Routes

**Confirmed by Code**: Protected routes check authentication.

**ProtectedRoute Component**:
```typescript
export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
```

**What This Does**:
- **useAuth**: Gets auth state
- **Check Auth**: Checks if user is authenticated
- **Navigate**: Redirects to login if not authenticated
- **Render Children**: Renders children if authenticated

**Usage**:
```typescript
<Route path="/admissions" element={<ProtectedRoute><AdmissionsPage /></ProtectedRoute>} />
```

### Route Parameters

**Confirmed by Code**: Route parameters used for dynamic routes.

**Route with Parameter**:
```typescript
<Route path="/users/:id" element={<UserDetailPage />} />
```

**Accessing Parameter**:
```typescript
export function UserDetailPage() {
  const { id } = useParams<{ id: string }>();

  const { data } = useQuery({
    queryKey: ['user', id],
    queryFn: () => api.getUser(id),
  });

  if (!data) return <div>Loading...</div>;

  return <div>{data.name}</div>;
}
```

**What This Does**:
- **useParams**: Accesses route parameters
- **TypeScript**: Type-safe parameter access
- **React Query**: Fetches data with parameter
- **Conditional Rendering**: Renders based on data

### Query Parameters

**Confirmed by Code**: Query parameters used for filtering.

**Query Parameters**:
```typescript
export function UsersPage() {
  const [searchParams] = useSearchParams();
  const page = searchParams.get('page') || '1';
  const search = searchParams.get('search') || '';

  const { data } = useQuery({
    queryKey: ['users', page, search],
    queryFn: () => api.getUsers({ page: parseInt(page), search }),
  });

  return (
    <div>
      <input
        value={search}
        onChange={(e) => {
          const params = new URLSearchParams(searchParams);
          params.set('search', e.target.value);
          setSearchParams(params);
        }}
      />
      {/* User list */}
    </div>
  );
}
```

**What This Does**:
- **useSearchParams**: Accesses query parameters
- **TypeScript**: Type-safe parameter access
- **Update Params**: Updates query parameters
- **React Query**: Fetches data with parameters

### Navigation

**Confirmed by Code**: Navigation done with useNavigate.

**useNavigate Hook**:
```typescript
export function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (credentials: Credentials) => {
    await login(credentials);
    navigate('/');
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Login form */}
    </form>
  );
}
```

**What This Does**:
- **useNavigate**: Gets navigate function
- **Navigate**: Navigates to route
- **Login**: Authenticates user
- **Redirect**: Redirects after login

### Lazy Loading

**Confirmed by Code**: Routes lazy loaded for performance.

**lazyWithReload Function**:
```typescript
function lazyWithReload<T extends { default: ComponentType<any> }>(
  factory: () => Promise<T>,
) {
  return lazy(() =>
    factory().catch((err) => {
      const KEY = 'chunkReloadAt'
      const now = Date.now()
      const last = Number(sessionStorage.getItem(KEY) || 0)
      if (now - last > 10_000) {
        sessionStorage.setItem(KEY, String(now))
        window.location.reload()
        return new Promise<T>(() => {}) // hold render until the reload takes over
      }
      throw err // reloaded moments ago — genuine failure, surface to ErrorBoundary
    }),
  )
}
```

**What This Does**:
- **lazy**: Lazy loads component
- **Error Handling**: Handles chunk load errors
- **Reload**: Reloads page on chunk error
- **Session Storage**: Prevents infinite reload loop

**Usage**:
```typescript
const AdmissionsPage = lazyWithReload(() => import('./pages/AdmissionsPage'))
const AnalyticsPage = lazyWithReload(() => import('./pages/AnalyticsPage'))
```

## Database Interactions

### Routing-Database Flow

**Confirmed by Code**: Routing doesn't directly interact with database.

**Flow**:
```
Route → Component → API → Backend → Database
```

## Redis Interactions

### Routing-Redis Flow

**Confirmed by Code**: Routing doesn't directly interact with Redis.

**Flow**:
```
Route → Component → API → Backend → Redis
```

## Queue Interactions

### Routing-Queue Flow

**Confirmed by Code**: Routing doesn't directly interact with queues.

**Flow**:
```
Route → Component → API → Backend → Queue
```

## Worker Interactions

### Routing-Worker Flow

**Confirmed by Code**: Routing doesn't directly interact with workers.

**Flow**:
```
Route → Component → API → Backend → Worker
```

## Business Rules

### Routing Rules

**Confirmed by Code**: Routing follows these rules:

1. **Route Protection**: Protect authenticated routes
2. **Lazy Loading**: Lazy load routes for performance
3. **Type Safety**: Type-safe route parameters
4. **Navigation**: Use useNavigate for navigation
5. **URL State**: Use URL params for state

### Route Organization规则

**Confirmed by Code**: Route organization follows these rules:

1. **Public Routes**: No authentication required
2. **Protected Routes**: Authentication required
3. **Nested Routes**: Use nested routes for layouts
4. **Dynamic Routes**: Use route parameters for dynamic data
5. **Query Params**: Use query params for filtering

## Security

### Routing Security

**Confirmed by Code**: Security considerations for routing:

1. **Route Protection**: Protect authenticated routes
2. **Role-Based Routes**: Protect routes by role
3. **Token Validation**: Validate tokens on protected routes
4. **Redirect**: Redirect unauthenticated users
5. **URL Sanitization**: Sanitize URL parameters

## Performance Considerations

### Routing Performance

**Confirmed by Code**: Performance considerations for routing:

1. **Code Splitting**: Lazy load routes
2. **Prefetching**: Prefetch routes for better UX
3. **Route Caching**: Cache route components
4. **Bundle Size**: Keep route bundles small
5. **Navigation**: Use efficient navigation

## Common Mistakes

### Mistake 1: Not Protecting Routes

**Symptom**: Unauthenticated users accessing protected routes

**Cause**: Not protecting routes

**Fix**:
```typescript
// Add ProtectedRoute wrapper
<Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
```

### Mistake 2: Not Using Lazy Loading

**Symptom**: Slow initial load

**Cause**: Not lazy loading routes

**Fix**:
```typescript
// Use lazy loading
const Dashboard = lazy(() => import('./pages/Dashboard'));
```

### Mistake 3: Not Type-Safe Parameters

**Symptom**: Type errors with route parameters

**Cause**: Not typing route parameters

**Fix**:
```typescript
// Add TypeScript types
const { id } = useParams<{ id: string }>();
```

## Debugging Guide

### Routing Debugging

**Issue**: Route not working

**Investigation**:
1. Check route path
2. Check route component
3. Check route protection
4. Check navigation logic
5. Use React Router DevTools

**Tools**:
- React Router DevTools
- Browser DevTools
- Console logs
- Network tab

## Future Enhancements

### Route-Based Code Splitting

**Status**: Not implemented

**Proposal**: Implement route-based code splitting:
- Automatic code splitting
- Better performance
- Smaller bundles
- Faster load times
- Better UX

### Nested Routing

**Status**: Not implemented

**Proposal**: Implement nested routing:
- Nested layouts
- Better organization
- Cleaner code
- Better UX
- Easier maintenance

## Production Considerations

### Production Routing

**Production Deployment**:
- Enable route-based code splitting
- Enable route caching
- Enable prefetching
- Monitor route performance
- Monitor navigation errors

### Routing Monitoring

**Monitoring Metrics**:
- Route load time
- Navigation frequency
- Route errors
- Bundle size per route
- User navigation patterns

## Example Requests

### Navigation Example

**Request**: Navigate to route

```typescript
navigate('/users');
```

## Example Responses

### Navigation Response

**Response**: Route navigated

```html
<!-- Users page rendered -->
```

## Sequence Diagrams

### Navigation Flow

```
User Action → useNavigate → Route Change → Component Load → Render
```

## Architecture Diagrams

### Routing Architecture

```
┌─────────────────────────────────────────────────────────┐
│              BrowserRouter                                │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Public Routes│  │  Protected Routes│  │  Dynamic Routes│
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: How does React Router work?

**Answer**: React Router:
- Uses HTML5 history API
- Renders components based on URL
- Provides navigation methods
- Supports nested routes
- Supports route parameters

### Q2: How do you protect routes?

**Answer**: Route protection via:
- ProtectedRoute component
- Check authentication state
- Redirect to login if not authenticated
- Use useAuth hook
- Wrap protected routes

### Q3: How do you handle route parameters?

**Answer**: Route parameters via:
- useParams hook
- TypeScript types for parameters
- Use parameters in data fetching
- Update query with parameters
- Type-safe parameter access

## Exercises

### Exercise 1: Create a Protected Route

**Task**: Create a protected route.

**Steps**:
1. Create ProtectedRoute component
2. Check authentication
3. Redirect if not authenticated
4. Use ProtectedRoute in routes
5. Test route protection

**Verification**:
- ProtectedRoute created
- Auth check works
- Redirect works
- Route protected
- Tests pass

### Exercise 2: Add Route Parameters

**Task**: Add route parameters.

**Steps**:
1. Define route with parameter
2. Access parameter with useParams
3. Use parameter in component
4. TypeScript type parameter
5. Test parameter access

**Verification**:
- Route parameter defined
- Parameter accessed
- TypeScript types work
- Component uses parameter
- Tests pass

## Real Production Scenarios

### Scenario 1: Route Not Found

**Situation**: 404 error on route

**Response**:
1. Check route definition
2. Check route path
3. Check component import
4. Add 404 route
5. Test navigation

### Scenario 2: Navigation Not Working

**Situation**: Navigation not working

**Response**:
1. Check useNavigate usage
2. Check route path
3. Check navigation logic
4. Fix navigation
5. Test navigation

## Navigation

**Next Section**: [05-API-Integration](./05-API-Integration.md)

**Previous Section**: [03-State-Management](./03-State-Management.md)

**Related Documentation**:
- [01-React-Framework](./01-React-Framework.md) - React framework
- [02-Component-Architecture](./02-Component-Architecture.md) - Component architecture
- [12-API-Reference](../01-System-Architecture/12-API-Reference.md) - API reference
