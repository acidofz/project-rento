'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRequireAuth } from '@/hooks/useRequireAuth';
import { useLang } from '@/contexts/LangContext';
import { getAuthedClient } from '@/lib/supabase';
import { Listing } from '@/lib/types';
import { ListingCard } from '@/components/ListingCard';

export default function FavoritesPage() {
  const { t } = useLang();
  const auth = useRequireAuth();
  const [listings, setListings] = useState<Listing[]>([]);
  const [favoriteIds, setFavoriteIds] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  async function load() {
    if (!auth.isLoggedIn || !auth.accessToken || !auth.userId) return;
    setLoading(true);
    const sb = getAuthedClient(auth.accessToken);
    const { data: favRows, error: favErr } = await sb.from('favorites').select('listing_id').eq('user_id', auth.userId);
    if (favErr) { setError('Не удалось загрузить избранное.'); setLoading(false); return; }
    const ids = (favRows ?? []).map((r: { listing_id: number }) => r.listing_id);
    setFavoriteIds(ids);
    if (!ids.length) { setListings([]); setLoading(false); return; }
    const { data, error: listErr } = await sb.from('listings').select('id,title,district,rooms,price,owner_id,image_url,image_urls,latitude,longitude,is_premium,phone,agency,listing_type').in('id', ids).order('id', { ascending: false });
    if (listErr) { setError('Не удалось загрузить объявления.'); } else { setListings((data as Listing[]) ?? []); }
    setLoading(false);
  }

  useEffect(() => { if (!auth.loading) load(); }, [auth.loading, auth.isLoggedIn, auth.accessToken]); // eslint-disable-line react-hooks/exhaustive-deps

  async function toggleFavorite(id: number) {
    if (!auth.accessToken || !auth.userId) return;
    const sb = getAuthedClient(auth.accessToken);
    await sb.from('favorites').delete().eq('user_id', auth.userId).eq('listing_id', id);
    setFavoriteIds((prev) => prev.filter((x) => x !== id));
    setListings((prev) => prev.filter((l) => l.id !== id));
  }

  if (auth.loading) return <div className="flex items-center justify-center min-h-[50vh]"><span className="text-gray-400">...</span></div>;

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 space-y-5">
      <div className="flex items-center gap-3">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{t('favorites_title')}</h1>
          <p className="text-sm text-gray-500 mt-0.5">{t('favorites_subtitle')}</p>
        </div>
        <div className="flex-1" />
        <button onClick={load} className="px-3 py-1.5 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">{t('favorites_refresh')}</button>
      </div>

      {error && <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-700">{error}</div>}

      {loading ? (
        <div className="text-center py-10 text-gray-400 text-sm">...</div>
      ) : listings.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {listings.map((l) => (
            <div key={l.id} className="space-y-2">
              <ListingCard listing={l} isFavorite={favoriteIds.includes(l.id)} onToggleFavorite={toggleFavorite} roomsSuffix={t('rooms_suffix')} />
            </div>
          ))}
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center py-14 space-y-3">
          <svg className="w-10 h-10 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
          <p className="text-gray-500 text-sm">{t('favorites_empty')}</p>
          <Link href="/listings" className="px-3 py-1.5 bg-teal-600 text-white text-sm rounded-lg hover:bg-teal-700 transition-colors">{t('favorites_go_listings')}</Link>
        </div>
      )}
    </div>
  );
}
