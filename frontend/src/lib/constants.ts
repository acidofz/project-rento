export const LISTINGS_PAGE_SIZE = 12;
export const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://uy-click.uz';
export const SITE_OG_IMAGE = `${SITE_URL}/icon.svg`;
export const LISTING_IMAGES_BUCKET = 'listing-images';

export const BOT_AGENTS = [
  'facebookexternalhit',
  'whatsapp',
  'telegrambot',
  'twitterbot',
  'linkedinbot',
  'slackbot',
  'discordbot',
  'vkshare',
  'okhttp',
];

export const UZ_BOUNDS = {
  lat: { min: 37.0, max: 45.6 },
  lng: { min: 56.0, max: 73.2 },
};

export const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
export const MAX_IMAGE_SIZE = 5_000_000; // 5MB
