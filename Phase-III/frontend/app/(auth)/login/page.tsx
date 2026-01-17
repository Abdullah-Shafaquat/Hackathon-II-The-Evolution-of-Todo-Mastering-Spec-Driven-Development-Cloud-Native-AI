'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/api';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import { useToast } from '@/components/ui/ToastContainer';

export default function LoginPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    remember_me: false
  });
  const [loading, setLoading] = useState(false);
  const { success, error } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await api.login(formData);
      success('Login successful! Redirecting...');
      router.push('/dashboard');
    } catch (err) {
      error(err instanceof Error ? err.message : 'Login failed');
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
              Welcome Back
            </h2>
            <div className="h-1 w-20 bg-white mx-auto rounded-full mb-4"></div>
            <p className="text-center text-base text-gray-400 animate-fade-in" style={{ animationDelay: '0.1s' }}>
              Don&apos;t have an account?{' '}
              <Link href="/signup" className="font-bold text-white hover:text-gray-300 transition-colors duration-300 underline underline-offset-4">
                Sign up
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
                label="Password"
                id="password"
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                placeholder="Enter your password"
                fullWidth
              />

              <div className="flex items-center">
                <input
                  id="remember_me"
                  name="remember_me"
                  type="checkbox"
                  checked={formData.remember_me}
                  onChange={(e) => setFormData({ ...formData, remember_me: e.target.checked })}
                  className="h-5 w-5 bg-gray-800 border-2 border-gray-700 text-white rounded focus:ring-2 focus:ring-white transition-all duration-300 cursor-pointer"
                />
                <label htmlFor="remember_me" className="ml-3 block text-sm text-gray-300 font-medium">
                  Remember me
                </label>
              </div>
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
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                  </svg>
                )}
                Sign in
              </span>
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
