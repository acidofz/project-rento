'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';

interface AdminStats {
  listingCount: number;
  userCount: number;
  recentListings: { id: number; title: string; owner_id: string; created_at: string }[];
  recentUsers: { id: string; email: string; created_at: string }[];
}

export default function AdminPage() {
  const auth = useAuth();
  const router = useRouter();
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [actionMsg, setActionMsg] = useState('');

  const adminIds = (process.env.NEXT_PUBLIC_ADMIN_USER_IDS ?? '').split(',').map((s) => s.trim()).filter(Boolean);
  const isAdmin = auth.userId && adminIds.includes(auth.userId);

  useEffect(() => {
    if (!auth.loading && !auth.isLoggedIn) { router.push('/login'); return; }
    if (!auth.loading && auth.isLoggedIn && !isAdmin) { router.push('/'); return; }
  }, [auth.loading, auth.isLoggedIn, isAdmin, router]);

  useEffect(() => {
    if (auth.loading || !isAdmin || !auth.accessToken) return;
    fetch('/api/admin/stats', { headers: { Authorization: `Bearer ${auth.accessToken}` } })
      .then((r) => r.json())
      .then((data) => { setStats(data); setLoading(false); })
      .catch(() => { setError('Не удалось загрузить статистику.'); setLoading(false); });
  }, [auth.loading, isAdmin, auth.accessToken]);

  async function deleteListing(id: number) {
    if (!auth.accessToken) return;
    const r = await fetch('/api/admin/delete-listing', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${auth.accessToken}` }, body: JSON.stringify({ listing_id: id }) });
    if (!r.ok) { setActionMsg('Ошибка при удалении.'); return; }
    setActionMsg(`Объявление #${id} удалено.`);
    setStats((prev) => prev ? { ...prev, recentListings: prev.recentListings.filter((l) => l.id !== id) } : prev);
  }

  async function setBlock(userId: string, blocked: boolean) {
    if (!auth.accessToken) return;
    const r = await fetch('/api/admin/set-block', { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${auth.accessToken}` }, body: JSON.stringify({ user_id: userId, blocked }) });
    if (!r.ok) { setActionMsg('Ошибка.'); return; }
    setActionMsg(`Пользователь ${userId.slice(0, 8)} ${blocked ? 'заблокирован' : 'разблокирован'}.`);
  }

  if (auth.loading) return <div className="flex items-center justify-center min-h-[50vh]"><span className="text-gray-400">...</span></div>;
  if (!isAdmin) return null;

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Администрирование</h1>

      {error && <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-700">{error}</div>}
      {actionMsg && <div className="p-3 rounded-lg bg-teal-50 border border-teal-200 text-sm text-teal-700">{actionMsg}</div>}

      {loading ? (
        <div className="text-center py-10 text-gray-400">Загрузка...</div>
      ) : stats ? (
        <>
          {/* Stats row */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: 'Объявлений', value: stats.listingCount },
              { label: 'Пользователей', value: stats.userCount },
            ].map((s) => (
              <div key={s.label} className="bg-white rounded-xl border border-gray-200 p-4 text-center">
                <div className="text-3xl font-extrabold text-teal-700">{s.value}</div>
                <div className="text-xs text-gray-500 mt-0.5">{s.label}</div>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {/* Recent listings */}
            <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
              <div className="px-4 py-3 border-b border-gray-100 font-semibold text-sm text-gray-900">Последние объявления</div>
              <div className="divide-y divide-gray-100">
                {stats.recentListings.map((l) => (
                  <div key={l.id} className="flex items-center gap-3 px-4 py-2.5">
                    <div className="flex-1 min-w-0">
                      <Link href={`/listing/${l.id}`} target="_blank" className="text-sm font-medium text-gray-900 hover:underline truncate block">{l.title}</Link>
                      <div className="text-xs text-gray-400">ID: {l.id} · {new Date(l.created_at).toLocaleDateString('ru-RU')}</div>
                    </div>
                    <button onClick={() => deleteListing(l.id)} className="flex-shrink-0 text-xs text-red-500 hover:text-red-700 px-2 py-1 border border-red-200 rounded-lg hover:bg-red-50 transition-colors">Удалить</button>
                  </div>
                ))}
              </div>
            </div>

            {/* Recent users */}
            <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
              <div className="px-4 py-3 border-b border-gray-100 font-semibold text-sm text-gray-900">Последние пользователи</div>
              <div className="divide-y divide-gray-100">
                {stats.recentUsers.map((u) => (
                  <div key={u.id} className="flex items-center gap-3 px-4 py-2.5">
                    <div className="flex-1 min-w-0">
                      <div className="text-sm text-gray-900 truncate">{u.email}</div>
                      <div className="text-xs text-gray-400">{u.id.slice(0, 8)} · {new Date(u.created_at).toLocaleDateString('ru-RU')}</div>
                    </div>
                    <div className="flex gap-1">
                      <button onClick={() => setBlock(u.id, true)} className="text-xs text-red-500 hover:text-red-700 px-1.5 py-0.5 border border-red-200 rounded hover:bg-red-50 transition-colors">Блок</button>
                      <button onClick={() => setBlock(u.id, false)} className="text-xs text-teal-600 hover:text-teal-800 px-1.5 py-0.5 border border-teal-200 rounded hover:bg-teal-50 transition-colors">Разблок</button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </>
      ) : null}
    </div>
  );
}
