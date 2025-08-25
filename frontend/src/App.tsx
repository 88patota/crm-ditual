import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { ConfigProvider, App as AntApp } from 'antd';
import ptBR from 'antd/locale/pt_BR';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { setQueryClient } from './lib/api';
import ProtectedRoute from './components/auth/ProtectedRoute';
import AntLayout from './components/layout/AntLayout';
import AntLogin from './pages/AntLogin';
import Register from './pages/Register';
import AntDashboard from './pages/AntDashboard';
import Profile from './pages/Profile';
import Users from './pages/Users';
import Budgets from './pages/Budgets';
import BudgetCreate from './pages/BudgetCreate';
import SimplifiedBudgetCreate from './pages/AutoMarkupBudgetCreate';
import BudgetEditSimplified from './pages/BudgetEditSimplified';
import BudgetView from './pages/BudgetView';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
});

// Configure queryClient for API interceptors
setQueryClient(queryClient);

function AppRoutes() {
  const { isAuthenticated } = useAuth();

  return (
    <Routes>
      {/* Public routes */}
      <Route
        path="/login"
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <AntLogin />}
      />
      <Route
        path="/register"
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Register />}
      />

      {/* Protected routes */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <AntLayout>
              <AntDashboard />
            </AntLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <AntLayout>
              <Profile />
            </AntLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/users"
        element={
          <ProtectedRoute adminOnly>
            <AntLayout>
              <Users />
            </AntLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/budgets"
        element={
          <ProtectedRoute>
            <AntLayout>
              <Budgets />
            </AntLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/budgets/new"
        element={
          <ProtectedRoute>
            <AntLayout>
              <SimplifiedBudgetCreate />
            </AntLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/budgets/new-simplified"
        element={
          <ProtectedRoute>
            <AntLayout>
              <SimplifiedBudgetCreate />
            </AntLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/budgets/new-complete"
        element={
          <ProtectedRoute>
            <AntLayout>
              <BudgetCreate />
            </AntLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/budgets/:id"
        element={
          <ProtectedRoute>
            <AntLayout>
              <BudgetView />
            </AntLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/budgets/:id/edit"
        element={
          <ProtectedRoute>
            <AntLayout>
              <BudgetEditSimplified />
            </AntLayout>
          </ProtectedRoute>
        }
      />

      {/* Default redirect */}
      <Route
        path="/"
        element={
          <Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />
        }
      />

      {/* 404 fallback */}
      <Route
        path="*"
        element={
          <div style={{ 
            minHeight: '100vh', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            background: '#f5f5f5'
          }}>
            <div style={{ textAlign: 'center' }}>
              <h1 style={{ fontSize: '48px', fontWeight: 'bold', margin: '0 0 16px 0' }}>404</h1>
              <p style={{ color: '#8c8c8c', marginBottom: '24px' }}>Página não encontrada</p>
              <a
                href={isAuthenticated ? "/dashboard" : "/login"}
                style={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  padding: '8px 16px',
                  borderRadius: '6px',
                  textDecoration: 'none'
                }}
              >
                Voltar ao início
              </a>
            </div>
          </div>
        }
      />
    </Routes>
  );
}

function App() {
  return (
    <ConfigProvider
      locale={ptBR}
      theme={{
        token: {
          colorPrimary: '#667eea',
          colorInfo: '#667eea',
          borderRadius: 8,
          fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        },
        components: {
          Layout: {
            siderBg: '#ffffff',
            triggerBg: '#ffffff',
            triggerColor: '#1890ff',
          },
          Menu: {
            itemBg: 'transparent',
            itemSelectedBg: '#e6f4ff',
            itemSelectedColor: '#1890ff',
            itemHoverBg: '#f0f0f0',
          },
          Button: {
            borderRadius: 8,
            primaryShadow: '0 2px 0 rgba(102, 126, 234, 0.1)',
          },
          Card: {
            borderRadius: 12,
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.06)',
          },
        },
      }}
    >
      <AntApp>
        <QueryClientProvider client={queryClient}>
          <AuthProvider>
            <Router>
              <div className="App">
                <AppRoutes />
              </div>
            </Router>
          </AuthProvider>
          <ReactQueryDevtools initialIsOpen={false} />
        </QueryClientProvider>
      </AntApp>
    </ConfigProvider>
  );
}

export default App;
