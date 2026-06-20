import { NextRequest, NextResponse } from 'next/server';
import { BOT_AGENTS, SITE_URL, SITE_OG_IMAGE } from '@/lib/constants';

const LISTING_RE = /^\/listing\/(\d+)\/?$/;

function isSocialBot(ua: string): boolean {
  const lower = ua.toLowerCase();
  return BOT_AGENTS.some((b) => lower.includes(b));
}

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function buildOgHtml(listingId: string, row: Record<string, unknown>): string {
  const title = escapeHtml(String(row.title ?? '').trim());
  const district = escapeHtml(String(row.district ?? '').trim());
  const rooms = Number(row.rooms ?? 1);
  const price = Number(row.price ?? 0);
  const imageUrl = String(row.image_url ?? '').trim();

  const descParts: string[] = title ? [title] : [];
  if (district) descParts.push(`район ${district}`);
  if (rooms) descParts.push(`${rooms} комн.`);
  if (price) descParts.push(`${price.toLocaleString('ru-RU')} сум/мес`);
  descParts.push('Аренда напрямую от владельца');

  const description = escapeHtml(descParts.join(' · '));
  const ogImage = escapeHtml(imageUrl || SITE_OG_IMAGE);
  const ogUrl = escapeHtml(`${SITE_URL}/listing/${listingId}`);
  const pageTitle = escapeHtml(title ? `${title} · UY-CLICK` : 'Объявление · UY-CLICK');

  return `<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>${pageTitle}</title>
<meta name="description" content="${description}">
<meta property="og:type" content="article">
<meta property="og:url" content="${ogUrl}">
<meta property="og:title" content="${pageTitle}">
<meta property="og:description" content="${description}">
<meta property="og:image" content="${ogImage}">
<meta property="og:site_name" content="UY-CLICK">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${pageTitle}">
<meta name="twitter:description" content="${description}">
<meta name="twitter:image" content="${ogImage}">
</head>
<body></body>
</html>`;
}

export async function middleware(request: NextRequest) {
  const ua = request.headers.get('user-agent') ?? '';
  const path = request.nextUrl.pathname;
  const match = LISTING_RE.exec(path);

  if (match && isSocialBot(ua)) {
    const listingId = match[1];
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
    if (supabaseUrl && anonKey) {
      try {
        const url = `${supabaseUrl}/rest/v1/listings?id=eq.${listingId}&select=title,district,rooms,price,image_url&limit=1`;
        const res = await fetch(url, {
          headers: {
            apikey: anonKey,
            Authorization: `Bearer ${anonKey}`,
          },
        });
        const rows = await res.json() as Record<string, unknown>[];
        if (rows?.[0]) {
          return new NextResponse(buildOgHtml(listingId, rows[0]), {
            headers: { 'Content-Type': 'text/html; charset=utf-8' },
          });
        }
      } catch { /* pass through */ }
    }
  }

  return NextResponse.next();
}

export const config = { matcher: '/listing/:path*' };
