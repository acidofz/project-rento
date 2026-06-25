import { Metadata } from 'next';
import { MapClient } from './MapClient';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://uy-click.uz';

export const metadata: Metadata = {
  title: 'Карта аренды жилья в Ташкенте и Узбекистане · UY-CLICK',
  description: 'Интерактивная карта объявлений об аренде квартир и домов в Ташкенте и по всему Узбекистану. Найдите жильё рядом с нужным районом.',
  alternates: { canonical: `${SITE_URL}/map` },
  openGraph: {
    type: 'website',
    title: 'Карта аренды · UY-CLICK',
    description: 'Интерактивная карта объявлений об аренде жилья в Узбекистане.',
    url: `${SITE_URL}/map`,
  },
};

export default function MapPage() {
  return <MapClient />;
}
