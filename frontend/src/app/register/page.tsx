'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { useLang } from '@/contexts/LangContext';

export default function RegisterPage() {
  const { t } = useLang();
  const { register, isLoggedIn, loading } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [phone, setPhone] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!loading && isLoggedIn) router.replace('/');
  }, [loading, isLoggedIn, router]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    setMessage('');
    const result = await register(email, password, {
      firstName: firstName.trim() || undefined,
      lastName: lastName.trim() || undefined,
      phone: phone.trim() || undefined,
    });
    if (!result) {
      router.replace('/');
    } else if (result.includes('email') || result.includes('Подтверди')) {
      setMessage(result);
    } else {
      setError(result);
    }
    setSubmitting(false);
  }

  return (
    <div className="min-h-[70vh] flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-sm">
        <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-8 space-y-5">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{t('register_title')}</h1>
            <p className="text-sm text-gray-500 mt-1">{t('register_subtitle')}</p>
          </div>

          {error && <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-700">{error}</div>}
          {message && <div className="p-3 rounded-lg bg-teal-50 border border-teal-200 text-sm text-teal-700">{message}</div>}

          <form onSubmit={handleSubmit} className="space-y-3">
            {/* Name fields */}
            <div className="grid grid-cols-2 gap-2">
              <input
                value={firstName}
                onChange={(e) => setFirstName(e.target.value.slice(0, 50))}
                placeholder="Имя"
                className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
              />
              <input
                value={lastName}
                onChange={(e) => setLastName(e.target.value.slice(0, 50))}
                placeholder="Фамилия"
                className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
              />
            </div>
            <input
              value={phone}
              onChange={(e) => setPhone(e.target.value.slice(0, 30))}
              placeholder="Телефон (необязательно)"
              type="tel"
              className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
            />
            <div className="border-t border-gray-100 pt-1" />
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder={t('register_ph_email')}
              required
              className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
            />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder={t('register_ph_password')}
              required
              className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
            />
            <button
              type="submit"
              disabled={submitting}
              className="w-full py-2.5 bg-teal-600 text-white font-semibold rounded-xl hover:bg-teal-700 transition-colors disabled:opacity-50"
            >
              {submitting ? '...' : t('register_btn')}
            </button>
          </form>

          <p className="text-sm text-center text-gray-500">
            <Link href="/login" className="text-teal-700 font-medium hover:underline">{t('register_have_account')}</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
