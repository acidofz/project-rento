import { NextResponse } from 'next/server';
import { getSupabase } from '@/lib/supabase';

export const dynamic = 'force-dynamic';

export async function GET() {
  const sb = getSupabase();
  if (!process.env.NEXT_PUBLIC_SUPABASE_URL || !process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY) {
    return NextResponse.json({ ok: true, supabase: 'not_configured', hint: 'Set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY.' }, { status: 200 });
  }
  try {
    const { error } = await sb.from('listings').select('id').limit(1);
    if (error) throw error;
    return NextResponse.json({ ok: true, supabase: 'ok' }, { status: 200 });
  } catch {
    return NextResponse.json({ ok: false, supabase: 'unreachable' }, { status: 503 });
  }
}
