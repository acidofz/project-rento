import Link from 'next/link';
import Image from 'next/image';
import { Listing } from '@/lib/types';
import { formatPriceUzs } from '@/lib/utils';

interface ListingCardProps {
  listing: Listing;
  isFavorite?: boolean;
  onToggleFavorite?: (id: number) => void;
  roomsSuffix?: string;
}

export function ListingCard({ listing, isFavorite, onToggleFavorite, roomsSuffix = 'комн.' }: ListingCardProps) {
  return (
    <div
      className={[
        'rounded-xl border bg-white overflow-hidden shadow-sm',
        'transition-all duration-200 hover:-translate-y-1 hover:shadow-lg',
        listing.is_premium ? 'border-amber-300/60' : 'border-gray-100',
      ].join(' ')}
    >
      {/* Image area */}
      <div className="relative h-[200px] bg-gray-100 overflow-hidden">
        {listing.image_url ? (
          <Image
            src={listing.image_url}
            alt={listing.title}
            fill
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
            className="object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <svg className="w-10 h-10 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        )}
        {listing.is_premium && (
          <span className="absolute top-2 left-2 bg-amber-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full flex items-center gap-1">
            ★ PREMIUM
          </span>
        )}
      </div>

      {/* Content */}
      <div className="p-3 space-y-1.5">
        <Link
          href={`/listing/${listing.id}`}
          className="block font-bold text-sm text-gray-900 leading-snug hover:text-teal-700 transition-colors line-clamp-2"
        >
          {listing.title}
        </Link>

        <div className="flex items-center gap-1 text-xs text-gray-500 flex-wrap">
          <svg className="w-3 h-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span>{listing.district}</span>
          <span className="text-gray-300">·</span>
          <svg className="w-3 h-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          <span>{listing.rooms} {roomsSuffix}</span>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="font-bold text-base text-green-700">{formatPriceUzs(listing.price)}</span>
            <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded-full ${listing.listing_type === 'sale' ? 'bg-blue-100 text-blue-700' : 'bg-teal-100 text-teal-700'}`}>
              {listing.listing_type === 'sale' ? 'Продажа' : 'Аренда'}
            </span>
          </div>
          <div className="flex items-center gap-1">
            {listing.phone && (
              <a
                href={`tel:${listing.phone}`}
                className="flex items-center gap-1 text-xs text-teal-700 font-medium hover:underline"
                onClick={(e) => e.stopPropagation()}
              >
                <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
                {listing.phone}
              </a>
            )}
            {onToggleFavorite && (
              <button
                onClick={() => onToggleFavorite(listing.id)}
                className={`ml-1 p-1 rounded-lg transition-colors ${isFavorite ? 'text-red-500 hover:text-red-600' : 'text-gray-300 hover:text-red-400'}`}
                title={isFavorite ? 'Убрать из избранного' : 'В избранное'}
              >
                <svg className="w-4 h-4" fill={isFavorite ? 'currentColor' : 'none'} viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
