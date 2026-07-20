# React Framework

## Purpose

This document explains the React framework used in the University ERP frontend. It details React concepts, component patterns, hooks, and React-specific features.

## Why This Document Exists

**Confirmed by Code**: The University ERP frontend is built with React 19. Understanding React is critical for:
- Developing React components
- Understanding React patterns
- Implementing React features
- Debugging React issues
- Optimizing React performance

Without understanding React, developers may struggle to work with the frontend codebase.

## Where This Is Used

- **Onboarding**: New developers learn React
- **Feature Development**: Implementing React features
- **Code Reviews**: Understanding React code
- **Debugging**: Debugging React issues
- **Performance**: Optimizing React performance

## Dependencies

### React Dependencies

**Confirmed by Code**: React depends on:

- **React 19**: UI library
- **TypeScript 6.x**: Type-safe JavaScript
- **React DOM**: DOM renderer
- **React Router**: Routing library
- **React Query**: Server state management

## Internal Architecture

### React Architecture

**Confirmed by Code**: React follows component-based architecture.

```
┌─────────────────────────────────────────────────────────┐
│                  React Application                         │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  Components   │  │  Hooks          │  │  Context       │
│  (UI)         │  │  (Logic)        │  │  (State)       │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Code Walkthrough

### Component Definition

**Confirmed by Code**: Components defined as functions.

**Function Component**:
```typescript
interface Props {
  title: string;
  count: number;
  onIncrement: () => void;
}

export function Counter({ title, count, onIncrement }: Props) {
  return (
    <div className="p-4">
      <h1>{title}</h1>
      <p>Count: {count}</p>
      <button onClick={onIncrement}>Increment</button>
    </div>
  );
}
```

**What This Does**:
- **Interface**: Defines component props
- **Destructuring**: Destructures props
- **TypeScript**: Type-safe props
- **JSX**: Returns JSX markup

### Hooks

**Confirmed by Code**: Hooks used for state and side effects.

**useState Hook**:
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

**useEffect Hook**:
```typescript
export function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);

  if (!user) return <div>Loading...</div>;

  return <div>{user.name}</div>;
}
```

**What This Does**:
- **useEffect**: Handles side effects
- **Dependency Array**: [userId] - effect runs when userId changes
- **Fetch Data**: Fetches user data
- **Cleanup**: Cleanup function can be returned

**useContext Hook**:
```typescript
export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button onClick={toggleTheme}>
      Current theme: {theme}
    </button>
  );
}
```

**What This Does**:
- **useContext**: Accesses context value
- **theme**: Current theme value
- **toggleTheme**: Function to toggle theme

**Custom Hook**:
```typescript
function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch user
    fetchUser().then(setUser).finally(() => setLoading(false));
  }, []);

  return { user, loading };
}

export function UserProfile() {
  const { user, loading } = useAuth();

  if (loading) return <div>Loading...</div>;
  if (!user) return <div>Not logged in</div>;

  return <div>{user.name}</div>;
}
```

**What This Does**:
- **Custom Hook**: Encapsulates logic
- **Reusable**: Can be used in multiple components
- **Type-Safe**: TypeScript types
- **State Management**: Manages auth state

### Context

**Confirmed by Code**: Context used for global state.

**AuthContext**:
```typescript
interface AuthContextType {
  user: User | null;
  login: (credentials: Credentials) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = async (credentials: Credentials) => {
    const user = await api.login(credentials);
    setUser(user);
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
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
- **Error Handling**: Throws error if used outside provider

## Database Interactions

### React-Database Flow

**Confirmed by Code**: React doesn't directly interact with database.

**Flow**:
```
React → API → Backend → Database
```

## Redis Interactions

### React-Redis Flow

**Confirmed by Code**: React doesn't directly interact with Redis.

**Flow**:
```
React → API → Backend → Redis
```

## Queue Interactions

### React-Queue Flow

**Confirmed by Code**: React doesn't directly interact with queues.

**Flow**:
```
React → API → Backend → Queue
```

## Worker Interactions

### React-Worker Flow

**Confirmed by Code**: React doesn't directly interact with workers.

**Flow**:
```
React → API → Backend → Worker
```

## Business Rules

### React Rules

**Confirmed by Code**: React follows these rules:

1. **Component-Based**: UI built from components
2. **Unidirectional Data Flow**: Data flows down
3. **State Management**: Use hooks for state
4. **Side Effects**: Use useEffect for side effects
5. **Type Safety**: All code is TypeScript

### Hook Rules

**Confirmed by Code**: Hooks follow these rules:

1. **Only Call at Top Level**: Don't call hooks inside loops or conditions
2. **Only Call from React Functions**: Don't call hooks from regular functions
3. **Custom Hooks**: Create custom hooks for reusable logic
4. **Dependency Array**: Always include dependencies in useEffect
5. **Cleanup**: Cleanup side effects in useEffect

## Security

### React Security

**Confirmed by Code**: Security considerations for React:

1. **XSS Prevention**: React escapes JSX by default
2. **Sanitization**: Sanitize user input
3. **JWT Storage**: Store JWT securely
4. **HTTPS**: Use HTTPS in production
5. **CSRF Prevention**: Implement CSRF tokens

## Performance Considerations

### React Performance

**Confirmed by Code**: Performance considerations:

1. **Memoization**: Use useMemo and useCallback
2. **Code Splitting**: Lazy load components
3. **Virtual DOM**: React uses virtual DOM
4. **Key Props**: Use key props for lists
5. **Avoid Unnecessary Re-renders**: Optimize re-renders

## Common Mistakes

### Mistake 1: Not Using Dependency Array

**Symptom**: Infinite loop in useEffect

**Cause**: Not including dependencies in useEffect

**Fix**:
```typescript
// Wrong
useEffect(() => {
  fetchUser(userId);
});

// Correct
useEffect(() => {
  fetchUser(userId);
}, [userId]);
```

### Mistake 2: Mutating State Directly

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

### Mistake 3: Not Using Keys in Lists

**Symptom**: List rendering issues

**Cause**: Not using keys in lists

**Fix**:
```typescript
// Wrong
users.map(user => <UserCard user={user} />)

// Correct
users.map(user => <UserCard key={user.id} user={user} />)
```

## Debugging Guide

### React Debugging

**Issue**: Component not rendering correctly

**Investigation**:
1. Check component state
2. Check props
3. Check useEffect dependencies
4. Check for errors
5. Use React DevTools

**Tools**:
- React DevTools
- Browser DevTools
- Console logs
- Breakpoints

## Future Enhancements

### Server Components

**Status**: Not implemented

**Proposal**: Add server components:
- React Server Components
- Better performance
- Reduced bundle size
- Server-side rendering
- Streaming

### Concurrent Features

**Status**: Not implemented

**Proposal**: Add concurrent features:
- Suspense for data fetching
- Concurrent rendering
- Better user experience
- Interruptible rendering
- Priority-based rendering

## Production Considerations

### Production React

**Production Deployment**:
- Build for production
- Enable minification
- Enable compression
- Use CDN
- Monitor performance
- Monitor errors

### React Monitoring

**Monitoring Metrics**:
- Component render time
- Re-render frequency
- Bundle size
- Error rate
- User engagement

## Example Requests

### Component Example

**Request**: Render a component

```tsx
<Counter title="My Counter" count={0} onIncrement={() => {}} />
```

## Example Responses

### Component Rendering

**Response**: Component renders

```html
<div class="p-4">
  <h1>My Counter</h1>
  <p>Count: 0</p>
  <button>Increment</button>
</div>
```

## Sequence Diagrams

### Component Lifecycle

```
Mount → useEffect → Render → Update → useEffect → Render → Unmount
```

## Architecture Diagrams

### React Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Component                                 │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐  ┌────────▼────────┐  ┌──────▼──────────┐
│  State        │  │  Props          │  │  Effects       │
│  (useState)   │  │  (Parameters)   │  │  (useEffect)   │
└────────────────┘  └────────────────┘  └─────────────────┘
```

## Common Interview Questions

### Q1: What is the difference between useState and useReducer?

**Answer**: useState vs useReducer:
- useState: Simple state management
- useReducer: Complex state management with actions
- useState: Good for independent state
- useReducer: Good for related state
- useReducer: Better for complex state transitions

### Q2: How does useEffect work?

**Answer**: useEffect:
- Runs after render
- Runs when dependencies change
- Can return cleanup function
- Handles side effects
- Replaces componentDidMount, componentDidUpdate, componentWillUnmount

### Q3: What are React hooks?

**Answer**: React hooks:
- Functions that start with "use"
- Allow using state and lifecycle in functional components
- Must be called at top level
- Must be called from React functions
- Custom hooks can be created

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

### Scenario 1: Component Not Updating

**Situation**: Component not updating when state changes

**Response**:
1. Check state mutation
2. Check dependency array
3. Check prop updates
4. Fix state update
5. Test component

### Scenario 2: Memory Leak

**Situation**: Memory leak in useEffect

**Response**:
1. Check cleanup function
2. Add cleanup to useEffect
3. Remove event listeners
4. Test cleanup
5. Monitor memory

## Navigation

**Next Section**: [02-Component-Architecture](./02-Component-Architecture.md)

**Previous Section**: [README](./README.md)

**Related Documentation**:
- [01-System-Architecture](../01-System-Architecture/README.md) - System architecture
- [03-Backend](../03-Backend/README.md) - Backend architecture
- [03-State-Management](./03-State-Management.md) - State management
