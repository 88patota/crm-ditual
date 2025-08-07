import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { useAuth } from '../contexts/AuthContext';
import StripeButton from '../components/ui/StripeButton';
import { ModernInput, FormGroup } from '../components/ui/forms';
import { StripeCard, StripeCardContent } from '../components/ui/StripeCard';
import type { LoginRequest } from '../types/auth';
import { LogIn, UserPlus, ArrowRight, User, Lock } from 'lucide-react';

export default function StripeLogin() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<LoginRequest>();

  const onSubmit = async (data: LoginRequest) => {
    setIsLoading(true);
    try {
      await login(data);
      navigate('/dashboard');
    } catch (error: any) {
      if (error.response?.status === 401) {
        setError('root', { message: 'Invalid credentials' });
      } else {
        setError('root', { message: 'An error occurred. Please try again.' });
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 via-purple-50 to-blue-50 py-6 sm:py-12 px-4 sm:px-6 lg:px-8" style={{ colorScheme: 'light' }}>
      <div className="max-w-md w-full">
        {/* Enhanced Header */}
        <div className="text-center mb-6 sm:mb-10">
          <div className="flex items-center justify-center mb-6 sm:mb-8">
            <div className="relative">
              <div className="h-12 w-12 sm:h-16 sm:w-16 rounded-2xl bg-gradient-to-br from-purple-600 via-purple-600 to-blue-600 flex items-center justify-center shadow-2xl">
                <span className="text-white font-bold text-lg sm:text-2xl">C</span>
              </div>
              <div className="absolute -top-1 -right-1 h-4 w-4 sm:h-6 sm:w-6 bg-green-400 rounded-full border-2 border-white"></div>
            </div>
          </div>
          <h2 className="text-2xl sm:text-4xl font-bold text-gray-900 mb-2 sm:mb-3">
            Welcome back
          </h2>
          <p className="text-base sm:text-lg text-gray-600 mb-2">
            Sign in to your CRM Ditual account
          </p>
          <p className="text-sm sm:text-base text-gray-500">
            Don't have an account?{' '}
            <Link
              to="/register"
              className="font-semibold text-purple-600 hover:text-purple-700 transition-colors"
            >
              Create one here
            </Link>
          </p>
        </div>

        {/* Enhanced Login Form */}
        <StripeCard className="stripe-card-elevated shadow-2xl border-0 bg-white">
          <StripeCardContent className="p-4 sm:p-8">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div className="space-y-5">
                <ModernInput
                  label="Username"
                  type="text"
                  placeholder="Enter your username"
                  autoComplete="username"
                  leftIcon={<User className="h-4 w-4" />}
                  error={errors.username?.message}
                  size="lg"
                  variant="filled"
                  {...register('username', {
                    required: 'Username is required',
                    minLength: {
                      value: 3,
                      message: 'Username must be at least 3 characters',
                    },
                  })}
                />

                <ModernInput
                  label="Password"
                  type="password"
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  leftIcon={<Lock className="h-4 w-4" />}
                  error={errors.password?.message}
                  size="lg"
                  variant="filled"
                  {...register('password', {
                    required: 'Password is required',
                    minLength: {
                      value: 8,
                      message: 'Password must be at least 8 characters',
                    },
                  })}
                />
              </div>

              {errors.root && (
                <div className="bg-red-50 border border-red-200 rounded-xl p-4">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm font-medium text-red-800">{errors.root.message}</p>
                    </div>
                  </div>
                </div>
              )}

              <div className="space-y-4">
                <StripeButton
                  type="submit"
                  loading={isLoading}
                  className="w-full h-12 text-base font-semibold"
                  size="lg"
                >
                  {isLoading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Signing in...
                    </>
                  ) : (
                    <>
                      <LogIn className="mr-2 h-5 w-5" />
                      Sign in to Dashboard
                      <ArrowRight className="ml-2 h-5 w-5" />
                    </>
                  )}
                </StripeButton>

                <div className="relative">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-gray-200" />
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="px-2 bg-white text-gray-500">or</span>
                  </div>
                </div>

                <Link to="/register" className="block">
                  <StripeButton
                    type="button"
                    variant="secondary"
                    className="w-full h-12 text-base font-medium"
                    size="lg"
                  >
                    <UserPlus className="mr-2 h-5 w-5" />
                    Create new account
                  </StripeButton>
                </Link>
              </div>
            </form>
          </StripeCardContent>
        </StripeCard>

        {/* Enhanced Demo Credentials */}
        <StripeCard className="mt-6 sm:mt-8 bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
          <StripeCardContent className="p-4 sm:p-6">
            <div>
              <div className="flex items-center justify-center mb-4">
                <div className="bg-blue-100 rounded-full p-2">
                  <svg className="h-5 w-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
              </div>
              <h3 className="text-base sm:text-lg font-semibold text-center text-gray-900 mb-4">Demo Credentials</h3>
              <div className="space-y-3">
                <div className="bg-white rounded-xl p-3 sm:p-4 border border-blue-200">
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                    <div>
                      <p className="font-medium text-gray-900 text-sm sm:text-base">Administrator</p>
                      <p className="text-xs sm:text-sm text-gray-500">Full system access</p>
                    </div>
                    <div className="text-left sm:text-right">
                      <code className="bg-gray-100 px-2 sm:px-3 py-1 rounded-lg text-xs sm:text-sm font-mono">admin</code>
                      <br />
                      <code className="bg-gray-100 px-2 sm:px-3 py-1 rounded-lg text-xs sm:text-sm font-mono mt-1 inline-block">admin123</code>
                    </div>
                  </div>
                </div>
                <div className="bg-white rounded-xl p-3 sm:p-4 border border-blue-200">
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                    <div>
                      <p className="font-medium text-gray-900 text-sm sm:text-base">Sales Representative</p>
                      <p className="text-xs sm:text-sm text-gray-500">Limited access</p>
                    </div>
                    <div className="text-left sm:text-right">
                      <code className="bg-gray-100 px-2 sm:px-3 py-1 rounded-lg text-xs sm:text-sm font-mono">vendedor1</code>
                      <br />
                      <code className="bg-gray-100 px-2 sm:px-3 py-1 rounded-lg text-xs sm:text-sm font-mono mt-1 inline-block">venda123456</code>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </StripeCardContent>
        </StripeCard>

        {/* Enhanced Footer */}
        <div className="text-center mt-6 sm:mt-10 space-y-3 sm:space-y-4">
          <div className="flex items-center justify-center space-x-2">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <p className="text-xs sm:text-sm text-gray-600 font-medium">
              Secure JWT authentication system
            </p>
          </div>
          <p className="text-xs text-gray-500">
            Powered by FastAPI • Built with ❤️ for modern businesses
          </p>
        </div>
      </div>
    </div>
  );
}