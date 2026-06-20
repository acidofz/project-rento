'use client';

import Link from 'next/link';
import { useLang } from '@/contexts/LangContext';

export function Footer() {
  const { t } = useLang();
  return (
    <footer className="border-t border-gray-200 bg-gray-50 py-4 mt-auto">
      <div className="max-w-6xl mx-auto px-4 flex flex-wrap items-center justify-between gap-3 text-sm text-gray-500">
        <div className="flex items-center gap-4 flex-wrap">
          <Link href="/terms" className="hover:text-teal-700 transition-colors">{t('footer_terms')}</Link>
          <Link href="/privacy" className="hover:text-teal-700 transition-colors">{t('footer_privacy')}</Link>
          <Link href="/monetization" className="hover:text-teal-700 transition-colors">{t('footer_biz')}</Link>
        </div>
        <span>© {new Date().getFullYear()} UY-CLICK</span>
      </div>
    </footer>
  );
}
