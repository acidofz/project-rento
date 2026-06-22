import { NextRequest, NextResponse } from 'next/server';
import { getServiceClient } from '@/lib/supabase-server';
import { getSupabase } from '@/lib/supabase';

export const dynamic = 'force-dynamic';

function adminIds(): Set<string> {
  return new Set((process.env.ADMIN_USER_IDS ?? '').split(',').map((s) => s.trim()).filter(Boolean));
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
  const { user_id, blocked } = await req.json() as { user_id: string; blocked: boolean };
  if (!user_id || typeof blocked !== 'boolean') return NextResponse.json({ error: 'Missing fields' }, { status: 400 });
  const { error } = await getServiceClient().from('profiles').update({ is_blocked: blocked }).eq('id', user_id);
  if (error) return NextResponse.json({ error: error.message }, { status: 500 });
  return NextResponse.json({ ok: true });
}
