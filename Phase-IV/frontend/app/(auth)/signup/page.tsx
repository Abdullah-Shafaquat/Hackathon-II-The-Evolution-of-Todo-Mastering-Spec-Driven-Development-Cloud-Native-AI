'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import { useToast } from '@/components/ui/ToastContainer';

export default function SignupPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: ''
  });
  const [loading, setLoading] = useState(false);
  const { success, error } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await api.signup(formData);
      success('Account created successfully! Redirecting...');
      router.push('/dashboard');
    } catch (err) {
      error(err instanceof Error ? err.message : 'Signup failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-black via-gray-900 to-black px-4 sm:px-6 lg:px-8 animate-fade-in relative overflow-hidden">
      {/* Background decorative elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-white/5 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-white/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
      </div>

      <div className="max-w-md w-full space-y-8 relative z-10">
        <div className="bg-gradient-to-br from-gray-900 to-black border-2 border-gray-800 rounded-2xl shadow-2xl shadow-white/5 p-8 sm:p-10 animate-scale-in">
          <div className="mb-8">
            <h2 className="text-center text-3xl sm:text-4xl font-bold text-white mb-3 tracking-tight animate-slide-up">
              Create Account
            </h2>
            <div className="h-1 w-20 bg-white mx-auto rounded-full mb-4"></div>
            <p className="text-center text-base text-gray-400 animate-fade-in" style={{ animationDelay: '0.1s' }}>
              Already have an account?{' '}
              <Link href="/login" className="font-bold text-white hover:text-gray-300 transition-colors duration-300 underline underline-offset-4">
                Sign in
              </Link>
            </p>
          </div>

          <form className="space-y-6 animate-fade-in" style={{ animationDelay: '0.2s' }} onSubmit={handleSubmit}>
            <div className="space-y-5">
              <Input
                label="Email address"
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                placeholder="you@example.com"
                fullWidth
              />

              <Input
                label="Name"
                id="name"
                name="name"
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                placeholder="John Doe"
                helperText="Optional - for personalization"
                fullWidth
              />

              <Input
                label="Password"
                id="password"
                name="password"
                type="password"
                required
                minLength={8}
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                placeholder="Minimum 8 characters"
                helperText="Must be at least 8 characters"
                fullWidth
              />
            </div>

            <Button
              type="submit"
              loading={loading}
              fullWidth
              variant="primary"
              className="mt-6"
            >
              <span className="flex items-center justify-center gap-2 text-lg">
                {!loading && (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                  </svg>
                )}
                Create Account
              </span>
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
