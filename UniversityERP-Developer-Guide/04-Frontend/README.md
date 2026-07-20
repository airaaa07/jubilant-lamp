# 04-Frontend

## Purpose

This folder provides comprehensive documentation about the frontend architecture of the University ERP system. It explains the React application, component structure, state management, routing, and frontend patterns.

## Why This Folder Exists

**Confirmed by Code**: The University ERP frontend is built with React 19. Understanding the frontend architecture is critical for:
- Developing frontend features
- Understanding component structure
- Implementing state management
- Integrating with backend APIs
- Debugging frontend issues

Without understanding the frontend architecture, developers may struggle to implement features correctly or may introduce bugs.

## Where This Is Used

- **Onboarding**: New developers learn frontend architecture
- **Feature Development**: Implementing frontend features
- **Code Reviews**: Understanding frontend code
- **Debugging**: Debugging frontend issues
- **Architecture Reviews**: Evaluating frontend architecture

## Dependencies

### Frontend Dependencies

**Confirmed by Code**: The frontend depends on:

- **React 19**: UI library
- **TypeScript 6.x**: Type-safe JavaScript
- **Vite**: Build tool and dev server
- **React Router**: Routing library
- **React Query**: Server state management
- **Axios**: HTTP client
- **Tailwind CSS**: CSS framework
- **Lucide React**: Icon library

## Internal Architecture

### Frontend Architecture

**Confirmed by Code**: The frontend follows React architecture.

```
┌─────────────────────────────────────────────────────────┐
│                  React Application                         │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Components   │  │  Pages          │  │  Layouts       │
│  (Reusable)   │  │  (Routes)       │  │  (Structure)   │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Hooks        │  │  Contexts       │  │  API           │
│  (Logic)      │  │  (State)        │  │  (Backend)     │
└────────────────┘  └────────────────┘  └─────────────────┘
```

### Directory Structure

**Confirmed by Code**: Frontend organized in web/admin-portal.

```
web/admin-portal/
├── src/
│   ├── api/              # API layer
│   │   ├── axios.ts      # Axios configuration
│   │   ├── auth.ts       # Authentication API
│   │   └── modules.ts    # Module-specific APIs
│   ├── components/       # Reusable components
│   │   ├── Modal.tsx
│   │   ├── Table.tsx
│   │   ├── Spinner.tsx
│   │   └── SearchBar.tsx
│   ├── contexts/         # React contexts
│   │   ├── AuthContext.tsx
│   │   ├── ThemeContext.tsx
│   │   └── StudentStatusContext.tsx
│   ├── hooks/            # Custom hooks
│   │   ├── useAuth.ts
│   │   └── useApi.ts
│   ├── lib/              # Utilities
│   │   └── utils.ts
│   ├── pages/            # Page components
│   │   ├── AdmissionsPage.tsx
│   │   ├── AnalyticsPage.tsx
│   │   ├── AttendancePage.tsx
│   │   └── ...
│   ├── types/            # TypeScript types
│   │   └── index.ts
│   ├── App.tsx           # Main app component
│   └── main.tsx          # Entry point
├── public/               # Static assets
├── index.html            # HTML template
├── vite.config.ts        # Vite configuration
├── tailwind.config.js    # Tailwind configuration
└── tsconfig.json         # TypeScript configuration
```

## Code Walkthrough

### Application Bootstrap

**Confirmed by Code**: Application bootstraps through main.tsx.

**main.tsx**:
```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

// Set document title before app mounts
document.title = 'University ERP';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
```

**What This Does**:
- Sets document title
- Renders App component
- Uses StrictMode for development
- Uses createRoot for React 18+

### App Component

**Confirmed by Code**: App component sets up routing and providers.

**App.tsx**:
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

const AdmissionsPage = lazyWithReload(() => import('./pages/AdmissionsPage'))
const AnalyticsPage = lazyWithReload(() => import('./pages/AnalyticsPage'))
// ... more pages

function App() {
  return (
    <BrowserRouter>
      <ErrorBoundary>
        <AuthProvider>
          <ThemeProvider>
            <StudentStatusProvider>
              <QueryClientProvider client={queryClient}>
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/admissions" element={<AdmissionsPage />} />
                  <Route path="/analytics" element={<AnalyticsPage />} />
                  {/* ... more routes */}
                </Routes>
              </QueryClientProvider>
            </StudentStatusProvider>
          </ThemeProvider>
        </AuthProvider>
      </ErrorBoundary>
    </BrowserRouter>
  )
}
```

**What This Does**:
- **lazyWithReload**: Custom lazy loading with chunk reload on deploy
- **ErrorBoundary**: Catches component errors
- **AuthProvider**: Provides authentication context
- **ThemeProvider**: Provides theme context
- **StudentStatusProvider**: Provides student status context
- **QueryClientProvider**: Provides React Query client
- **Routes**: Defines application routes

### Component Pattern

**Confirmed by Code**: Components follow React patterns.

**Basic Component**:
```typescript
interface Props {
  title: string;
  onAction: () => void;
}

export function MyComponent({ title, onAction }: Props) {
  return (
    <div className="p-4">
      <h1>{title}</h1>
      <button onClick={onAction}>Action</button>
    </div>
  );
}
```

**What This Does**:
- **Interface**: Defines component props
- **Destructuring**: Destructures props
- **TypeScript**: Type-safe props
- **Tailwind**: Uses Tailwind CSS classes

## Database Interactions

### Frontend-Database Flow

**Confirmed by Code**: Frontend doesn't directly interact with database.

**Flow**:
```
Frontend → API → Backend → Database
```

## Redis Interactions

### Frontend-Redis Flow

**Confirmed by Code**: Frontend doesn't directly interact with Redis.

**Flow**:
```
Frontend → API → Backend → Redis
```

## Queue Interactions

### Frontend-Queue Flow

**Confirmed by Code**: Frontend doesn't directly interact with queues.

**Flow**:
```
Frontend → API → Backend → Queue
```

## Worker Interactions

### Frontend-Worker Flow

**Confirmed by Code**: Frontend doesn't directly interact with workers.

**Flow**:
```
Frontend → API → Backend → Worker
```

## Business Rules

### Frontend Rules

**Confirmed by Code**: Frontend follows these rules:

1. **Component Reusability**: Create reusable components
2. **Type Safety**: All code is TypeScript
3. **State Management**: Use React Query for server state
4. **Context**: Use context for global state
5. **Routing**: Use React Router for navigation

### Code Organization Rules

**Confirmed by Code**: Code organization follows these rules:

1. **Components**: Reusable components in components/
2. **Pages**: Page components in pages/
3. **API**: API calls in api/
4. **Hooks**: Custom hooks in hooks/
5. **Types**: TypeScript types in types/

## Security

### Frontend Security

**Confirmed by Code**: Security measures in frontend:

1. **JWT Storage**: Store JWT in localStorage
2. **Token Refresh**: Implement token refresh
3. **HTTPS**: Use HTTPS in production
4. **XSS Prevention**: Sanitize user input
5. **CSRF Prevention**: Implement CSRF tokens

## Performance Considerations

### Frontend Performance

**Confirmed by Code**: Performance considerations:

1. **Code Splitting**: Lazy load routes
2. **Caching**: Use React Query caching
3. **Optimization**: Optimize images and assets
4. **Bundle Size**: Keep bundle size small
5. **Lazy Loading**: Lazy load components

## Common Mistakes

### Mistake 1: Not Using TypeScript

**Symptom**: Type errors

**Cause**: Not using TypeScript

**Fix**:
```typescript
// Use TypeScript interfaces
interface Props {
  title: string;
}
```

### Mistake 2: Not Using React Query

**Symptom**: Manual state management

**Cause**: Not using React Query

**Fix**:
```typescript
// Use React Query
const { data, isLoading } = useQuery({
  queryKey: ['users'],
  queryFn: () => api.getUsers(),
});
```

### Mistake 3: Not Handling Errors

**Symptom**: Unhandled errors

**Cause**: Not handling errors

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

## Debugging Guide

### Frontend Debugging

**Issue**: Frontend not working

**Investigation**:
1. Check browser console
2. Check network requests
3. Check component state
4. Check API calls
5. Check routing

**Tools**:
- React DevTools
- Browser DevTools
- Network tab
- Console logs

## Future Enhancements

### PWA Support

**Status**: Not implemented

**Proposal**: Add PWA support:
- Service worker
- Offline support
- App manifest
- Push notifications
- Better mobile experience

### Testing

**Status**: Not implemented

**Proposal**: Add testing:
- Unit tests with Vitest
- Component tests with React Testing Library
- E2E tests with Playwright
- Test coverage
- CI/CD integration

## Production Considerations

### Production Frontend

**Production Deployment**:
- Build for production
- Enable compression
- Enable caching
- Use CDN
- Monitor performance
- Monitor errors

### Frontend Monitoring

**Monitoring Metrics**:
- Page load time
- Bundle size
- Error rate
- API response time
- User engagement

## Example Requests

### API Call Example

**Request**:
```typescript
const { data } = useQuery({
  queryKey: ['users'],
  queryFn: () => api.getUsers(),
});
```

## Example Responses

### Component Example

**Response**: Component rendering

```tsx
<div className="p-4">
  <h1>Users</h1>
  <ul>
    {data?.map(user => (
      <li key={user.id}>{user.name}</li>
    ))}
  </ul>
</div>
```

## Sequence Diagrams

### Request Flow

```
User Action → Component → Hook → API → Backend → Response → Component Update
```

## Architecture Diagrams

### Frontend Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  React Application                         │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Components   │  │  Pages          │  │  Hooks         │
└────────────────┘  └────────────────┘  └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Contexts     │  │  React Query   │  │  API Layer     │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: Why did you choose React for the frontend?

**Answer**: React chosen because:
- Component-based architecture
- Large ecosystem and community
- TypeScript support
- React Query for server state
- Vite for fast development
- Tailwind CSS for styling

### Q2: How does state management work in the frontend?

**Answer**: State management via:
- React Query for server state
- Context API for global state
- useState for local state
- Custom hooks for reusable logic
- Type-safe with TypeScript

### Q3: How do you handle API calls?

**Answer**: API calls via:
- Axios for HTTP client
- React Query for data fetching
- Custom hooks for API logic
- Type-safe API responses
- Error handling

## Exercises

### Exercise 1: Create a Component

**Task**: Create a new component.

**Steps**:
1. Create component file
2. Define props interface
3. Implement component logic
4. Add styling
5. Test component

**Verification**:
- Component created
- Props typed
- Logic works
- Styling applied
- Tests pass

### Exercise 2: Create a Custom Hook

**Task**: Create a custom hook.

**Steps**:
1. Create hook file
2. Implement hook logic
3. Add TypeScript types
4. Use hook in component
5. Test hook

**Verification**:
- Hook created
- Logic works
- Types correct
- Used correctly
- Tests pass

## Real Production Scenarios

### Scenario 1: Slow Page Load

**Situation**: Page load slow

**Response**:
1. Check bundle size
2. Implement code splitting
3. Optimize images
4. Enable caching
5. Monitor performance

### Scenario 2: API Error

**Situation**: API call failing

**Response**:
1. Check API endpoint
2. Check authentication
3. Check error handling
4. Add retry logic
5. Monitor errors

## Navigation

**Next Section**: [01-React-Framework](./01-React-Framework.md)

**Previous Section**: [03-Backend](../03-Backend/README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [12-API-Reference](../01-System-Architecture/12-API-Reference.md) - API reference
