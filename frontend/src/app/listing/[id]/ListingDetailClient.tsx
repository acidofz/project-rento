'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { useRouter } from 'next/navigation';
import { Listing } from '@/lib/types';
import { useLang } from '@/contexts/LangContext';
import { useAuth } from '@/contexts/AuthContext';
import { getAuthedClient, getSupabase } from '@/lib/supabase';
import { formatPriceUzs } from '@/lib/utils';

interface Props { listing: Listing | null }

export function ListingDetailClient({ listing }: Props) {
  const { t } = useLang();
  const { isLoggedIn, accessToken, userId } = useAuth();
  const router = useRouter();
  const [isFavorite, setIsFavorite] = useState(false);

  useEffect(() => {
    if (!isLoggedIn || !accessToken || !listing) return;
    getAuthedClient(accessToken)
      .from('favorites')
      .select('id')
      .eq('listing_id', listing.id)
      .limit(1)
      .then(({ data }) => setIsFavorite(Boolean(data?.length)));
  }, [isLoggedIn, accessToken, listing]);

  async function toggleFavorite() {
    if (!isLoggedIn || !accessToken || !listing || !userId) return;
    const sb = getAuthedClient(accessToken);
    if (isFavorite) {
      await sb.from('favorites').delete().eq('user_id', userId).eq('listing_id', listing.id);
      setIsFavorite(false);
    } else {
      await sb.from('favorites').insert({ user_id: userId, listing_id: listing.id });
      setIsFavorite(true);
    }
  }

  if (!listing) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-16 text-center space-y-4">
        <div className="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center mx-auto">
          <svg className="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
        </div>
        <h1 className="text-xl font-bold text-gray-900">{t('detail_not_found_title')}</h1>
        <p className="text-gray-500 text-sm">{t('detail_not_found_desc')}</p>
        <Link href="/listings" className="inline-block px-4 py-2 bg-teal-600 text-white text-sm rounded-xl hover:bg-teal-700 transition-colors">
          {t('detail_all_listings')}
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 space-y-4">
      <Link href="/listings" className="inline-flex items-center gap-1 text-sm text-teal-700 hover:underline">
        {t('detail_back')}
      </Link>

      <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
        {/* Image */}
        {listing.image_url ? (
          <div className="relative w-full h-[400px]">
            <Image
              src={listing.image_url}
              alt={listing.title}
              fill
              sizes="(max-width: 768px) 100vw, 672px"
              className="object-cover"
              priority
            />
          </div>
        ) : (
          <div className="w-full h-48 bg-gray-100 flex items-center justify-center">
            <span className="text-sm text-gray-400">{t('detail_no_photo')}</span>
          </div>
        )}

        <div className="p-5 space-y-4">
          {/* Title + premium */}
          <div className="flex items-start gap-2 flex-wrap">
            <h1 className="text-xl font-bold text-gray-900 leading-snug flex-1">{listing.title}</h1>
            {listing.is_premium && (
              <span className="flex-shrink-0 bg-amber-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">★ PREMIUM</span>
            )}
          </div>

          {/* District + rooms */}
          <div className="flex items-center gap-3 text-sm text-gray-600 flex-wrap">
            <span className="flex items-center gap-1">
              <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              </svg>
              {listing.district}
            </span>
            <span className="text-gray-300">·</span>
            <span>{listing.rooms} {t('detail_rooms_suffix')}</span>
          </div>

          {/* Price */}
          <div className="inline-block px-4 py-2 bg-green-50 border border-green-200 rounded-xl">
            <span className="text-xl font-bold text-green-700">{formatPriceUzs(listing.price)}</span>
          </div>

          <hr className="border-gray-100" />

          {/* Phone */}
          {listing.phone ? (
            <div className="p-3 bg-teal-50 border border-teal-200 rounded-xl flex items-center justify-between gap-3">
              <div className="flex items-center gap-2 text-sm text-teal-800">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                <span className="font-medium">{listing.phone}</span>
              </div>
              <a href={`tel:${listing.phone}`} className="px-3 py-1.5 bg-teal-600 text-white text-sm font-medium rounded-lg hover:bg-teal-700 transition-colors">
                {t('detail_phone_call')}
              </a>
            </div>
          ) : (
            <div className="p-3 bg-gray-50 border border-gray-200 rounded-xl text-sm text-gray-500">
              {t('detail_phone_none')}
            </div>
          )}

          {/* Actions */}
          <div className="flex items-center gap-3 flex-wrap">
            <button
              onClick={toggleFavorite}
              className={`flex items-center gap-1.5 px-4 py-2 border rounded-xl text-sm font-medium transition-colors ${
                isFavorite
                  ? 'bg-red-50 border-red-200 text-red-600 hover:bg-red-100'
                  : 'border-gray-200 text-gray-700 hover:bg-gray-50'
              }`}
            >
              <svg className="w-4 h-4" fill={isFavorite ? 'currentColor' : 'none'} viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
              {isFavorite ? t('detail_fav_remove') : t('detail_fav_add')}
            </button>

            {listing.latitude != null && listing.longitude != null && (
              <button
                onClick={() => router.push(`/map?focus=${listing.id}`)}
                className="flex items-center gap-1.5 px-4 py-2 border border-gray-200 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
              >
                <svg className="w-4 h-4 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                </svg>
                {t('detail_show_map')}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
