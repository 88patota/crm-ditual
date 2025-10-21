import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { ConfigProvider, theme } from 'antd';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/auth/ProtectedRoute';
import AntLayout from './components/layout/AntLayout';

// Páginas
import AntLogin from './pages/AntLogin';
import AntDashboard from './pages/AntDashboard';
import Users from './pages/Users';
import Budgets from './pages/Budgets';
import BudgetCreate from './pages/BudgetCreate';
import BudgetEdit from './pages/BudgetEdit';
import BudgetView from './pages/BudgetView';
import Profile from './pages/Profile';
import MarkupSettings from './components/settings/MarkupSettings';

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
    // === CORES PRINCIPAIS (Base da Paleta) ===
    colorPrimary: '#93CFF0',           // Azul pastel - cor principal (ações, botões primários, links)
    colorSuccess: '#86E2A1',           // Verde pastel - sucesso (geral)
    colorWarning: '#FFE8A1',           // Amarelo pastel - aviso (alertas de atenção)
    colorError: '#F4A6A6',             // Rosa claro - erro (geral)
    colorInfo: '#A7D8F5',              // Azul claro - informação (mensagens neutras)
    
    // === CORES DE FUNDO (Base) ===
    colorBgContainer: '#F7F8FA',       // Fundo geral - cinza muito claro
    colorBgElevated: '#FFFFFF',        // Branco gelo - cards e blocos
    colorBgLayout: '#F7F8FA',          // Fundo geral das telas e dashboards
    colorBgSpotlight: '#FFFFFF',       // Branco gelo para destaques
    
    // === CORES DE TEXTO (Base) ===
    colorText: '#333333',              // Cinza escuro - texto principal
    colorTextSecondary: '#666666',     // Cinza médio - texto secundário
    colorTextTertiary: '#666666',      // Cinza médio - labels, descrições, tooltips
    colorTextQuaternary: '#666666',    // Cinza médio
    
    // === CORES DE BORDA ===
    colorBorder: '#FFFFFF',            // Branco gelo - boa legibilidade
    colorBorderSecondary: '#FFFFFF',   // Branco gelo - bordas secundárias
    
    // === SOMBRAS ===
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
    boxShadowSecondary: '0 4px 12px rgba(0, 0, 0, 0.08)',
    
    // === TIPOGRAFIA ===
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif",
    fontSize: 14,
    fontSizeHeading1: 32,
    fontSizeHeading2: 24,
    fontSizeHeading3: 20,
    fontSizeHeading4: 16,
    fontSizeHeading5: 14,
    
    // === BORDAS ARREDONDADAS ===
    borderRadius: 8,
    borderRadiusLG: 12,
    borderRadiusSM: 6,
    
    // === ESPAÇAMENTOS ===
    padding: 16,
    paddingLG: 24,
    paddingSM: 12,
    paddingXS: 8,
    
    // === CORES ESPECÍFICAS DE COMPONENTES ===
    colorFillAlter: '#F7F8FA',         // Fundo geral
    colorFillContent: '#FFFFFF',       // Branco gelo - fundo de conteúdo
    colorFillContentHover: '#C8A2C8',  // Lilás claro - hover
    
    // === MENU ===
    colorBgMenuItemSelected: '#C8A2C8', // Lilás claro - item de menu selecionado
    colorTextMenuItemSelected: '#93CFF0', // Azul pastel - texto do item selecionado
    
    // === BOTÕES ===
    colorPrimaryHover: '#93CFF0',      // Azul pastel - hover do botão primário
    colorPrimaryActive: '#93CFF0',     // Azul pastel - active do botão primário
    
    // === INPUTS ===
    colorBgContainerDisabled: '#FFFFFF', // Branco gelo - fundo de input desabilitado
    colorTextDisabled: '#666666',      // Cinza médio - texto desabilitado
    
    // === LINKS ===
    colorLink: '#93CFF0',              // Azul pastel - cor dos links
    colorLinkHover: '#93CFF0',         // Azul pastel - hover dos links
    colorLinkActive: '#93CFF0',        // Azul pastel - active dos links
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
      itemSelectedBg: '#E8F4FD',       // Azul pastel muito suave - item selecionado
      itemSelectedColor: '#93CFF0',    // Azul pastel - texto selecionado
      itemHoverBg: '#E8F4FD',          // Azul pastel muito suave - hover
      itemHoverColor: '#93CFF0',       // Azul pastel - texto hover
      itemActiveBg: '#E8F4FD',         // Azul pastel muito suave - active
      subMenuItemBg: 'transparent',
      groupTitleColor: '#666666',      // Cinza médio - títulos de grupo
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
      optionSelectedBg: '#C8A2C8',     // Lilás claro - opção selecionada
      optionSelectedColor: '#93CFF0',  // Azul pastel - texto selecionado
      optionActiveBg: '#C8A2C8',       // Lilás claro - opção ativa
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
      colorText: '#000000',            // Preto - texto do tooltip
      colorBgSpotlight: '#ffffff',     // Fundo branco para o tooltip
      colorTextLightSolid: '#000000',  // Força texto preto
      colorBgElevated: '#ffffff',      // Fundo branco elevado
    },
  },
};

function App() {
  return (
    <ConfigProvider theme={customTheme}>
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
                        <BudgetCreate />
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
                <Route
                  path="/markup-settings"
                  element={
                    <ProtectedRoute>
                      <AntLayout>
                        <MarkupSettings />
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
    </ConfigProvider>
  );
}

export default App;
