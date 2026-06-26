import { Metadata } from 'next';
import { getServiceClient } from '@/lib/supabase-server';
import { getSupabase } from '@/lib/supabase';
import { Listing } from '@/lib/types';
import { PublicProfileClient } from './PublicProfileClient';

interface Props { params: { id: string } }

function isValidUuid(s: string) {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(s);
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  if (!isValidUuid(params.id)) return { title: 'Профиль не найден' };
  const sb = getServiceClient();
  const { data } = await sb.from('profiles').select('first_name,last_name,username').eq('id', params.id).limit(1).single();
  const name = data ? [data.first_name, data.last_name].filter(Boolean).join(' ') || data.username || 'Пользователь' : 'Пользователь';
  return { title: `${name} — профиль на UY-CLICK`, description: `Объявления пользователя ${name} на UY-CLICK Samarkand` };
}

export default async function PublicProfilePage({ params }: Props) {
  if (!isValidUuid(params.id)) return <NotFound />;

  const sb = getServiceClient();
  const anon = getSupabase();

  const [profileRes, listingsRes, countRes] = await Promise.all([
    sb.from('profiles').select('id,first_name,last_name,username').eq('id', params.id).limit(1).single(),
    anon.from('listings').select('id,title,district,rooms,price,owner_id,image_url,image_urls,latitude,longitude,is_premium,phone,agency,listing_type').eq('owner_id', params.id).order('id', { ascending: false }).limit(20),
    anon.from('listings').select('id', { count: 'exact', head: true }).eq('owner_id', params.id),
  ]);

  if (!profileRes.data) return <NotFound />;

  const profile = {
    id: profileRes.data.id as string,
    firstName: (profileRes.data.first_name as string | null) ?? null,
    lastName: (profileRes.data.last_name as string | null) ?? null,
    username: (profileRes.data.username as string | null) ?? null,
  };

  return (
    <PublicProfileClient
      profile={profile}
      listings={(listingsRes.data as Listing[]) ?? []}
      listingCount={countRes.count ?? 0}
    />
  );
}

function NotFound() {
  return (
    <div className="max-w-xl mx-auto px-4 py-16 text-center space-y-3">
      <div className="w-14 h-14 rounded-full bg-gray-100 flex items-center justify-center mx-auto">
        <svg className="w-7 h-7 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
      </div>
      <h1 className="text-xl font-bold text-gray-900">Профиль не найден</h1>
      <p className="text-sm text-gray-500">Пользователь не существует или был удалён.</p>
    </div>
  );
}
