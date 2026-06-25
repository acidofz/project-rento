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

export const SAMARKAND_CENTER: [number, number] = [39.6547, 66.9758];
export const SAMARKAND_BOUNDS = {
  lat: { min: 39.3, max: 39.9 },
  lng: { min: 66.6, max: 67.3 },
};

export const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
export const MAX_IMAGE_SIZE = 5_000_000; // 5MB
