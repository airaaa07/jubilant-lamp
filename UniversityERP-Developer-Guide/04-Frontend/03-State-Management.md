# State Management

## Purpose

This document explains the state management strategy used in the University ERP frontend. It details how state is managed, the tools used, and best practices for state management.

## Why This Document Exists

**Confirmed by Code**: The University ERP frontend uses multiple state management solutions. Understanding state management is critical for:
- Managing application state
- Managing server state
- Managing local component state
- Debugging state issues
- Optimizing state performance

Without understanding state management, developers may struggle with state-related bugs or performance issues.

## Where This Is Used

- **Onboarding**: New developers learn state management
- **Feature Development**: Implementing state management
- **Code Reviews**: Reviewing state management code
- **Debugging**: Debugging state issues
- **Performance**: Optimizing state performance

## Dependencies

### State Management Dependencies

**Confirmed by Code**: State management depends on:

- **React 19**: Built-in state (useState, useReducer)
- **React Query**: Server state management
- **Context API**: Global state management
- **Custom Hooks**: Reusable state logic

## Internal Architecture

### State Architecture

**Confirmed by Code**: State is managed at multiple levels.

```
┌─────────────────────────────────────────────────────────┐
│              State Management Layers                       │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Server State │  │  Global State   │  │  Local State   │
│  (React Query)│  │  (Context)      │  │  (useState)    │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Local State

**Confirmed by Code**: Local state managed with useState.

**useState Example**:
```typescript
export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

**What This Does**:
- **useState**: Manages component state
- **count**: Current state value
- **setCount**: Function to update state
- **Initial Value**: 0

**useReducer Example**:
```typescript
type State = { count: number };
type Action = { type: 'increment' } | { type: 'decrement' };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    default:
      return state;
  }
}

export function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0 });

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'increment' })}>Increment</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>Decrement</button>
    </div>
  );
}
```

**What This Does**:
- **useReducer**: Manages complex state with actions
- **reducer**: Reducer function for state updates
- **dispatch**: Dispatches actions
- **Type Safety**: TypeScript types for state and actions

### Global State

**Confirmed by Code**: Global state managed with Context API.

**AuthContext**:
```typescript
interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);

  const login = async (credentials: Credentials) => {
    const { user, token } = await api.login(credentials);
    setUser(user);
    setToken(token);
    localStorage.setItem('token', token);
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setToken(token);
      // Fetch user with token
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

**What This Does**:
- **Context**: Creates context for auth state
- **Provider**: Provides context to children
- **useAuth**: Custom hook to access context
- **localStorage**: Persists token
- **useEffect**: Loads token on mount

**ThemeContext**:
```typescript
interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | null>(null);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <div className={theme}>{children}</div>
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}
```

### Server State

**Confirmed by Code**: Server state managed with React Query.

**React Query Setup**:
```typescript
// api/queryClient.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      retry: 1,
    },
  },
});
```

**What This Does**:
- **QueryClient**: Creates React Query client
- **staleTime**: Time before data considered stale
- **cacheTime**: Time to keep data in cache
- **retry**: Number of retries on failure

**useQuery Example**:
```typescript
export function UsersList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: () => api.getUsers(),
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <ul>
      {data?.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

**What This Does**:
- **useQuery**: Fetches server data
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
    mutationFn: (data: CreateUserDto) => api.createUser(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
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
- **useMutation**: Performs server mutation
- **mutationFn**: Function to perform mutation
- **onSuccess**: Callback on success
- **invalidateQueries**: Invalidates cache after mutation

## Database Interactions

### State-Database Flow

**Confirmed by Code**: State doesn't directly interact with database.

**Flow**:
```
State → API → Backend → Database
```

## Redis Interactions

### State-Redis Flow

**Confirmed by Code**: State doesn't directly interact with Redis.

**Flow**:
```
State → API → Backend → Redis
```

## Queue Interactions

### State-Queue Flow

**Confirmed by Code**: State doesn't directly interact with queues.

**Flow**:
```
State → API → Backend → Queue
```

## Worker Interactions

### State-Worker Flow

**Confirmed by Code**: State doesn't directly interact with workers.

**Flow**:
```
State → API → Backend → Worker
```

## Business Rules

### State Management Rules

**Confirmed by Code**: State management follows these rules:

1. **Local State**: Use useState for local component state
2. **Global State**: Use Context for global state
3. **Server State**: Use React Query for server state
4. **Form State**: Use form state management for forms
5. **URL State**: Use URL params for URL state

### State Organization Rules

**Confirmed by Code**: State organization follows these rules:

1. **Component State**: Keep state in component if only used there
2. **Context State**: Use context for state shared across components
3. **Server State**: Use React Query for server data
4. **Form State**: Use form state for form data
5. **URL State**: Use URL params for navigation state

## Security

### State Security

**Confirmed by Code**: Security considerations for state:

1. **Token Storage**: Store token in localStorage
2. **Sensitive Data**: Don't store sensitive data in state
3. **Sanitization**: Sanitize data before storing
4. **Encryption**: Encrypt sensitive data if needed
5. **Clear on Logout**: Clear state on logout

## Performance Considerations

### State Performance

**Confirmed by Code**: Performance considerations for state:

1. **Memoization**: Use useMemo for expensive calculations
2. **Callback Memoization**: Use useCallback for function references
3. **Selective Updates**: Update only necessary state
4. **Debounce**: Debounce rapid state updates
5. **Virtualization**: Use virtualization for large lists

## Common Mistakes

### Mistake 1: Using Context for Everything

**Symptom**: Unnecessary re-renders

**Cause**: Using context for all state

**Fix**:
```typescript
// Use context only for global state
// Use local state for component-specific state
// Use React Query for server state
```

### Mistake 2: Not Using React Query

**Symptom**: Manual state management for server data

**Cause**: Not using React Query

**Fix**:
```typescript
// Use React Query for server state
const { data } = useQuery({
  queryKey: ['users'],
  queryFn: () => api.getUsers(),
});
```

### Mistake 3: Mutating State Directly

**Symptom**: Component not updating

**Cause**: Mutating state directly

**Fix**:
```typescript
// Wrong
user.name = 'New Name';
setUser(user);

// Correct
setUser({ ...user, name: 'New Name' });
```

## Debugging Guide

### State Debugging

**Issue**: State not updating correctly

**Investigation**:
1. Check state update logic
2. Check dependency array
3. Check context provider
4. Check React Query cache
5. Use React DevTools

**Tools**:
- React DevTools
- React Query DevTools
- Console logs
- Breakpoints

## Future Enhancements

### Zustand

**Status**: Not implemented

**Proposal**: Add Zustand for global state:
- Simpler than Context API
- Better performance
- Easier to use
- TypeScript support
- DevTools

### Jotai

**Status**: Not implemented

**Proposal**: Add Jotai for atomic state:
- Atomic state management
- Better performance
- Simpler API
- TypeScript support
- Composable state

## Production Considerations

### Production State

**Production Deployment**:
- Optimize state updates
- Enable React Query caching
- Monitor state performance
- Monitor state errors
- Implement state persistence

### State Monitoring

**Monitoring Metrics**:
- State update frequency
- Re-render frequency
- Cache hit rate
- Query error rate
- Mutation success rate

## Example Requests

### State Update Example

**Request**: Update state

```typescript
setCount(prev => prev + 1);
```

## Example Responses

### State Response

**Response**: State updated

```typescript
count: 1
```

## Sequence Diagrams

### State Update Flow

```
User Action → Component → State Update → Re-render
```

## Architecture Diagrams

### State Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Component                                     │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  useState     │  │  useContext     │  │  useQuery      │
│  (Local)      │  │  (Global)       │  │  (Server)      │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: How do you manage state in React?

**Answer**: State management via:
- useState for local component state
- useReducer for complex state
- Context API for global state
- React Query for server state
- Custom hooks for reusable state logic

### Q2: When should you use React Query vs Context vs useState?

**Answer**: Use:
- React Query for server data (API calls)
- Context for global state shared across components
- useState for local component state
- useReducer for complex local state
- URL params for navigation state

### Q3: How do you optimize state performance?

**Answer**: Optimize via:
- useMemo for expensive calculations
- useCallback for function references
- React.memo for component memoization
- Selective context updates
- Debounce rapid updates

## Exercises

### Exercise 1: Create a Context

**Task**: Create a new context.

**Steps**:
1. Create context file
2. Define context type
3. Create provider component
4. Create custom hook
5. Use context in component

**Verification**:
- Context created
- Provider works
- Hook works
- Context used correctly
- Tests pass

### Exercise 2: Use React Query

**Task**: Use React Query for data fetching.

**Steps**:
1. Set up QueryClient
2. Create query function
3. Use useQuery in component
4. Handle loading and error states
5. Test query

**Verification**:
- QueryClient set up
- Query function works
- useQuery works
- States handled
- Tests pass

## Real Production Scenarios

### Scenario 1: State Not Updating

**Situation**: State not updating when expected

**Response**:
1. Check state update logic
2. Check dependency array
3. Check for stale closures
4. Fix state update
5. Test component

### Scenario 2: Too Many Re-renders

**Situation**: Component re-rendering too frequently

**Response**:
1. Identify cause of re-renders
2. Add React.memo
3. Add useMemo/useCallback
4. Optimize context updates
5. Monitor performance

## Navigation

**Next Section**: [04-Routing](./04-Routing.md)

**Previous Section**: [02-Component-Architecture](./02-Component-Architecture.md)

**Related Documentation**:
- [01-React-Framework](./01-React-Framework.md) - React framework
- [02-Component-Architecture](./02-Component-Architecture.md) - Component architecture
- [05-API-Integration](./05-API-Integration.md) - API integration
