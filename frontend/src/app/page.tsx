'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { getSupabase } from '@/lib/supabase';
import { useLang } from '@/contexts/LangContext';
import { Listing } from '@/lib/types';
import { ListingCard } from '@/components/ListingCard';
import { SkeletonCard } from '@/components/SkeletonCard';

const FEATURES = [
  {
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
      </svg>
    ),
    color: 'teal',
    titleKey: 'feat_chat_title',
    descKey: 'feat_chat_desc',
  },
  {
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
      </svg>
    ),
    color: 'rose',
    titleKey: 'feat_fav_title',
    descKey: 'feat_fav_desc',
  },
  {
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    ),
    color: 'blue',
    titleKey: 'feat_map_title',
    descKey: 'feat_map_desc',
  },
];

const COLOR_MAP: Record<string, string> = {
  teal: 'bg-teal-100 text-teal-700',
  rose: 'bg-rose-100 text-rose-600',
  blue: 'bg-blue-100 text-blue-700',
};

export default function HomePage() {
  const { t } = useLang();
  const [listings, setListings] = useState<Listing[]>([]);
  const [count, setCount] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const sb = getSupabase();
    Promise.all([
      sb.from('listings').select('id,title,district,rooms,price,owner_id,image_url,image_urls,latitude,longitude,is_premium,phone,agency,listing_type').order('id', { ascending: false }).limit(6),
      sb.from('listings').select('id', { count: 'exact', head: true }),
    ]).then(([listRes, countRes]) => {
      setListings((listRes.data as Listing[]) ?? []);
      setCount(countRes.count ?? 0);
    }).finally(() => setLoading(false));
  }, []);

  return (
    <>
      {/* Hero */}
      <section className="w-full" style={{ background: 'linear-gradient(140deg, #0f4c45 0%, #0d9488 50%, #0891b2 100%)' }}>
        <div className="max-w-6xl mx-auto px-4 py-14 md:py-20">
          <div className="max-w-xl space-y-5">
            <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium text-white/90 border border-white/20 bg-white/10 backdrop-blur-sm">
              <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
              {t('hero_badge')}
            </span>

            <h1 className="text-4xl md:text-5xl font-bold text-white leading-tight tracking-tight">
              {t('hero_title')}
              <span className="text-white/65">{t('hero_direct')}</span>
            </h1>

            <p className="text-base text-white/75 leading-relaxed">{t('hero_subtitle')}</p>

            <div className="flex flex-wrap gap-3 pt-2">
              <Link href="/listings" className="flex items-center gap-1.5 px-5 py-2.5 bg-white text-teal-800 font-bold text-sm rounded-xl shadow-md hover:shadow-lg transition-shadow">
                {t('hero_btn_view')}
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </Link>
              <Link href="/create" className="flex items-center gap-1.5 px-5 py-2.5 border border-white/40 text-white font-semibold text-sm rounded-xl hover:bg-white/10 transition-colors">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                {t('hero_btn_post')}
              </Link>
            </div>

            <div className="flex items-center gap-6 flex-wrap pt-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-white">{count}+</div>
                <div className="text-xs text-white/60 tracking-wide">{t('stat_listings')}</div>
              </div>
              <div className="w-px h-8 bg-white/20" />
              <div className="text-center">
                <div className="text-2xl font-bold text-white">0%</div>
                <div className="text-xs text-white/60 tracking-wide">{t('stat_commission')}</div>
              </div>
              <div className="w-px h-8 bg-white/20" />
              <div className="text-center">
                <div className="text-2xl font-bold text-white">P2P</div>
                <div className="text-xs text-white/60 tracking-wide">{t('stat_chat')}</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features row */}
      <section className="w-full border-t border-b border-gray-200 bg-white py-8">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
            {FEATURES.map(({ icon, color, titleKey, descKey }) => (
              <div key={titleKey} className="flex items-start gap-3">
                <div className={`flex-shrink-0 w-9 h-9 rounded-xl flex items-center justify-center ${COLOR_MAP[color]}`}>
                  {icon}
                </div>
                <div>
                  <div className="font-bold text-sm text-gray-900">{t(titleKey)}</div>
                  <div className="text-xs text-gray-500 leading-relaxed mt-0.5">{t(descKey)}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Recent listings */}
      <section className="w-full bg-gray-50 py-8">
        <div className="max-w-6xl mx-auto px-4 space-y-5">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-gray-900">{t('section_recent')}</h2>
              <p className="text-sm text-gray-500 mt-0.5">{t('listings_count_suffix')}</p>
            </div>
            <Link href="/listings" className="flex items-center gap-1 text-sm text-teal-700 font-semibold hover:underline">
              {t('section_all')}
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </Link>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)}
            </div>
          ) : listings.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {listings.map((l) => <ListingCard key={l.id} listing={l} roomsSuffix={t('rooms_suffix')} />)}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-14 space-y-3">
              <div className="w-14 h-14 rounded-full bg-teal-50 flex items-center justify-center">
                <svg className="w-7 h-7 text-teal-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
              </div>
              <p className="text-gray-500 text-sm font-medium">{t('home_empty')}</p>
              <Link href="/create" className="flex items-center gap-1 px-3 py-1.5 bg-teal-600 text-white text-sm rounded-lg hover:bg-teal-700 transition-colors">
                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                {t('nav_post')}
              </Link>
            </div>
          )}
        </div>
      </section>
    </>
  );
}
