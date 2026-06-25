import { NextRequest, NextResponse } from 'next/server';
import { getServiceClient } from '@/lib/supabase-server';
import { getSupabase } from '@/lib/supabase';

export const dynamic = 'force-dynamic';

function adminIds(): Set<string> {
  const raw = process.env.ADMIN_USER_IDS ?? process.env.NEXT_PUBLIC_ADMIN_USER_IDS ?? '';
  return new Set(raw.split(',').map((s) => s.trim()).filter(Boolean));
}

async function verifyAdmin(req: NextRequest): Promise<string | null> {
  const auth = req.headers.get('authorization') ?? '';
  const token = auth.replace('Bearer ', '').trim();
  if (!token) return null;
  try {
    const { data: { user } } = await getSupabase().auth.getUser(token);
    if (!user?.id || !adminIds().has(user.id)) return null;
    return user.id;
  } catch { return null; }
}

export async function GET(req: NextRequest) {
  if (!await verifyAdmin(req)) return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
  const sb = getServiceClient();
  const [listingsRes, usersRes, latestListingsRes, latestUsersRes] = await Promise.all([
    sb.from('listings').select('id', { count: 'exact', head: true }),
    sb.from('profiles').select('id', { count: 'exact', head: true }),
    sb.from('listings').select('id,title,district,price,created_at').order('id', { ascending: false }).limit(8),
    sb.from('profiles').select('id,email,username,is_blocked,created_at').order('created_at', { ascending: false }).limit(12),
  ]);
  return NextResponse.json({
    listingCount: listingsRes.count ?? 0,
    userCount: usersRes.count ?? 0,
    recentListings: latestListingsRes.data ?? [],
    recentUsers: latestUsersRes.data ?? [],
  });
}
