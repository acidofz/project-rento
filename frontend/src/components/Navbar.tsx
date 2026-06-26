'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { useLang } from '@/contexts/LangContext';
import { Lang } from '@/lib/i18n';

const NAV_LINKS = [
  { key: 'nav_listings', href: '/listings' },
  { key: 'nav_map', href: '/map' },
  { key: 'nav_favorites', href: '/favorites' },
  { key: 'nav_my_listings', href: '/my-listings' },
];

const LANGS: Lang[] = ['uz', 'ru', 'en'];

export function Navbar() {
  const { isLoggedIn, userName, isBlocked, logout } = useAuth();
  const { lang, setLang, t } = useLang();
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 bg-white/95 backdrop-blur-sm border-b border-gray-200">
      <div className="max-w-6xl mx-auto px-4 h-14 flex items-center gap-3">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 font-bold text-gray-900 text-lg mr-2 flex-shrink-0" onClick={() => setMenuOpen(false)}>
          <span className="w-7 h-7 rounded-lg bg-gradient-to-br from-teal-600 to-teal-700 flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
          </span>
          UY-CLICK
        </Link>

        {/* Desktop nav */}
        <div className="hidden lg:flex items-center gap-1 flex-1">
          {NAV_LINKS.map(({ key, href }) => (
            <Link key={href} href={href} className="px-3 py-1.5 rounded-lg text-sm text-gray-600 hover:text-teal-700 hover:bg-teal-50 transition-colors">
              {t(key)}
            </Link>
          ))}
        </div>

        <div className="flex-1 lg:flex-none" />

        {/* Lang switcher */}
        <div className="hidden sm:flex items-center gap-0.5">
          {LANGS.map((l) => (
            <button
              key={l}
              onClick={() => setLang(l)}
              className={`px-2 py-1 rounded text-xs font-semibold uppercase transition-colors ${
                lang === l ? 'bg-teal-600 text-white' : 'text-gray-500 hover:bg-gray-100'
              }`}
            >
              {l}
            </button>
          ))}
        </div>

        {/* Post button */}
        <Link
          href="/create"
          className="hidden sm:flex items-center gap-1 px-3 py-1.5 bg-teal-600 text-white text-sm font-semibold rounded-lg hover:bg-teal-700 transition-colors flex-shrink-0"
        >
          <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          {t('nav_post')}
        </Link>

        {/* Auth */}
        <div className="hidden lg:flex items-center gap-2">
          {isLoggedIn ? (
            <>
              <Link
                href="/profile"
                className={`flex items-center gap-2 px-2.5 py-1.5 rounded-xl transition-colors ${isBlocked ? 'text-red-600 bg-red-50 hover:bg-red-100' : 'text-gray-700 hover:bg-gray-100'}`}
                title="Профиль"
              >
                <span className="w-7 h-7 rounded-full bg-gradient-to-br from-teal-500 to-teal-700 flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
                  {isBlocked ? '⛔' : userName?.slice(0, 1).toUpperCase() || '?'}
                </span>
                <span className="text-sm font-medium max-w-[120px] truncate">{isBlocked ? t('nav_blocked') : userName}</span>
              </Link>
              <button onClick={() => logout()} className="text-sm text-gray-400 hover:text-gray-600 transition-colors px-2 py-1">
                {t('nav_sign_out')}
              </button>
            </>
          ) : (
            <Link href="/login" className="text-sm text-teal-700 font-medium hover:underline">
              {t('nav_sign_in')}
            </Link>
          )}
        </div>

        {/* Hamburger */}
        <button
          className="lg:hidden p-1.5 rounded-lg text-gray-500 hover:bg-gray-100 transition-colors"
          onClick={() => setMenuOpen((o) => !o)}
          aria-label={t('nav_menu')}
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            {menuOpen
              ? <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              : <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            }
          </svg>
        </button>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <div className="lg:hidden border-t border-gray-200 bg-white px-4 py-3 space-y-2">
          <Link href="/create" className="flex items-center gap-1.5 w-full px-3 py-2 bg-teal-600 text-white text-sm font-semibold rounded-lg" onClick={() => setMenuOpen(false)}>
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            {t('nav_post')}
          </Link>
          {NAV_LINKS.map(({ key, href }) => (
            <Link key={href} href={href} className="block px-3 py-2 text-sm text-gray-700 rounded-lg hover:bg-gray-50" onClick={() => setMenuOpen(false)}>
              {t(key)}
            </Link>
          ))}
          <div className="flex gap-1 pt-1">
            {LANGS.map((l) => (
              <button key={l} onClick={() => { setLang(l); setMenuOpen(false); }} className={`px-3 py-1.5 rounded text-xs font-semibold uppercase transition-colors ${lang === l ? 'bg-teal-600 text-white' : 'text-gray-500 hover:bg-gray-100'}`}>
                {l}
              </button>
            ))}
          </div>
          <div className="pt-1 border-t border-gray-100">
            {isLoggedIn ? (
              <div className="flex items-center justify-between">
                <Link href="/profile" className="flex items-center gap-2 px-2 py-2" onClick={() => setMenuOpen(false)}>
                  <span className="w-7 h-7 rounded-full bg-gradient-to-br from-teal-500 to-teal-700 flex items-center justify-center text-white text-xs font-bold flex-shrink-0">
                    {isBlocked ? '⛔' : userName?.slice(0, 1).toUpperCase() || '?'}
                  </span>
                  <span className={`text-sm font-medium ${isBlocked ? 'text-red-600' : 'text-gray-700'}`}>{isBlocked ? t('nav_blocked') : userName}</span>
                </Link>
                <button onClick={() => { logout(); setMenuOpen(false); }} className="text-sm text-gray-500 px-3 py-2 hover:text-gray-700">
                  {t('nav_sign_out')}
                </button>
              </div>
            ) : (
              <div className="flex gap-2">
                <Link href="/login" className="flex-1 text-center px-3 py-2 border border-teal-600 text-teal-700 text-sm font-medium rounded-lg hover:bg-teal-50" onClick={() => setMenuOpen(false)}>
                  {t('nav_sign_in')}
                </Link>
                <Link href="/register" className="flex-1 text-center px-3 py-2 bg-teal-600 text-white text-sm font-medium rounded-lg hover:bg-teal-700" onClick={() => setMenuOpen(false)}>
                  {t('nav_register')}
                </Link>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
