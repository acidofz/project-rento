import { Metadata } from 'next';
import { getSupabase } from '@/lib/supabase';
import { Listing } from '@/lib/types';
import { ListingDetailClient } from './ListingDetailClient';

interface Props { params: { id: string } }

async function fetchListing(id: string): Promise<Listing | null> {
  if (!/^\d+$/.test(id)) return null;
  try {
    const sb = getSupabase();
    const { data } = await sb
      .from('listings')
      .select('id,title,district,rooms,price,owner_id,image_url,latitude,longitude,is_premium,phone')
      .eq('id', Number(id))
      .limit(1)
      .single();
    return (data as Listing) ?? null;
  } catch { return null; }
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const listing = await fetchListing(params.id);
  if (!listing) return { title: 'Объявление не найдено · UY-CLICK' };

  const parts: string[] = [listing.title];
  if (listing.district) parts.push(`район ${listing.district}`);
  if (listing.rooms) parts.push(`${listing.rooms} комн.`);
  if (listing.price) parts.push(`${listing.price.toLocaleString('ru-RU')} сум/мес`);
  parts.push('Аренда напрямую от владельца');
  const description = parts.join(' · ');

  return {
    title: `${listing.title} · UY-CLICK`,
    description,
    openGraph: {
      type: 'article',
      title: `${listing.title} · UY-CLICK`,
      description,
      images: listing.image_url ? [listing.image_url] : [],
    },
  };
}

export default async function ListingDetailPage({ params }: Props) {
  const listing = await fetchListing(params.id);

  const jsonLd = listing
    ? {
        '@context': 'https://schema.org',
        '@type': 'RealEstateListing',
        name: listing.title,
        description: [
          listing.district && `Район: ${listing.district}`,
          listing.rooms && `Комнат: ${listing.rooms}`,
          listing.price && `Цена: ${listing.price.toLocaleString('ru-RU')} сум/мес`,
        ]
          .filter(Boolean)
          .join('. '),
        url: `${process.env.NEXT_PUBLIC_SITE_URL ?? 'https://uy-click.uz'}/listing/${listing.id}`,
        image: listing.image_url ?? undefined,
        offers: {
          '@type': 'Offer',
          price: listing.price,
          priceCurrency: 'UZS',
          availability: 'https://schema.org/InStock',
        },
        address: {
          '@type': 'PostalAddress',
          addressLocality: listing.district ?? 'Ташкент',
          addressCountry: 'UZ',
        },
      }
    : null;

  return (
    <>
      {jsonLd && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      )}
      <ListingDetailClient listing={listing} />
    </>
  );
}
