'use client';

import { useEffect, useState, useMemo } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { getSupabase, getAuthedClient } from '@/lib/supabase';
import { useLang } from '@/contexts/LangContext';
import { useAuth } from '@/contexts/AuthContext';
import { Listing } from '@/lib/types';
import { ListingCard } from '@/components/ListingCard';
import { SkeletonCard } from '@/components/SkeletonCard';
import { Pagination } from '@/components/Pagination';

const PAGE_SIZE = 12;

type SortKey = 'newest' | 'price_asc' | 'price_desc' | 'rooms_desc';

function sortListings(items: Listing[], sortBy: SortKey): Listing[] {
  const sorted = [...items];
  sorted.sort((a, b) => {
    // Premium always first
    if (a.is_premium !== b.is_premium) return b.is_premium ? 1 : -1;
    if (sortBy === 'price_asc') return a.price - b.price || b.id - a.id;
    if (sortBy === 'price_desc') return b.price - a.price || b.id - a.id;
    if (sortBy === 'rooms_desc') return b.rooms - a.rooms || b.id - a.id;
    return b.id - a.id; // newest
  });
  return sorted;
}

export default function ListingsPage() {
  const { t } = useLang();
  const { isLoggedIn, accessToken, userId } = useAuth();
  const router = useRouter();

  const [allListings, setAllListings] = useState<Listing[]>([]);
  const [favoriteIds, setFavoriteIds] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [search, setSearch] = useState('');
  const [district, setDistrict] = useState('');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [minRooms, setMinRooms] = useState('');
  const [maxRooms, setMaxRooms] = useState('');
  const [sortBy, setSortBy] = useState<SortKey>('newest');
  const [page, setPage] = useState(1);

  useEffect(() => {
    const sb = getSupabase();
    Promise.all([
      sb.from('listings').select('id,title,district,rooms,price,owner_id,image_url,latitude,longitude,is_premium,phone').order('id', { ascending: false }),
      isLoggedIn && accessToken
        ? getAuthedClient(accessToken).from('favorites').select('listing_id')
        : Promise.resolve({ data: [] }),
    ]).then(([listRes, favRes]) => {
      if (listRes.error) setError('Не удалось загрузить объявления.');
      setAllListings((listRes.data as Listing[]) ?? []);
      setFavoriteIds(((favRes.data ?? []) as { listing_id: number }[]).map((r) => r.listing_id));
    }).finally(() => setLoading(false));
  }, [isLoggedIn, accessToken]);

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    const d = district.trim().toLowerCase();
    const minP = Number(minPrice) || 0;
    const maxP = Number(maxPrice) || 0;
    const minR = Number(minRooms) || 0;
    const maxR = Number(maxRooms) || 0;
    return allListings.filter((l) => {
      if (q && !l.title.toLowerCase().includes(q) && !l.district.toLowerCase().includes(q)) return false;
      if (d && !l.district.toLowerCase().includes(d)) return false;
      if (minP > 0 && l.price < minP) return false;
      if (maxP > 0 && l.price > maxP) return false;
      if (minR > 0 && l.rooms < minR) return false;
      if (maxR > 0 && l.rooms > maxR) return false;
      return true;
    });
  }, [allListings, search, district, minPrice, maxPrice, minRooms, maxRooms]);

  const sorted = useMemo(() => sortListings(filtered, sortBy), [filtered, sortBy]);
  const totalPages = Math.max(1, Math.ceil(sorted.length / PAGE_SIZE));
  const paginated = sorted.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  function resetFilters() {
    setSearch(''); setDistrict(''); setMinPrice(''); setMaxPrice('');
    setMinRooms(''); setMaxRooms(''); setSortBy('newest'); setPage(1);
  }

  function changeFilter(fn: () => void) { fn(); setPage(1); }

  async function toggleFavorite(id: number) {
    if (!isLoggedIn || !accessToken || !userId) return;
    const sb = getAuthedClient(accessToken);
    if (favoriteIds.includes(id)) {
      await sb.from('favorites').delete().eq('user_id', userId).eq('listing_id', id);
      setFavoriteIds((prev) => prev.filter((x) => x !== id));
    } else {
      await sb.from('favorites').insert({ user_id: userId, listing_id: id });
      setFavoriteIds((prev) => [...prev, id]);
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 space-y-5">
      {/* Header */}
      <div className="flex flex-wrap items-center gap-3">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{t('listings_title')}</h1>
          <p className="text-sm text-gray-500">{sorted.length} {t('listings_count_suffix')}</p>
        </div>
        <div className="flex-1" />
        <Link href="/map" className="flex items-center gap-1.5 px-3 py-1.5 border border-gray-200 rounded-lg text-sm text-gray-700 hover:bg-gray-50 transition-colors">
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
          </svg>
          {t('btn_map')}
        </Link>
        <select
          value={sortBy}
          onChange={(e) => changeFilter(() => setSortBy(e.target.value as SortKey))}
          className="px-3 py-1.5 border border-gray-200 rounded-lg text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-teal-500"
        >
          <option value="newest">{t('sort_newest')}</option>
          <option value="price_asc">{t('sort_price_asc')}</option>
          <option value="price_desc">{t('sort_price_desc')}</option>
          <option value="rooms_desc">{t('sort_rooms_desc')}</option>
        </select>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl border border-gray-200 p-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          <div>
            <label className="text-xs font-medium text-gray-500 block mb-1">{t('filter_search_label')}</label>
            <input type="text" value={search} onChange={(e) => changeFilter(() => setSearch(e.target.value))} placeholder={t('filter_search_ph')} className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
          </div>
          <div>
            <label className="text-xs font-medium text-gray-500 block mb-1">{t('filter_district_label')}</label>
            <input type="text" value={district} onChange={(e) => changeFilter(() => setDistrict(e.target.value))} placeholder={t('filter_district_ph')} className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
          </div>
          <div>
            <label className="text-xs font-medium text-gray-500 block mb-1">{t('filter_price_label')}</label>
            <div className="flex gap-2">
              <input type="number" value={minPrice} onChange={(e) => changeFilter(() => setMinPrice(e.target.value))} placeholder={t('filter_from')} className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
              <input type="number" value={maxPrice} onChange={(e) => changeFilter(() => setMaxPrice(e.target.value))} placeholder={t('filter_to')} className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
            </div>
          </div>
          <div>
            <label className="text-xs font-medium text-gray-500 block mb-1">{t('filter_rooms_label')}</label>
            <div className="flex gap-2">
              <input type="number" value={minRooms} onChange={(e) => changeFilter(() => setMinRooms(e.target.value))} placeholder={t('filter_from')} className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
              <input type="number" value={maxRooms} onChange={(e) => changeFilter(() => setMaxRooms(e.target.value))} placeholder={t('filter_to')} className="w-full px-3 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
            </div>
          </div>
        </div>
        <button onClick={resetFilters} className="mt-3 text-xs text-gray-500 hover:text-gray-700 transition-colors underline">
          {t('btn_reset')}
        </button>
      </div>

      {error && <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-700">{error}</div>}

      {/* Listings grid */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => <SkeletonCard key={i} />)}
        </div>
      ) : paginated.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {paginated.map((l) => (
            <ListingCard
              key={l.id}
              listing={l}
              isFavorite={favoriteIds.includes(l.id)}
              onToggleFavorite={isLoggedIn ? toggleFavorite : undefined}
              roomsSuffix={t('rooms_suffix')}
            />
          ))}
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center py-14 space-y-3">
          <svg className="w-10 h-10 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <p className="font-medium text-gray-700">{t('no_results_title')}</p>
          <p className="text-sm text-gray-500">{t('no_results_subtitle')}</p>
          <button onClick={resetFilters} className="px-3 py-1.5 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">{t('btn_reset')}</button>
        </div>
      )}

      <Pagination page={page} totalPages={totalPages} onPrev={() => setPage((p) => p - 1)} onNext={() => setPage((p) => p + 1)} label={t('page_label')} ofLabel={t('page_of')} />
    </div>
  );
}
