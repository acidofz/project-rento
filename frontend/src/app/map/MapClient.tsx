'use client';

import { useEffect, useRef, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import Script from 'next/script';
import { getSupabase } from '@/lib/supabase';
import { useLang } from '@/contexts/LangContext';
import { Listing } from '@/lib/types';
import { formatPriceUzs } from '@/lib/utils';
import { Suspense } from 'react';

function MapInner() {
  const { t } = useLang();
  const searchParams = useSearchParams();
  const focusId = Number(searchParams.get('focus') ?? 0);
  const [error, setError] = useState('');
  const markersRef = useRef<object[]>([]);
  const readyRef = useRef({ ymaps: false, mapScript: false, data: false });
  const initializedRef = useRef(false);
  const ymapsKey = process.env.NEXT_PUBLIC_YANDEX_MAPS_KEY ?? '';

  function tryInit() {
    if (initializedRef.current) return;
    if (!readyRef.current.ymaps || !readyRef.current.mapScript || !readyRef.current.data) return;
    initializedRef.current = true;
    if (typeof window.__uyClickInitMap === 'function') {
      window.__uyClickInitMap(markersRef.current as never, focusId);
    }
  }

  useEffect(() => {
    // ymaps may already be loaded
    if (typeof window !== 'undefined' && window.ymaps) {
      readyRef.current.ymaps = true;
      tryInit();
    }

    getSupabase()
      .from('listings')
      .select('id,title,district,rooms,price,image_url,latitude,longitude,phone')
      .not('latitude', 'is', null)
      .not('longitude', 'is', null)
      .then(({ data, error: err }) => {
        if (err) { setError('Не удалось загрузить объявления.'); return; }
        markersRef.current = ((data as Listing[]) ?? []).map((l) => ({
          id: l.id,
          lat: l.latitude,
          lng: l.longitude,
          title: l.title,
          price: formatPriceUzs(l.price),
          url: `/listing/${l.id}`,
          image_url: l.image_url || '',
        }));
        readyRef.current.data = true;
        tryInit();
      });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 space-y-4">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">{t('map_title')}</h1>
        <p className="text-sm text-gray-500 mt-1">{t('map_description')}</p>
      </div>

      {error && <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-700">{error}</div>}

      <div
        id="uy-click-map"
        style={{ height: '70vh', width: '100%', borderRadius: '12px', overflow: 'hidden', border: '1px solid #e5e7eb' }}
      />

      <Script
        src={`https://api-maps.yandex.ru/2.1/?apikey=${ymapsKey}&lang=ru_RU`}
        strategy="afterInteractive"
        onLoad={() => { readyRef.current.ymaps = true; tryInit(); }}
      />
      <Script
        src="/uy_click_map.js"
        strategy="afterInteractive"
        onLoad={() => { readyRef.current.mapScript = true; tryInit(); }}
      />
    </div>
  );
}

export function MapClient() {
  return (
    <Suspense>
      <MapInner />
    </Suspense>
  );
}
