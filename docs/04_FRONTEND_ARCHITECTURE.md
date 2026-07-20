# University ERP - Frontend Architecture

## Overview

The frontend is a **React 19** single-page application built with **Vite 8**, using **TypeScript 6** for type safety. It serves as the admin interface for the University ERP system, providing access to all 36 backend modules through a rich, interactive UI.

## Technology Stack

### Core Framework
- **React 19**: UI library with modern hooks
- **Vite 8**: Build tool and dev server
- **TypeScript 6**: Type-safe JavaScript
- **React Router 7**: Client-side routing

### State Management & Data Fetching
- **@tanstack/react-query 5**: Server state management and caching
- **React Context**: Client state (auth, theme, student status)

### UI Components & Styling
- **TailwindCSS 3**: Utility-first CSS framework
- **@headlessui/react**: Unstyled accessible components
- **lucide-react**: Icon library
- **clsx**: Conditional class names
- **tailwind-merge**: Tailwind class merging

### Forms & Validation
- **react-hook-form 7**: Form state management
- **@hookform/resolvers**: Validation integration
- **zod 3.22.x**: Schema validation

### Rich Text & Documents
- **@tiptap/react 3**: Rich text editor
- **@tiptap/starter-kit**: Tiptap extensions
- **jspdf**: PDF generation
- **jspdf-autotable**: PDF tables
- **react-markdown**: Markdown rendering
- **remark-gfm**: GitHub Flavored Markdown
- **rehype-sanitize**: HTML sanitization

### Data Visualization
- **recharts 3**: Chart library
- **@xyflow/react**: Diagram/flow chart library

### Drag and Drop
- **@dnd-kit/core**: Drag and drop core
- **@dnd-kit/sortable**: Sortable lists
- **@dnd-kit/utilities**: DnD utilities

### Barcodes & QR Codes
- **jsbarcode**: Barcode generation
- **qrcode**: QR code generation

### LaTeX Rendering
- **katex**: LaTeX math rendering

### HTTP Client
- **axios**: HTTP requests

### Other Utilities
- **date-fns**: Date manipulation
- **clsx**: Class name utilities
- **tailwind-merge**: Tailwind utilities

## Project Structure

```
web/admin-portal/src/
├── App.tsx                  # Root component with routing
├── main.tsx                 # React entry point
├── index.css                # Global styles
├── App.css                  # App-specific styles
│
├── api/                     # API client layer
│   ├── auth.ts             # Authentication API
│   ├── axios.ts            # Axios configuration
│   └── modules.ts          # Module-specific API calls
│
├── auth/                    # Authentication context
│   ├── AuthContext.tsx     # Auth provider
│   ├── ProtectedRoute.tsx   # Route protection
│   ├── StudentStatusContext.tsx # Student status
│   └── useAuth.ts          # Auth hook
│
├── components/              # Reusable components
│   ├── (40+ components)
│   └── canvas/             # Canvas-specific components
│
├── config/                  # Configuration
│   └── appTitle.ts         # App title management
│
├── help/                    # Help documentation
│   └── (32 help files)
│
├── layouts/                 # Layout components
│   └── AdminLayout.tsx     # Main admin layout
│
├── lib/                     # Utility libraries
│   └── appTitle.ts         # Title utilities
│
├── pages/                   # Page components (41 pages)
│   ├── (41 page components)
│
├── theme/                   # Theme configuration
│   └── ThemeContext.tsx    # Theme provider
│
└── utils/                   # Utility functions
    └── (utility functions)
```

## Application Bootstrap

### Entry Point: `src/main.tsx`

```typescript
1. Import React StrictMode
2. Import CSS files (index.css, katex)
3. Bootstrap branded tab title
4. Create root and render App
```

### Root Component: `src/App.tsx`

```typescript
1. Setup QueryClient (React Query)
2. Configure providers:
   - BrowserRouter (routing)
   - QueryClientProvider (server state)
   - AuthProvider (authentication)
   - StudentStatusProvider (student status)
   - ThemeProvider (theming)
   - ErrorBoundary (error handling)
3. Define lazy-loaded routes (41 pages)
4. Configure route protection
5. Setup title management
```

## Routing Architecture

### Route Pattern

```typescript
<BrowserRouter>
  <Routes>
    {/* Public routes */}
    <Route path="/login" element={<LoginPage />} />
    <Route path="/register" element={<RegisterPage />} />
    <Route path="/forgot-password" element={<ForgotPasswordPage />} />
    
    {/* Protected routes */}
    <Route element={<ProtectedRoute><AdminLayout /></ProtectedRoute>}>
      <Route path="/" element={<DashboardPage />} />
      <Route path="/master-data" element={<MasterDataPage />} />
      {/* ... 38 more routes */}
    </Route>
  </Routes>
</BrowserRouter>
```

### Lazy Loading

All 41 pages are lazy-loaded to reduce initial bundle size:

```typescript
const DashboardPage = lazyWithReload(() => import('./pages/DashboardPage'))
const MasterDataPage = lazyWithReload(() => import('./pages/MasterDataPage'))
// ... 39 more
```

### lazyWithReload Pattern

Custom lazy loading with chunk reload handling:

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
        return new Promise<T>(() => {})
      }
      throw err
    }),
  )
}
```

**Purpose**: Handle chunk hash changes after deployment by forcing a single reload.

## State Management

### Server State (React Query)

```typescript
const qc = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, staleTime: 30_000 }
  }
})
```

**Configuration**:
- **Retry**: 1 failed request
- **Stale Time**: 30 seconds (data considered fresh)
- **Cache**: Automatic caching and invalidation

### Client State (React Context)

#### AuthContext
- **Purpose**: Authentication state
- **State**: user, token, isAuthenticated
- **Methods**: login, logout, refresh

#### StudentStatusContext
- **Purpose**: Student enrollment status
- **State**: isEnrolled, enrollmentNo
- **Methods**: checkStatus

#### ThemeContext
- **Purpose**: Theme management
- **State**: theme (light/dark)
- **Methods**: toggleTheme

## API Client Architecture

### Axios Configuration (`src/api/axios.ts`)

```typescript
const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:3000/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})
```

### Request Interceptor

```typescript
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)
```

### Response Interceptor

```typescript
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Try refresh token
      const refreshToken = localStorage.getItem('refreshToken')
      if (refreshToken) {
        try {
          const { data } = await axios.post('/auth/refresh', { refreshToken })
          localStorage.setItem('accessToken', data.accessToken)
          return axiosInstance.request(error.config)
        } catch (refreshError) {
          // Refresh failed, logout
          localStorage.clear()
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)
```

### Module API (`src/api/modules.ts`)

Organized by backend modules:

```typescript
export const masterDataApi = {
  universities: {
    get: (id: string) => axiosInstance.get(`/master-data/universities/${id}`),
    list: (params) => axiosInstance.get('/master-data/universities', { params }),
    create: (data) => axiosInstance.post('/master-data/universities', data),
    update: (id, data) => axiosInstance.patch(`/master-data/universities/${id}`, data),
    delete: (id) => axiosInstance.delete(`/master-data/universities/${id}`),
  },
  // ... other modules
}
```

## Component Architecture

### Component Categories

#### 1. Layout Components
- **AdminLayout**: Main layout with sidebar, header, content area

#### 2. Page Components (41 pages)
- Dashboard, MasterData, Admissions, Attendance, Fees, etc.

#### 3. Reusable Components (40+)
- **Modal**: Dialog component
- **Table**: Data table with pagination
- **Form**: Form components
- **Spinner**: Loading indicator
- **Badge**: Status badge
- **Tabs**: Tab navigation
- **SearchBar**: Search input
- **Pagination**: Pagination controls
- **ConfirmDialog**: Confirmation dialog
- **ErrorBoundary**: Error boundary
- **NotificationBell**: Notification dropdown
- **PageHeader**: Page header
- **HelpDrawer**: Help documentation drawer
- **RichContent**: Rich text renderer
- **DateInput**: Date picker
- **DateTimeInput**: Date-time picker
- **SearchSelect**: Searchable select
- **WorkflowProgress**: Workflow progress indicator
- **SystemStatus**: System status display
- **CanvasDocumentDesigner**: Document designer
- **ExecDashboard**: Executive dashboard
- **PersonalDashboard**: Personal dashboard
- **Folder**: Folder component
- **FormField**: Form field wrapper
- **NotEnrolledNotice**: Enrollment notice
- **InstanceDrawer**: Instance detail drawer
- **ReadOnlyFormView**: Read-only form view
- **StreamLabelDetailModal**: Stream label details
- **ProgramLabelDetailModal**: Program label details
- **AdmissionApplyModal**: Admission application modal
- **ApplicantCard**: Applicant card
- **ApplicationFeeModal**: Application fee modal
- **BannerHost**: Banner host component

#### 4. Canvas Components
- Specialized components for canvas/document designer

## Page Architecture

### Page Pattern

```typescript
export default function [PageName]() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['resource', params],
    queryFn: () => api.resource.get(params.id),
  })

  const mutation = useMutation({
    mutationFn: (data) => api.resource.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries(['resource'])
    },
  })

  if (isLoading) return <Spinner />
  if (error) return <ErrorState />

  return (
    <div className="p-6">
      <PageHeader title="[Page Title]" />
      {/* Page content */}
    </div>
  )
}
```

### Page List (41 Pages)

1. **LoginPage** - User login
2. **RegisterPage** - User registration
3. **ForgotPasswordPage** - Password recovery
4. **ResetPasswordPage** - Password reset
5. **SetupAccountPage** - Account setup
6. **DashboardPage** - Main dashboard
7. **MasterDataPage** - Master data management
8. **AdmissionsPage** - Admissions management
9. **StartAdmissionsPage** - Start admissions
10. **MeritListPage** - Merit list management
11. **AttendancePage** - Attendance tracking
12. **FeesPage** - Fee management
13. **TimetablePage** - Timetable management
14. **LibraryPage** - Library management
15. **HostelPage** - Hostel management
16. **TransportPage** - Transport management
17. **HRPage** - HR management
18. **ExaminationsPage** - Examination management
19. **ExamTakePage** - Taking exams (CBE)
20. **ExamMonitorPage** - Exam monitoring
21. **ExamItemAnalysisPage** - Exam item analysis
22. **CounsellingAdminPage** - Counselling admin
23. **CounsellingDeskPage** - Counselling desk
24. **DocumentsPage** - Document management
25. **NoticeBoardPage** - Notice board
26. **AnalyticsPage** - Analytics and reports
27. **UserManagementPage** - User management
28. **StudentProfilePage** - Student profiles
29. **StudentApplicationsPage** - Student applications
30. **LeaveRequestsPage** - Leave requests
31. **FormsPage** - Dynamic forms
32. **DirectoryPage** - Staff/student directory
33. **AuditLogPage** - Audit log viewer
34. **WorkflowDesignerPage** - Workflow designer
35. **MyTasksPage** - My tasks (workflow)
36. **MyInvigilationPage** - My invigilation duties
37. **WorkflowMonitorPage** - Workflow monitoring
38. **IdFormatsPage** - ID format configuration
39. **HelpCenterPage** - Help center
40. **OnboardStudentsPage** - Student onboarding
41. **BannersPage** - Banner management
42. **SettingsPage** - System settings
43. **ProgramFeeManager** - Program fee management
44. **ResourceFeeManager** - Resource fee management

## Form Architecture

### Form Pattern (react-hook-form + zod)

```typescript
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const schema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email'),
})

export default function [FormName]() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(schema),
  })

  const mutation = useMutation({
    mutationFn: (data) => api.resource.create(data),
    onSuccess: () => {
      // Handle success
    },
  })

  return (
    <form onSubmit={handleSubmit((data) => mutation.mutate(data))}>
      <input {...register('name')} />
      {errors.name && <span>{errors.name.message}</span>}
      <button type="submit">Submit</button>
    </form>
  )
}
```

## Rich Text Editor (TipTap)

### Configuration

```typescript
import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'

const editor = useEditor({
  extensions: [StarterKit],
  content: '<p>Hello World!</p>',
})

return <EditorContent editor={editor} />
```

### Usage

Used in:
- **FormsPage**: Dynamic form descriptions
- **NoticeBoardPage**: Notice content
- **DocumentsPage**: Document templates

## Data Visualization (Recharts)

### Chart Types

- **LineChart**: Trends over time
- **BarChart**: Comparisons
- **PieChart**: Distributions
- **AreaChart**: Cumulative data

### Usage

Used in:
- **AnalyticsPage**: Analytics dashboards
- **DashboardPage**: Overview charts
- **FeesPage**: Fee collection charts

## PDF Generation (jsPDF)

### Pattern

```typescript
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

const doc = new jsPDF()
autoTable(doc, {
  head: [['Name', 'Email']],
  body: [['John', 'john@example.com']],
})
doc.save('table.pdf')
```

### Usage

Used in:
- **DocumentsPage**: Document generation
- **FeesPage**: Fee receipts
- **ExaminationsPage**: Admit cards

## Authentication Flow

### Login Flow

```
1. User enters credentials
   ↓
2. POST /api/auth/login
   ↓
3. Store tokens in localStorage
   ↓
4. Update AuthContext
   ↓
5. Redirect to dashboard
```

### Protected Route Flow

```
1. User navigates to protected route
   ↓
2. ProtectedRoute checks AuthContext
   ↓
3. If not authenticated, redirect to login
   ↓
4. If authenticated, render component
   ↓
5. Axios interceptor adds token to requests
   ↓
6. On 401, attempt token refresh
   ↓
7. If refresh fails, logout and redirect
```

## Error Handling

### Error Boundary

```typescript
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

Catches React errors and displays fallback UI.

### Query Error Handling

```typescript
const { error } = useQuery({
  queryKey: ['resource'],
  queryFn: () => api.resource.get(),
  onError: (error) => {
    // Handle error
  },
})
```

### Mutation Error Handling

```typescript
const mutation = useMutation({
  mutationFn: (data) => api.resource.create(data),
  onError: (error) => {
    // Show error message
  },
})
```

## Performance Optimizations

### Code Splitting

- **Route-based**: Lazy loading of pages
- **Component-based**: Dynamic imports for large components

### Caching

- **React Query**: Automatic caching and invalidation
- **Stale Time**: 30 seconds for most queries
- **Cache Time**: 5 minutes default

### Image Optimization

- **Lazy loading**: Images loaded on demand
- **Presigned URLs**: MinIO direct access

### Bundle Size

- **Tree shaking**: Remove unused code
- **Minification**: Production builds
- **Compression**: Gzip compression (Vite default)

## Styling Architecture

### TailwindCSS Configuration

```javascript
// tailwind.config.js (inferred)
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      // Custom theme extensions
    },
  },
  plugins: [],
}
```

### CSS Pattern

```tsx
<div className="flex items-center justify-between p-4 bg-white rounded-lg shadow">
  <h2 className="text-lg font-semibold text-gray-900">Title</h2>
  <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
    Action
  </button>
</div>
```

### Custom Components

- **Badge**: Status badges
- **Spinner**: Loading indicators
- **Modal**: Dialog components
- **Table**: Data tables
- **Tabs**: Tab navigation

## Responsive Design

### Breakpoints

TailwindCSS default breakpoints:
- **sm**: 640px
- **md**: 768px
- **lg**: 1024px
- **xl**: 1280px
- **2xl**: 1536px

### Pattern

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Responsive grid */}
</div>
```

## Accessibility

### ARIA Labels

```tsx
<button aria-label="Close" onClick={onClose}>
  <X />
</button>
```

### Keyboard Navigation

- **Focus management**: Modal focus trap
- **Keyboard shortcuts**: Custom shortcuts
- **Screen readers**: Semantic HTML

### Headless UI

Uses @headlessui/react for accessible components:
- **Dialog**: Accessible modals
- **Menu**: Accessible dropdowns
- **Disclosure**: Accessible accordions

## Testing Strategy

### Unit Tests

- **Framework**: Vitest (inferred from Vite)
- **Coverage**: Components, hooks, utilities

### E2E Tests

- **Framework**: Playwright (not extensively implemented)
- **Coverage**: Critical user flows

## Build Configuration

### Vite Configuration

```javascript
// vite.config.ts (inferred)
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:3000',
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
})
```

### Environment Variables

```bash
VITE_API_URL=http://localhost:3000/api
```

### Build Scripts

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  }
}
```

## Deployment

### Development

```bash
npm run dev
```

Runs Vite dev server on port 5173.

### Production Build

```bash
npm run build
```

Builds to `dist/` directory.

### Production Serve

```bash
npm run preview
```

Serves production build.

### Docker

Frontend served via Nginx in docker-compose.yml.

## Known Limitations

1. **No Mobile App**: Web-only interface
2. **No PWA**: Not installable as PWA
3. **Limited Offline**: No offline support
4. **No Internationalization**: English-only
5. **Limited E2E Tests**: Manual testing required
