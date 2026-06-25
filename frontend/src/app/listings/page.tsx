import { Metadata } from 'next';
import { ListingsClient } from './ListingsClient';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://uy-click.uz';

export const metadata: Metadata = {
  title: 'Объявления аренды и продажи недвижимости в Самарканде · UY-CLICK',
  description: 'Все объявления об аренде и продаже квартир и домов в Самарканде. Фильтры по районам, цене и количеству комнат. Напрямую от владельцев без комиссий.',
  alternates: { canonical: `${SITE_URL}/listings` },
  openGraph: {
    type: 'website',
    title: 'Аренда и продажа недвижимости в Самарканде · UY-CLICK',
    description: 'Аренда и продажа квартир и домов в Самарканде без посредников и комиссий.',
    url: `${SITE_URL}/listings`,
  },
};

export default function ListingsPage() {
  return <ListingsClient />;
}
