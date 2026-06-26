'use client';

import { useEffect, useState } from 'react';
import { useRequireAuth } from '@/hooks/useRequireAuth';
import { useLang } from '@/contexts/LangContext';
import { getAuthedClient, getSupabase } from '@/lib/supabase';

export default function ProfilePage() {
  const { t } = useLang();
  const auth = useRequireAuth();

  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [phone, setPhone] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [listingCount, setListingCount] = useState<number | null>(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    if (!auth.isLoggedIn || !auth.accessToken || !auth.userId) return;
    const sb = getAuthedClient(auth.accessToken);
    Promise.all([
      sb.from('profiles').select('first_name,last_name,phone').eq('id', auth.userId).limit(1).single(),
      getSupabase().from('listings').select('id', { count: 'exact', head: true }).eq('owner_id', auth.userId),
    ]).then(([profileRes, countRes]) => {
      if (profileRes.data) {
        setFirstName((profileRes.data.first_name as string | null) ?? '');
        setLastName((profileRes.data.last_name as string | null) ?? '');
        setPhone((profileRes.data.phone as string | null) ?? '');
      }
      setListingCount(countRes.count ?? 0);
      setLoading(false);
    });
  }, [auth.isLoggedIn, auth.accessToken, auth.userId]);

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    if (!auth.accessToken || !auth.userId) return;
    setSaving(true);
    setError('');
    setSuccess('');
    const sb = getAuthedClient(auth.accessToken);
    const { error: err } = await sb.from('profiles').update({
      first_name: firstName.trim().slice(0, 50) || null,
      last_name: lastName.trim().slice(0, 50) || null,
      phone: phone.trim().slice(0, 30) || null,
    }).eq('id', auth.userId);
    setSaving(false);
    if (err) { setError('Не удалось сохранить данные.'); return; }
    setSuccess('Данные сохранены.');
    await auth.reload();
  }

  const initials = (firstName.trim()[0] ?? auth.userName?.[0] ?? '?').toUpperCase();
  const displayName = [firstName.trim(), lastName.trim()].filter(Boolean).join(' ') || auth.userName || auth.userEmail || '';

  if (auth.loading || loading) return <div className="flex items-center justify-center min-h-[50vh]"><span className="text-gray-400">...</span></div>;

  return (
    <div className="max-w-xl mx-auto px-4 py-6 space-y-5">
      <h1 className="text-2xl font-bold text-gray-900">{t('profile_title')}</h1>

      {/* Avatar + name */}
      <div className="bg-white rounded-2xl border border-gray-200 p-5 flex items-center gap-4">
        <div className="w-14 h-14 rounded-full bg-gradient-to-br from-teal-500 to-teal-700 flex items-center justify-center text-white font-bold text-2xl flex-shrink-0">
          {initials}
        </div>
        <div className="min-w-0">
          <div className="font-bold text-gray-900 text-base truncate">{displayName}</div>
          <div className="text-sm text-gray-400 truncate">{auth.userEmail}</div>
          {auth.isBlocked && (
            <span className="mt-1 inline-block text-xs bg-red-50 text-red-600 border border-red-200 px-2 py-0.5 rounded-full">{t('profile_blocked_msg')}</span>
          )}
        </div>
      </div>

      {/* Stats */}
      {listingCount !== null && (
        <div className="bg-white rounded-2xl border border-gray-200 p-4 flex items-center gap-4">
          <div className="text-center flex-1">
            <div className="text-2xl font-extrabold text-teal-700">{listingCount}</div>
            <div className="text-xs text-gray-500 mt-0.5">объявлений</div>
          </div>
        </div>
      )}

      {/* Edit form */}
      <div className="bg-white rounded-2xl border border-gray-200 p-5 space-y-4">
        <h2 className="font-semibold text-gray-800 text-base">Личные данные</h2>

        {error && <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-700">{error}</div>}
        {success && <div className="p-3 rounded-lg bg-green-50 border border-green-200 text-sm text-green-700">{success}</div>}

        <form onSubmit={handleSave} className="space-y-3">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs font-medium text-gray-500 block mb-1">Имя</label>
              <input
                value={firstName}
                onChange={(e) => setFirstName(e.target.value.slice(0, 50))}
                placeholder="Введите имя"
                className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>
            <div>
              <label className="text-xs font-medium text-gray-500 block mb-1">Фамилия</label>
              <input
                value={lastName}
                onChange={(e) => setLastName(e.target.value.slice(0, 50))}
                placeholder="Введите фамилию"
                className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>
          </div>
          <div>
            <label className="text-xs font-medium text-gray-500 block mb-1">Номер телефона</label>
            <input
              value={phone}
              onChange={(e) => setPhone(e.target.value.slice(0, 30))}
              placeholder="+998 90 000 00 00"
              type="tel"
              className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
          </div>

          {/* Email (readonly) */}
          <div>
            <label className="text-xs font-medium text-gray-500 block mb-1">Email</label>
            <div className="flex items-center gap-2 px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm text-gray-500">
              <svg className="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              {auth.userEmail}
            </div>
          </div>

          <div className="flex items-center gap-3 pt-1">
            <button
              type="submit"
              disabled={saving}
              className="px-5 py-2.5 bg-teal-600 text-white text-sm font-semibold rounded-xl hover:bg-teal-700 transition-colors disabled:opacity-50"
            >
              {saving ? 'Сохранение...' : 'Сохранить'}
            </button>
            <button
              type="button"
              onClick={auth.logout}
              className="text-sm text-red-500 hover:text-red-700 transition-colors underline"
            >
              {t('nav_sign_out')}
            </button>
          </div>
        </form>
      </div>

      {/* Subscription plans */}
      <div className="space-y-3">
        <div className="flex items-center gap-2">
          <h2 className="font-bold text-gray-900">{t('profile_subscription_title')}</h2>
          <span className="text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full font-medium">{t('profile_demo_badge')}</span>
        </div>
        <p className="text-sm text-gray-500">{t('profile_demo_desc')}</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white rounded-2xl border border-gray-200 p-5 space-y-4">
            <div>
              <div className="text-lg font-bold text-gray-900">Free</div>
              <div className="text-3xl font-extrabold text-gray-900 mt-1">$0<span className="text-base font-normal text-gray-400">/mo</span></div>
              <p className="text-xs text-gray-500 mt-1">{t('profile_free_desc')}</p>
            </div>
            <ul className="space-y-1.5 text-sm text-gray-700">
              {[t('profile_feat_basic'), t('profile_feat_filters')].map((f) => (
                <li key={f} className="flex items-center gap-2"><span className="w-4 h-4 rounded-full bg-teal-100 text-teal-600 flex items-center justify-center text-[10px] font-bold flex-shrink-0">✓</span>{f}</li>
              ))}
            </ul>
            <button disabled className="w-full py-2 bg-gray-100 text-gray-400 text-sm font-semibold rounded-xl cursor-default">{t('profile_btn_active')}</button>
          </div>
          <div className="bg-gradient-to-br from-teal-50 to-teal-100 border-2 border-teal-500 rounded-2xl p-5 space-y-4 relative overflow-hidden">
            <span className="absolute top-3 right-3 text-[10px] bg-teal-600 text-white px-2 py-0.5 rounded-full font-bold">{t('profile_recommended')}</span>
            <div>
              <div className="text-lg font-bold text-gray-900">Pro</div>
              <div className="text-3xl font-extrabold text-gray-900 mt-1">$12<span className="text-base font-normal text-gray-400">/mo</span></div>
              <p className="text-xs text-gray-500 mt-1">{t('profile_billing_month_note')}</p>
            </div>
            <ul className="space-y-1.5 text-sm text-gray-700">
              {[t('profile_feat_basic'), t('profile_feat_filters'), t('profile_feat_priority'), t('profile_feat_analytics')].map((f) => (
                <li key={f} className="flex items-center gap-2"><span className="w-4 h-4 rounded-full bg-teal-500 text-white flex items-center justify-center text-[10px] font-bold flex-shrink-0">✓</span>{f}</li>
              ))}
            </ul>
            <button disabled className="w-full py-2 bg-teal-600 text-white text-sm font-semibold rounded-xl cursor-default opacity-70">{t('profile_coming_soon')}</button>
          </div>
        </div>
      </div>
    </div>
  );
}
