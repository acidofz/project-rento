import { MetadataRoute } from 'next';
import { getSupabase } from '@/lib/supabase';

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://uy-click.uz';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const staticPages: MetadataRoute.Sitemap = [
    { url: BASE_URL, lastModified: new Date(), changeFrequency: 'daily', priority: 1 },
    { url: `${BASE_URL}/listings`, lastModified: new Date(), changeFrequency: 'hourly', priority: 0.9 },
    { url: `${BASE_URL}/map`, lastModified: new Date(), changeFrequency: 'daily', priority: 0.7 },
    { url: `${BASE_URL}/terms`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.3 },
    { url: `${BASE_URL}/privacy`, lastModified: new Date(), changeFrequency: 'monthly', priority: 0.3 },
  ];

  try {
    const sb = getSupabase();
    const { data } = await sb
      .from('listings')
      .select('id,created_at')
      .order('id', { ascending: false })
      .limit(1000);

    const listingPages: MetadataRoute.Sitemap = (data ?? []).map((l) => ({
      url: `${BASE_URL}/listing/${l.id}`,
      lastModified: new Date(l.created_at ?? Date.now()),
      changeFrequency: 'weekly',
      priority: 0.8,
    }));

    return [...staticPages, ...listingPages];
  } catch {
    return staticPages;
  }
}
