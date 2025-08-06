
import { useForm } from 'react-hook-form';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useAuth } from '../contexts/AuthContext';
import { authService } from '../services/authService';
import StripeButton from '../components/ui/StripeButton';
import { ModernInput, FormGroup } from '../components/ui/forms';
import { StripeCard, StripeCardContent, StripeCardHeader, StripeCardTitle } from '../components/ui/StripeCard';
import StripeBadge from '../components/ui/StripeBadge';
import type { UserSelfUpdateRequest, PasswordUpdateRequest } from '../types/auth';
import { User, Lock, Save, Mail, Calendar } from 'lucide-react';
import toast from 'react-hot-toast';

export default function Profile() {
  const { user } = useAuth();
  const queryClient = useQueryClient();


  // Profile update form
  const profileForm = useForm<UserSelfUpdateRequest>({
    defaultValues: {
      full_name: user?.full_name || '',
      email: user?.email || '',
      username: user?.username || '',
    },
  });

  // Password update form
  const passwordForm = useForm<PasswordUpdateRequest>();

  // Mutations
  const updateProfileMutation = useMutation({
    mutationFn: authService.updateProfile,
    onSuccess: () => {
      toast.success('Profile updated successfully!');
      queryClient.invalidateQueries({ queryKey: ['user'] });
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update profile');
    },
  });

  const updatePasswordMutation = useMutation({
    mutationFn: authService.changePassword,
    onSuccess: () => {
      toast.success('Password updated successfully!');
      passwordForm.reset();
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to update password');
    },
  });

  const onProfileSubmit = (data: UserSelfUpdateRequest) => {
    updateProfileMutation.mutate(data);
  };

  const onPasswordSubmit = (data: PasswordUpdateRequest) => {
    updatePasswordMutation.mutate(data);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Profile Settings</h1>
        <p className="mt-1 text-sm text-gray-600">
          Manage your account information and password.
        </p>
      </div>

      <div className="grid-2">
        {/* Profile Information */}
        <StripeCard>
          <StripeCardHeader>
            <StripeCardTitle>Profile Information</StripeCardTitle>
          </StripeCardHeader>
          <StripeCardContent>
            <form onSubmit={profileForm.handleSubmit(onProfileSubmit)}>
              <FormGroup>
                <ModernInput
                  label="Full Name"
                  placeholder="Enter your full name"
                  leftIcon={<User className="h-4 w-4" />}
                  error={profileForm.formState.errors.full_name?.message}
                  {...profileForm.register('full_name', {
                    required: 'Full name is required',
                  })}
                />

                <ModernInput
                  label="Email"
                  type="email"
                  placeholder="Enter your email"
                  leftIcon={<Mail className="h-4 w-4" />}
                  error={profileForm.formState.errors.email?.message}
                  {...profileForm.register('email', {
                    required: 'Email is required',
                    pattern: {
                      value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                      message: 'Invalid email address',
                    },
                  })}
                />

                <ModernInput
                  label="Username"
                  placeholder="Enter your username"
                  leftIcon={<User className="h-4 w-4" />}
                  error={profileForm.formState.errors.username?.message}
                  {...profileForm.register('username', {
                    required: 'Username is required',
                    minLength: {
                      value: 3,
                      message: 'Username must be at least 3 characters',
                    },
                  })}
                />

                <div className="flex items-center space-x-4 pt-2">
                  <StripeButton
                    type="submit"
                    loading={updateProfileMutation.isPending}
                  >
                    <Save className="mr-2 h-4 w-4" />
                    Save Changes
                  </StripeButton>
                  <StripeButton
                    type="button"
                    variant="secondary"
                    onClick={() => profileForm.reset()}
                  >
                    Reset
                  </StripeButton>
                </div>
              </FormGroup>
            </form>
          </StripeCardContent>
        </StripeCard>

        {/* Password Change */}
        <StripeCard>
          <StripeCardHeader>
            <StripeCardTitle>Change Password</StripeCardTitle>
          </StripeCardHeader>
          <StripeCardContent>
            <form onSubmit={passwordForm.handleSubmit(onPasswordSubmit)}>
              <FormGroup>
                <ModernInput
                  label="Current Password"
                  type="password"
                  placeholder="Enter current password"
                  leftIcon={<Lock className="h-4 w-4" />}
                  error={passwordForm.formState.errors.current_password?.message}
                  {...passwordForm.register('current_password', {
                    required: 'Current password is required',
                  })}
                />

                <ModernInput
                  label="New Password"
                  type="password"
                  placeholder="Enter new password"
                  leftIcon={<Lock className="h-4 w-4" />}
                  error={passwordForm.formState.errors.new_password?.message}
                  helperText="Minimum 8 characters required"
                  {...passwordForm.register('new_password', {
                    required: 'New password is required',
                    minLength: {
                      value: 8,
                      message: 'Password must be at least 8 characters',
                    },
                  })}
                />

                <div className="flex items-center space-x-4 pt-2">
                  <StripeButton
                    type="submit"
                    loading={updatePasswordMutation.isPending}
                  >
                    <Save className="mr-2 h-4 w-4" />
                    Update Password
                  </StripeButton>
                  <StripeButton
                    type="button"
                    variant="secondary"
                    onClick={() => passwordForm.reset()}
                  >
                    Cancel
                  </StripeButton>
                </div>
              </FormGroup>
            </form>
          </StripeCardContent>
        </StripeCard>
      </div>

      {/* Account Information */}
      <StripeCard>
        <StripeCardHeader>
          <StripeCardTitle>Account Information</StripeCardTitle>
        </StripeCardHeader>
        <StripeCardContent>
          <div className="space-y-4">
            <div className="flex items-center justify-between py-3 border-b border-gray-100">
              <div>
                <span className="text-sm font-medium text-gray-900">Role</span>
                <p className="text-sm text-gray-500">Your account role and permissions</p>
              </div>
              <StripeBadge variant={user?.role === 'admin' ? 'primary' : 'success'}>
                {user?.role === 'admin' ? 'Administrator' : 'Sales Representative'}
              </StripeBadge>
            </div>
            
            <div className="flex items-center justify-between py-3 border-b border-gray-100">
              <div>
                <span className="text-sm font-medium text-gray-900">Account Status</span>
                <p className="text-sm text-gray-500">Current account status</p>
              </div>
              <StripeBadge variant={user?.is_active ? 'success' : 'error'}>
                {user?.is_active ? 'Active' : 'Inactive'}
              </StripeBadge>
            </div>
            
            <div className="flex items-center justify-between py-3">
              <div>
                <span className="text-sm font-medium text-gray-900">Member Since</span>
                <p className="text-sm text-gray-500">Account creation date</p>
              </div>
              <div className="flex items-center text-sm text-gray-600">
                <Calendar className="mr-1 h-4 w-4" />
                {user?.created_at ? new Date(user.created_at).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                }) : 'N/A'}
              </div>
            </div>
          </div>
        </StripeCardContent>
      </StripeCard>
    </div>
  );
}