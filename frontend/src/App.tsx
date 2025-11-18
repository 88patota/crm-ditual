import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { ConfigProvider, theme, App as AntdApp } from 'antd';
import ptBR from 'antd/locale/pt_BR';
import dayjs from 'dayjs';
import 'dayjs/locale/pt-br';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/auth/ProtectedRoute';
import AntLayout from './components/layout/AntLayout';

// Páginas
import AntLogin from './pages/AntLogin';
import AntDashboard from './pages/AntDashboard';
import Users from './pages/Users';
import Budgets from './pages/Budgets';
import SimplifiedBudgetCreate from './pages/SimplifiedBudgetCreate';
import BudgetEdit from './pages/BudgetEdit';
import BudgetView from './pages/BudgetView';
import Profile from './pages/Profile';

// Estilos
import './index.css';
import './styles/AntDashboard.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

// Tema customizado do Ant Design com paleta pastel profissional
const customTheme = {
  algorithm: theme.defaultAlgorithm,
  token: {
    colorPrimary: '#1677ff',
    colorSuccess: '#52c41a',
    colorWarning: '#faad14',
    colorError: '#ff4d4f',
    colorInfo: '#1890ff',
    colorBgContainer: '#ffffff',
    colorBgElevated: '#ffffff',
    colorBgLayout: '#f5f5f5',
    colorBgSpotlight: '#ffffff',
    colorText: '#1f1f1f',
    colorTextSecondary: '#595959',
    colorTextTertiary: '#595959',
    colorTextQuaternary: '#595959',
    colorBorder: '#f0f0f0',
    colorBorderSecondary: '#f0f0f0',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
    boxShadowSecondary: '0 4px 12px rgba(0, 0, 0, 0.12)',
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif",
    fontSize: 14,
    fontSizeHeading1: 32,
    fontSizeHeading2: 24,
    fontSizeHeading3: 20,
    fontSizeHeading4: 16,
    fontSizeHeading5: 14,
    borderRadius: 8,
    borderRadiusLG: 12,
    borderRadiusSM: 6,
    padding: 16,
    paddingLG: 24,
    paddingSM: 12,
    paddingXS: 8,
    colorFillAlter: '#f5f5f5',
    colorFillContent: '#ffffff',
    colorFillContentHover: '#f5f5f5',
    colorBgContainerDisabled: '#ffffff',
    colorTextDisabled: '#8c8c8c',
    colorLink: '#1677ff',
    colorLinkHover: '#3c8cff',
    colorLinkActive: '#1358cc',
  },
  components: {
    Layout: {
      headerBg: '#FFFFFF',             // Branco - header
      headerHeight: 64,
      headerPadding: '0 24px',
      siderBg: '#FFFFFF',              // Branco - sidebar
      bodyBg: '#F7F8FA',               // Fundo geral - body
      footerBg: '#FFFFFF',             // Branco - footer
      footerPadding: '24px 50px',
    },
    Menu: {
      itemBg: 'transparent',
      itemSelectedBg: '#e6f4ff',
      itemSelectedColor: '#1677ff',
      itemHoverBg: '#e6f4ff',
      itemHoverColor: '#1677ff',
      itemActiveBg: '#e6f4ff',
      subMenuItemBg: 'transparent',
      groupTitleColor: '#595959',
    },
    Button: {
      primaryShadow: '0 2px 8px rgba(147, 207, 240, 0.3)',
      defaultShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
    },
    Card: {
      headerBg: 'transparent',
      actionsBg: '#F7F8FA',            // Fundo geral - ações
      boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
      boxShadowTertiary: '0 1px 3px rgba(0, 0, 0, 0.06)',
      colorBg: '#FFFFFF',              // Fundo branco para todos os cards
      colorBgContainer: '#FFFFFF',     // Fundo branco para container dos cards
    },
    Table: {
      headerBg: '#F7F8FA',             // Fundo geral - header da tabela
      headerColor: '#666666',          // Cinza médio - texto do header
      rowHoverBg: '#E8F4FD',           // Azul pastel muito suave - hover da linha (igual ao menu)
      borderColor: '#FFFFFF',          // Branco gelo - bordas
      colorBg: '#FFFFFF',              // Fundo branco para o corpo da tabela
    },
    Form: {
      labelColor: '#666666',           // Cinza médio - labels
      labelRequiredMarkColor: '#F4A6A6', // Rosa claro - marca obrigatória
    },
    Input: {
      hoverBorderColor: '#93CFF0',     // Azul pastel - borda hover
      activeBorderColor: '#93CFF0',    // Azul pastel - borda active
      activeShadow: '0 0 0 2px rgba(147, 207, 240, 0.2)',
    },
    Select: {
      optionSelectedBg: '#e6f4ff',
      optionSelectedColor: '#1677ff',
      optionActiveBg: '#e6f4ff',
    },
    DatePicker: {
      hoverBorderColor: '#93CFF0',     // Azul pastel - borda hover
      activeBorderColor: '#93CFF0',    // Azul pastel - borda active
      activeShadow: '0 0 0 2px rgba(147, 207, 240, 0.2)',
    },
    Dropdown: {
      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.08)',
    },
    Modal: {
      headerBg: '#FFFFFF',             // Branco gelo - header do modal
      contentBg: '#FFFFFF',            // Branco gelo - conteúdo do modal
      footerBg: '#F7F8FA',             // Fundo geral - footer do modal
    },
    Tabs: {
      itemSelectedColor: '#93CFF0',    // Azul pastel - tab selecionada
      itemHoverColor: '#93CFF0',       // Azul pastel - hover da tab
      itemActiveColor: '#93CFF0',      // Azul pastel - tab ativa
      inkBarColor: '#93CFF0',          // Azul pastel - barra indicadora
    },
    Badge: {
      colorBgContainer: '#F4A6A6',     // Rosa claro - fundo do badge
      colorText: '#FFFFFF',            // Branco gelo - texto do badge
    },
    Tag: {
      defaultBg: '#F7F8FA',            // Fundo geral - fundo da tag
      defaultColor: '#666666',         // Cinza médio - texto da tag
    },
    Statistic: {
      titleFontSize: 14,
      contentFontSize: 24,
    },
    Typography: {
      titleMarginTop: 0,
      titleMarginBottom: 16,
    },
    Tooltip: {
      colorText: '#1f1f1f',
      colorBgSpotlight: '#ffffff',
      colorTextLightSolid: '#1f1f1f',
      colorBgElevated: '#ffffff',
    },
  },
};

function App() {
  dayjs.locale('pt-br');
  return (
    <ConfigProvider theme={customTheme} locale={ptBR}>
      <AntdApp>
        <QueryClientProvider client={queryClient}>
          <AuthProvider>
            <Router>
            <div style={{ minHeight: '100vh', backgroundColor: '#F7F8FA' }}>
              <Routes>
                <Route path="/login" element={<AntLogin />} />
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
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
                  path="/users"
                  element={
                    <ProtectedRoute>
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
                  path="/budgets/:id/edit"
                  element={
                    <ProtectedRoute>
                      <AntLayout>
                        <BudgetEdit />
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
                  path="/profile"
                  element={
                    <ProtectedRoute>
                      <AntLayout>
                        <Profile />
                      </AntLayout>
                    </ProtectedRoute>
                  }
                />
              </Routes>
            </div>
          </Router>
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#FFFFFF',
                color: '#333333',
                border: '1px solid #F0F0F0',
                borderRadius: '8px',
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.08)',
                fontFamily: "'Inter', sans-serif",
              },
              success: {
                iconTheme: {
                  primary: '#9FD8A3',
                  secondary: '#FFFFFF',
                },
              },
              error: {
                iconTheme: {
                  primary: '#F4A6A6',
                  secondary: '#FFFFFF',
                },
              },
            }}
          />
        </AuthProvider>
        <ReactQueryDevtools initialIsOpen={false} />
      </QueryClientProvider>
    </AntdApp>
    </ConfigProvider>
  );
}

export default App;
