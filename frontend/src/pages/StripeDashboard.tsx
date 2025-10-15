import { useAuth } from '../hooks/useAuth';
import { useQuery } from '@tanstack/react-query';
import { authService } from '../services/authService';
import { 
  Users, 
  UserCheck, 
  Shield, 
  Activity, 
  TrendingUp, 
  User, 
  MoreHorizontal,
  Plus,
  Settings,
  BarChart3,
  Clock,
  Calendar
} from 'lucide-react';

export default function StripeDashboard() {
  const { user } = useAuth();

  // Only fetch users if user is admin
  const { data: users = [] } = useQuery({
    queryKey: ['users'],
    queryFn: authService.getAllUsers,
    enabled: user?.role === 'admin',
  });

  const stats = [
    {
      title: 'Total Users',
      value: users.length,
      description: 'All registered users',
      icon: Users,
      trend: { value: 12, isPositive: true },
      visible: user?.role === 'admin',
      variant: 'primary' as const,
    },
    {
      title: 'Active Users',
      value: users.filter(u => u.is_active).length,
      description: 'Currently active',
      icon: UserCheck,
      trend: { value: 8, isPositive: true },
      visible: user?.role === 'admin',
      variant: 'success' as const,
    },
    {
      title: 'Administrators',
      value: users.filter(u => u.role === 'admin').length,
      description: 'Admin accounts',
      icon: Shield,
      trend: { value: 0, isPositive: true },
      visible: user?.role === 'admin',
      variant: 'warning' as const,
    },
    {
      title: 'Account Status',
      value: user?.is_active ? 'Active' : 'Inactive',
      description: 'Your current status',
      icon: Activity,
      visible: true,
      variant: user?.is_active ? 'success' as const : 'error' as const,
    },
  ].filter(stat => stat.visible);

  const recentUsers = users
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 5);

  return (
    <div className="space-y-8" style={{ colorScheme: 'light' }}>
      {/* Stripe-style Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-6">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-2xl font-semibold text-gray-900">
              Dashboard
            </h1>
            <div className="flex items-center gap-1 px-2.5 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">
              <div className="w-1.5 h-1.5 bg-green-500 rounded-full"></div>
              Live
            </div>
          </div>
          <p className="text-sm text-gray-600">
            Welcome back, <span className="font-medium">{user?.full_name}</span>. Here's what's happening with your business today.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-2 px-3 py-2 bg-gray-50 rounded-lg text-sm text-gray-600">
            <Calendar className="h-4 w-4" />
            {new Date().toLocaleDateString('pt-BR', { 
              weekday: 'long',
              year: 'numeric', 
              month: 'short', 
              day: 'numeric' 
            })}
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition-colors">
            <Plus className="h-4 w-4" />
            New Action
          </button>
        </div>
      </div>

      {/* Stripe-style Metrics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.title} className="bg-white border border-gray-200 rounded-lg p-4 hover:border-gray-300 transition-colors min-h-[140px] flex flex-col">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <div className="p-2 bg-gray-50 rounded-lg">
                  <stat.icon className="h-4 w-4 text-gray-600" />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="text-xs font-medium text-gray-600 truncate">{stat.title}</p>
                </div>
              </div>
              <button className="p-1 hover:bg-gray-50 rounded flex-shrink-0">
                <MoreHorizontal className="h-3 w-3 text-gray-400" />
              </button>
            </div>
            <div className="flex-1 flex flex-col justify-center space-y-1 overflow-hidden">
              <p className="text-xl font-semibold text-gray-900 truncate overflow-hidden text-ellipsis whitespace-nowrap" style={{ lineHeight: '1.4', paddingBottom: '1px', minHeight: '24px' }}>{stat.value}</p>
              {stat.trend && (
                <div className="flex items-center gap-1 overflow-hidden">
                  <TrendingUp className="h-3 w-3 text-green-500 flex-shrink-0" />
                  <span className="text-xs text-green-600 font-medium">+{stat.trend.value}%</span>
                  <span className="text-xs text-gray-500 truncate overflow-hidden text-ellipsis">vs last month</span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        {/* Profile Card - Stripe Style */}
        <div className="xl:col-span-2 bg-white border border-gray-200 rounded-lg">
          <div className="flex items-center justify-between p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Account Overview</h3>
            <button className="flex items-center gap-2 px-3 py-1.5 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors">
              <Settings className="h-4 w-4" />
              Manage
            </button>
          </div>
          <div className="p-6">
            <div className="flex items-start gap-4 mb-6">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-gray-900 text-white font-semibold">
                {user?.full_name?.charAt(0).toUpperCase()}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="text-lg font-semibold text-gray-900">{user?.full_name}</h4>
                  <span className={`inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium rounded-full ${
                    user?.is_active 
                      ? 'bg-green-100 text-green-700' 
                      : 'bg-red-100 text-red-700'
                  }`}>
                    <div className={`w-1.5 h-1.5 rounded-full ${
                      user?.is_active ? 'bg-green-500' : 'bg-red-500'
                    }`}></div>
                    {user?.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
                <p className="text-sm text-gray-600 mb-1">{user?.email}</p>
                <div className="flex items-center gap-4 text-xs text-gray-500">
                  <span>@{user?.username}</span>
                  <span>•</span>
                  <span className="capitalize">{user?.role}</span>
                  <span>•</span>
                  <span>Member since {user?.created_at ? new Date(user.created_at).toLocaleDateString('pt-BR', { 
                    month: 'short', 
                    year: 'numeric' 
                  }) : 'N/A'}</span>
                </div>
              </div>
            </div>
            
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="p-3 bg-gray-50 rounded-lg min-h-[70px] flex flex-col justify-center">
                <div className="flex items-center gap-2 mb-1">
                  <User className="h-3 w-3 text-gray-500 flex-shrink-0" />
                  <span className="text-xs font-medium text-gray-700">Role</span>
                </div>
                <p className="text-xs text-gray-900 font-semibold capitalize truncate">{user?.role}</p>
              </div>
              <div className="p-3 bg-gray-50 rounded-lg min-h-[70px] flex flex-col justify-center">
                <div className="flex items-center gap-2 mb-1">
                  <Clock className="h-3 w-3 text-gray-500 flex-shrink-0" />
                  <span className="text-xs font-medium text-gray-700">Activity</span>
                </div>
                <p className="text-xs text-gray-900 font-semibold truncate">Just now</p>
              </div>
              <div className="p-3 bg-gray-50 rounded-lg min-h-[70px] flex flex-col justify-center">
                <div className="flex items-center gap-2 mb-1">
                  <Shield className="h-3 w-3 text-gray-500 flex-shrink-0" />
                  <span className="text-xs font-medium text-gray-700">Access</span>
                </div>
                <p className="text-xs text-gray-900 font-semibold truncate">
                  {user?.role === 'admin' ? 'Full' : 'Limited'}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Activity - Stripe Style */}
        <div className="bg-white border border-gray-200 rounded-lg">
          <div className="flex items-center justify-between p-6 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
            <button className="text-sm text-gray-600 hover:text-gray-900">View all</button>
          </div>
          <div className="p-6">
            {user?.role === 'admin' && recentUsers.length > 0 ? (
              <div className="space-y-4">
                {recentUsers.map((recentUser) => (
                  <div key={recentUser.id} className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gray-100 text-gray-700 text-sm font-medium">
                      {recentUser.full_name.charAt(0).toUpperCase()}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-gray-900">
                        <span className="font-medium">{recentUser.full_name}</span> joined the team
                      </p>
                      <p className="text-xs text-gray-500">
                        {new Date(recentUser.created_at).toLocaleDateString('pt-BR', {
                          day: 'numeric',
                          month: 'short',
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </p>
                    </div>
                    <span className={`inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-full ${
                      recentUser.role === 'admin' 
                        ? 'bg-purple-100 text-purple-700' 
                        : 'bg-blue-100 text-blue-700'
                    }`}>
                      {recentUser.role === 'admin' ? 'Admin' : 'Sales'}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mx-auto mb-3">
                  <Activity className="h-6 w-6 text-gray-400" />
                </div>
                <p className="text-sm text-gray-500">No recent activity</p>
                <p className="text-xs text-gray-400 mt-1">Activity will appear here as it happens</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Quick Actions - Stripe Style */}
      <div className="bg-white border border-gray-200 rounded-lg">
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Quick Actions</h3>
          <span className="text-sm text-gray-500">Shortcuts to common tasks</span>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {/* Manage Profile */}
            <button className="flex items-center gap-4 p-4 text-left border border-gray-200 rounded-lg hover:border-gray-300 hover:bg-gray-50 transition-colors group min-h-[88px]">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gray-100 group-hover:bg-gray-200 transition-colors flex-shrink-0">
                <User className="h-5 w-5 text-gray-600" />
              </div>
              <div className="flex-1">
                <p className="font-medium text-gray-900 text-sm truncate">Manage Profile</p>
                <p className="text-xs text-gray-500 truncate">Update account settings</p>
              </div>
            </button>
            
            {user?.role === 'admin' && (
              <>
                {/* Add User */}
                <button className="flex items-center gap-4 p-4 text-left border border-gray-200 rounded-lg hover:border-gray-300 hover:bg-gray-50 transition-colors group min-h-[88px]">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-blue-100 group-hover:bg-blue-200 transition-colors flex-shrink-0">
                    <UserCheck className="h-5 w-5 text-blue-600" />
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-gray-900 text-sm truncate">Add User</p>
                    <p className="text-xs text-gray-500 truncate">Invite team members</p>
                  </div>
                </button>
                
                {/* View Reports */}
                <button className="flex items-center gap-4 p-4 text-left border border-gray-200 rounded-lg hover:border-gray-300 hover:bg-gray-50 transition-colors group min-h-[88px]">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-green-100 group-hover:bg-green-200 transition-colors flex-shrink-0">
                    <BarChart3 className="h-5 w-5 text-green-600" />
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-gray-900 text-sm truncate">View Reports</p>
                    <p className="text-xs text-gray-500 truncate">Analytics & insights</p>
                  </div>
                </button>
              </>
            )}          
          </div>
          
          {/* Additional Actions */}
          <div className="mt-6 pt-6 border-t border-gray-200">
            <div className="flex flex-wrap gap-2">
              <button className="inline-flex items-center gap-1 px-3 py-1.5 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
                <Settings className="h-4 w-4" />
                Settings
              </button>
              <button className="inline-flex items-center gap-1 px-3 py-1.5 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
                <BarChart3 className="h-4 w-4" />
                Analytics
              </button>
              {user?.role === 'admin' && (
                <button className="inline-flex items-center gap-1 px-3 py-1.5 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors">
                  <Users className="h-4 w-4" />
                  Manage Users
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}