import { Metadata } from 'next';
import { MapClient } from './MapClient';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://uy-click.uz';

export const metadata: Metadata = {
  title: 'Карта недвижимости в Самарканде · UY-CLICK',
  description: 'Интерактивная карта объявлений об аренде и продаже квартир и домов в Самарканде. Найдите объект рядом с нужным районом.',
  alternates: { canonical: `${SITE_URL}/map` },
  openGraph: {
    type: 'website',
    title: 'Карта недвижимости · UY-CLICK',
    description: 'Интерактивная карта объявлений об аренде и продаже недвижимости в Самарканде.',
    url: `${SITE_URL}/map`,
  },
};

export default function MapPage() {
  return <MapClient />;
}
