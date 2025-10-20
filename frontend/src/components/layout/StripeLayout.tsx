import { Link, useLocation } from 'react-router-dom';
import { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { BarChart3, Users, User, LogOut, Home, Settings, Menu, X } from 'lucide-react';

interface StripeLayoutProps {
  children: React.ReactNode;
}

export default function StripeLayout({ children }: StripeLayoutProps) {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const navigation = [
    {
      name: 'Dashboard',
      href: '/dashboard',
      icon: Home,
      current: location.pathname === '/dashboard',
    },
    {
      name: 'Profile',
      href: '/profile',
      icon: User,
      current: location.pathname === '/profile',
    },
  ];

  // Add admin-only navigation
  if (user?.role === 'admin') {
    navigation.splice(1, 0, {
      name: 'Users',
      href: '/users',
      icon: Users,
      current: location.pathname === '/users',
    });
  }

  return (
    <div className="min-h-screen bg-gray-50" style={{ colorScheme: 'light' }}>
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Enhanced Stripe-style Sidebar - Always Fixed */}
      <aside className={`stripe-sidebar ${sidebarOpen ? 'open' : ''} bg-white border-r border-gray-200`} style={{ position: 'fixed', left: '0', top: '0', width: '200px', height: '100vh', zIndex: 50 }}>
        {/* Logo Section */}
        <div className="flex h-16 items-center justify-center border-b border-gray-100 px-4">
          <div className="flex flex-col text-center">
            <h1 className="text-lg font-bold" style={{ color: '#e11d48' }}>LoenCRM</h1>
            <p className="text-xs text-gray-500 font-medium">Conecte. Entenda. Cresça.</p>
          </div>
        </div>
        
        {/* Navigation */}
        <nav className="flex-1 px-3 py-4">
          <ul className="flex flex-col gap-1">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <li key={item.name}>
                  <Link
                    to={item.href}
                    className={`flex items-center gap-3 px-3 py-2 rounded-lg font-medium text-gray-700 hover:bg-gray-100 transition-colors ${item.current ? 'bg-gray-100 text-primary-700' : ''}`}
                  >
                    <Icon className="w-5 h-5 flex-shrink-0" />
                    <span className="truncate">{item.name}</span>
                  </Link>
                </li>
              );
            })}
          </ul>

          {/* Admin Section */}
          {user?.role === 'admin' && (
            <div className="mt-8 pt-4 border-t border-gray-100">
              <p className="px-3 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">
                Administration
              </p>
              <ul className="flex flex-col gap-1">
                <li>
                  <a href="#" className="flex items-center gap-3 px-3 py-2 rounded-lg font-medium text-gray-700 hover:bg-gray-100 transition-colors">
                    <Settings className="w-5 h-5 flex-shrink-0" />
                    <span>Settings</span>
                  </a>
                </li>
                <li>
                  <a href="#" className="flex items-center gap-3 px-3 py-2 rounded-lg font-medium text-gray-700 hover:bg-gray-100 transition-colors">
                    <BarChart3 className="w-5 h-5 flex-shrink-0" />
                    <span>Analytics</span>
                  </a>
                </li>
              </ul>
            </div>
          )}
        </nav>

        {/* User Profile Section */}
        <div className="border-t border-gray-100 p-3">
          <div className="flex items-center space-x-2 mb-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-purple-100 to-blue-100 ring-2 ring-purple-500/20">
              <span className="text-xs font-semibold text-purple-700">
                {user?.full_name?.charAt(0).toUpperCase()}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-medium text-gray-900 truncate">{user?.full_name}</p>
              <p className="text-xs text-gray-500 capitalize flex items-center">
                {user?.role}
                <span className="ml-1 inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  Online
                </span>
              </p>
            </div>
            <button
              onClick={logout}
              className="flex h-6 w-6 items-center justify-center rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-all duration-200"
              title="Logout"
            >
              <LogOut className="h-3 w-3" />
            </button>
          </div>
        </div>
      </aside>

      {/* Enhanced Header Bar */}
      <header className="ml-0 lg:ml-50 bg-white border-b border-gray-100 px-4 lg:px-8 py-4 flex items-center justify-between" style={{ marginLeft: '200px' }}>
        <div className="flex items-center space-x-4">
          {/* Mobile menu button */}
          <button
            className="lg:hidden p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
          
          <h2 className="text-lg font-semibold text-gray-900">
            {navigation.find(item => item.current)?.name || 'Dashboard'}
          </h2>
        </div>
        <div className="flex items-center space-x-2 lg:space-x-4">
          <div className="hidden lg:flex items-center space-x-2">
            <div className="h-8 w-8 rounded-full bg-gradient-to-br from-purple-100 to-blue-100 flex items-center justify-center">
              <span className="text-xs font-semibold text-purple-700">
                {user?.full_name?.charAt(0).toUpperCase()}
              </span>
            </div>
            <span className="text-sm font-medium text-gray-700">{user?.full_name}</span>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="ml-0 lg:ml-50 p-4 lg:p-8" style={{ marginLeft: '200px' }}>
        {children}
      </main>
    </div>
  );
}