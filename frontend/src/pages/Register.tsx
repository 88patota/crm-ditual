import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { useAuth } from '../hooks/useAuth';
import StripeButton from '../components/ui/StripeButton';
import { ModernInput, FormGroup } from '../components/ui/forms';
import { StripeCard, StripeCardContent } from '../components/ui/StripeCard';
import type { RegisterRequest } from '../types/auth';
import { UserPlus, ArrowLeft, User, Mail, Lock } from 'lucide-react';

export default function Register() {
  const { register: registerUser } = useAuth();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<RegisterRequest>();

  const onSubmit = async (data: RegisterRequest) => {
    setIsLoading(true);
    try {
      await registerUser(data);
      navigate('/dashboard');
    } catch (error: unknown) {
      const axiosError = error as { response?: { data?: { detail?: string } } };
      if (axiosError.response?.data?.detail) {
        setError('root', { message: axiosError.response.data.detail });
      } else {
        setError('root', { message: 'An error occurred. Please try again.' });
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-6">
            <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-purple-600 to-blue-600 flex items-center justify-center">
              <span className="text-white font-bold text-lg">C</span>
            </div>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Create your account
          </h2>
          <p className="text-gray-600">
            Or{' '}
            <Link
              to="/login"
              className="font-medium text-purple-600 hover:text-purple-500 transition-colors"
            >
              sign in to existing account
            </Link>
          </p>
        </div>

        {/* Register Form */}
        <StripeCard>
          <StripeCardContent>
            <form onSubmit={handleSubmit(onSubmit)}>
              <FormGroup spacing="lg">
                <ModernInput
                  label="Full Name"
                  type="text"
                  placeholder="Enter your full name"
                  autoComplete="name"
                  leftIcon={<User className="h-4 w-4" />}
                  error={errors.full_name?.message}
                  size="lg"
                  {...register('full_name', {
                    required: 'Full name is required',
                  })}
                />

                <ModernInput
                  label="Email Address"
                  type="email"
                  placeholder="Enter your email"
                  autoComplete="email"
                  leftIcon={<Mail className="h-4 w-4" />}
                  error={errors.email?.message}
                  size="lg"
                  {...register('email', {
                    required: 'Email is required',
                    pattern: {
                      value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                      message: 'Invalid email address',
                    },
                  })}
                />

                <ModernInput
                  label="Username"
                  type="text"
                  placeholder="Choose a username"
                  autoComplete="username"
                  leftIcon={<User className="h-4 w-4" />}
                  error={errors.username?.message}
                  size="lg"
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
                  placeholder="Create a password"
                  autoComplete="new-password"
                  leftIcon={<Lock className="h-4 w-4" />}
                  error={errors.password?.message}
                  size="lg"
                  helperText="Minimum 8 characters required"
                  {...register('password', {
                    required: 'Password is required',
                    minLength: {
                      value: 8,
                      message: 'Password must be at least 8 characters',
                    },
                  })}
                />

                {errors.root && (
                  <div className="stripe-alert stripe-alert-error">
                    {errors.root.message}
                  </div>
                )}

                <div className="space-y-3">
                  <StripeButton
                    type="submit"
                    loading={isLoading}
                    className="w-full"
                    size="lg"
                  >
                    <UserPlus className="mr-2 h-4 w-4" />
                    Create account
                  </StripeButton>

                  <Link to="/login" className="block">
                    <StripeButton
                      type="button"
                      variant="secondary"
                      className="w-full"
                      size="lg"
                    >
                      <ArrowLeft className="mr-2 h-4 w-4" />
                      Back to login
                    </StripeButton>
                  </Link>
                </div>
              </FormGroup>
            </form>
          </StripeCardContent>
        </StripeCard>

        {/* Footer */}
        <div className="text-center mt-8">
          <p className="text-xs text-gray-500">
            By creating an account, you agree to our terms of service
          </p>
        </div>
      </div>
    </div>
  );
}