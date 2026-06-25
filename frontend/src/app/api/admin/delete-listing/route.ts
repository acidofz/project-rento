import { NextRequest, NextResponse } from 'next/server';
import { getServiceClient } from '@/lib/supabase-server';
import { getSupabase } from '@/lib/supabase';

export const dynamic = 'force-dynamic';

function adminIds(): Set<string> {
  const raw = process.env.ADMIN_USER_IDS ?? process.env.NEXT_PUBLIC_ADMIN_USER_IDS ?? '';
  return new Set(raw.split(',').map((s) => s.trim()).filter(Boolean));
}

async function verifyAdmin(req: NextRequest): Promise<boolean> {
  const token = (req.headers.get('authorization') ?? '').replace('Bearer ', '').trim();
  if (!token) return false;
  try {
    const { data: { user } } = await getSupabase().auth.getUser(token);
    return Boolean(user?.id && adminIds().has(user.id));
  } catch { return false; }
}

export async function POST(req: NextRequest) {
  if (!await verifyAdmin(req)) return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
  let listing_id: number;
  try { ({ listing_id } = await req.json() as { listing_id: number }); } catch { return NextResponse.json({ error: 'Invalid request body' }, { status: 400 }); }
  if (!listing_id) return NextResponse.json({ error: 'Missing listing_id' }, { status: 400 });
  const { error } = await getServiceClient().from('listings').delete().eq('id', listing_id);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ ok: true });
}
