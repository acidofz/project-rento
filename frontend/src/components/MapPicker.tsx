'use client';

import { useEffect, useRef, useState } from 'react';
import Script from 'next/script';

interface Props {
  lat: string;
  lng: string;
  onChange: (lat: string, lng: string) => void;
}

const CENTER: [number, number] = [39.6547, 66.9758];

export function MapPicker({ lat, lng, onChange }: Props) {
  const [ymapsReady, setYmapsReady] = useState(false);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const mapRef = useRef<any>(null);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const placemarkRef = useRef<any>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const onChangeRef = useRef(onChange);
  onChangeRef.current = onChange;

  // ymaps may already be loaded from a previous page navigation
  useEffect(() => {
    if (typeof window !== 'undefined' && window.ymaps) {
      setYmapsReady(true);
    }
  }, []);

  useEffect(() => {
    if (!ymapsReady || !containerRef.current) return;

    const initLat = lat ? parseFloat(lat) : null;
    const initLng = lng ? parseFloat(lng) : null;
    const center: [number, number] = initLat && initLng ? [initLat, initLng] : CENTER;
    const zoom = initLat && initLng ? 15 : 12;

    window.ymaps.ready(() => {
      if (!containerRef.current) return;

      const map = new window.ymaps.Map(containerRef.current, {
        center,
        zoom,
        controls: ['zoomControl'],
      });
      mapRef.current = map;

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      function addOrMove(coords: [number, number]) {
        if (placemarkRef.current) {
          placemarkRef.current.geometry.setCoordinates(coords);
        } else {
          const pm = new window.ymaps.Placemark(
            coords,
            {},
            { preset: 'islands#tealDotIcon', draggable: true }
          );
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          pm.events.add('dragend', () => {
            const c = pm.geometry.getCoordinates();
            onChangeRef.current(String(c[0].toFixed(6)), String(c[1].toFixed(6)));
          });
          map.geoObjects.add(pm);
          placemarkRef.current = pm;
        }
        onChangeRef.current(String(coords[0].toFixed(6)), String(coords[1].toFixed(6)));
      }

      if (initLat && initLng) addOrMove([initLat, initLng]);

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      map.events.add('click', (e: any) => {
        addOrMove(e.get('coords'));
      });
    });

    return () => {
      if (mapRef.current) {
        try { mapRef.current.destroy(); } catch { /* ignore */ }
        mapRef.current = null;
        placemarkRef.current = null;
      }
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ymapsReady]);

  const ymapsKey = process.env.NEXT_PUBLIC_YANDEX_MAPS_KEY ?? '';

  return (
    <div className="space-y-1.5">
      <Script
        src={`https://api-maps.yandex.ru/2.1/?apikey=${ymapsKey}&lang=ru_RU`}
        onLoad={() => setYmapsReady(true)}
        strategy="afterInteractive"
      />
      <div
        ref={containerRef}
        style={{
          height: '260px',
          width: '100%',
          borderRadius: '12px',
          border: '1px solid #e5e7eb',
          overflow: 'hidden',
        }}
      />
      <p className="text-xs text-gray-400">
        {lat && lng
          ? `${lat}, ${lng} — перетащите метку или кликните по карте`
          : 'Кликните по карте, чтобы указать местоположение'}
      </p>
    </div>
  );
}
