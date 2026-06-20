'use client';

import { useState } from 'react';
import { useRequireAuth } from '@/hooks/useRequireAuth';
import { useLang } from '@/contexts/LangContext';

export default function ProfilePage() {
  const { t } = useLang();
  const auth = useRequireAuth();
  const [billing, setBilling] = useState<'month' | 'year'>('month');

  if (auth.loading) return <div className="flex items-center justify-center min-h-[50vh]"><span className="text-gray-400">...</span></div>;

  const proMonthly = 12;
  const proYearly = 9.6;

  return (
    <div className="max-w-3xl mx-auto px-4 py-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">{t('profile_title')}</h1>

      {/* User info */}
      <div className="bg-white rounded-2xl border border-gray-200 p-5 space-y-3">
        {auth.isBlocked && (
          <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-700">{t('profile_blocked_msg')}</div>
        )}
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-full bg-gradient-to-br from-teal-500 to-teal-700 flex items-center justify-center text-white font-bold text-lg">
            {auth.userName?.slice(0, 1).toUpperCase() || '?'}
          </div>
          <div>
            <div className="font-semibold text-gray-900">{auth.userName || auth.userEmail || t('profile_guest')}</div>
            <div className="text-xs text-gray-400">{t('profile_auth_label')}: {auth.isLoggedIn ? t('profile_logged_in') : t('profile_guest')}</div>
          </div>
        </div>
        {auth.userEmail && (
          <div className="flex items-center gap-2 text-sm text-gray-600 bg-gray-50 rounded-lg px-3 py-2">
            <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            {auth.userEmail}
          </div>
        )}
        <button onClick={auth.logout} className="text-sm text-red-500 hover:text-red-700 underline transition-colors">
          {t('nav_sign_out')}
        </button>
      </div>

      {/* Subscription (demo) */}
      <div className="space-y-3">
        <div className="flex items-center gap-2">
          <h2 className="font-bold text-gray-900">{t('profile_subscription_title')}</h2>
          <span className="text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full font-medium">{t('profile_demo_badge')}</span>
        </div>
        <p className="text-sm text-gray-500">{t('profile_demo_desc')}</p>

        {/* Billing toggle */}
        <div className="inline-flex items-center bg-gray-100 rounded-xl p-1">
          <button onClick={() => setBilling('month')} className={`px-4 py-1.5 text-sm font-medium rounded-lg transition-colors ${billing === 'month' ? 'bg-white shadow text-gray-900' : 'text-gray-500 hover:text-gray-700'}`}>
            {t('profile_billing_month')}
          </button>
          <button onClick={() => setBilling('year')} className={`px-4 py-1.5 text-sm font-medium rounded-lg transition-colors flex items-center gap-1.5 ${billing === 'year' ? 'bg-white shadow text-gray-900' : 'text-gray-500 hover:text-gray-700'}`}>
            {t('profile_billing_year')}
            <span className="text-[10px] bg-green-100 text-green-700 px-1.5 py-0.5 rounded-full font-bold">{t('profile_save_20')}</span>
          </button>
        </div>

        {/* Plans */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Free */}
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

          {/* Pro */}
          <div className="bg-gradient-to-br from-teal-50 to-teal-100 border-2 border-teal-500 rounded-2xl p-5 space-y-4 relative overflow-hidden">
            <span className="absolute top-3 right-3 text-[10px] bg-teal-600 text-white px-2 py-0.5 rounded-full font-bold">{t('profile_recommended')}</span>
            <div>
              <div className="text-lg font-bold text-gray-900">Pro</div>
              <div className="text-3xl font-extrabold text-gray-900 mt-1">
                ${billing === 'year' ? proYearly : proMonthly}<span className="text-base font-normal text-gray-400">/mo</span>
              </div>
              <p className="text-xs text-gray-500 mt-1">{billing === 'year' ? t('profile_billing_year_note') : t('profile_billing_month_note')}</p>
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
