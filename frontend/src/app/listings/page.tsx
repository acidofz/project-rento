import { Metadata } from 'next';
import { ListingsClient } from './ListingsClient';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://uy-click.uz';

export const metadata: Metadata = {
  title: 'Объявления об аренде жилья в Узбекистане · UY-CLICK',
  description: 'Все объявления об аренде квартир и домов в Ташкенте и Узбекистане. Фильтры по районам, цене и количеству комнат. Аренда напрямую от владельцев без комиссий.',
  alternates: { canonical: `${SITE_URL}/listings` },
  openGraph: {
    type: 'website',
    title: 'Объявления об аренде · UY-CLICK',
    description: 'Аренда квартир и домов по всему Узбекистану без посредников и комиссий.',
    url: `${SITE_URL}/listings`,
  },
};

export default function ListingsPage() {
  return <ListingsClient />;
}
