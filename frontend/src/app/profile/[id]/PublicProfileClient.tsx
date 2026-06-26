'use client';

import Link from 'next/link';
import { Listing } from '@/lib/types';
import { ListingCard } from '@/components/ListingCard';

interface Profile {
  id: string;
  firstName: string | null;
  lastName: string | null;
  username: string | null;
}

interface Props {
  profile: Profile;
  listings: Listing[];
  listingCount: number;
}

export function PublicProfileClient({ profile, listings, listingCount }: Props) {
  const displayName = [profile.firstName, profile.lastName].filter(Boolean).join(' ') || profile.username || 'Пользователь';
  const initials = displayName[0]?.toUpperCase() ?? '?';

  return (
    <div className="max-w-4xl mx-auto px-4 py-6 space-y-5">
      <Link href="/listings" className="inline-flex items-center gap-1 text-sm text-teal-700 hover:underline">
        ← Все объявления
      </Link>

      {/* Profile header */}
      <div className="bg-white rounded-2xl border border-gray-200 p-5 flex items-center gap-4">
        <div className="w-16 h-16 rounded-full bg-gradient-to-br from-teal-500 to-teal-700 flex items-center justify-center text-white font-bold text-2xl flex-shrink-0">
          {initials}
        </div>
        <div className="min-w-0 flex-1">
          <h1 className="text-xl font-bold text-gray-900">{displayName}</h1>
          {profile.username && displayName !== profile.username && (
            <div className="text-sm text-gray-400">@{profile.username}</div>
          )}
        </div>
        {/* Stats */}
        <div className="text-center flex-shrink-0">
          <div className="text-2xl font-extrabold text-teal-700">{listingCount}</div>
          <div className="text-xs text-gray-500">объявлений</div>
        </div>
      </div>

      {/* Listings */}
      <div>
        <h2 className="text-base font-semibold text-gray-800 mb-3">Объявления продавца</h2>
        {listings.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {listings.map((l) => (
              <ListingCard key={l.id} listing={l} roomsSuffix="комн." />
            ))}
          </div>
        ) : (
          <div className="py-10 text-center text-sm text-gray-400">У этого пользователя нет активных объявлений.</div>
        )}
      </div>
    </div>
  );
}
