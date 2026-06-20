'use client';

import { useEffect, useState } from 'react';

interface ReadyResult {
  ok: boolean;
  supabase: 'ok' | 'unreachable' | 'not_configured';
}

export default function HealthPage() {
  const [data, setData] = useState<ReadyResult | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  async function check() {
    setLoading(true);
    setError('');
    try {
      const r = await fetch('/api/ready');
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      setData(await r.json());
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { check(); }, []);

  function statusBadge(status: string) {
    if (status === 'ok') return <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-green-100 text-green-700 text-xs font-bold"><span className="w-1.5 h-1.5 rounded-full bg-green-500 inline-block" />OK</span>;
    return <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-red-100 text-red-700 text-xs font-bold"><span className="w-1.5 h-1.5 rounded-full bg-red-500 inline-block" />{status}</span>;
  }

  return (
    <div className="max-w-md mx-auto px-4 py-10 space-y-5">
      <div className="flex items-center gap-3">
        <h1 className="text-xl font-bold text-gray-900">Состояние системы</h1>
        <button onClick={check} className="ml-auto px-3 py-1.5 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50 transition-colors">Проверить снова</button>
      </div>

      {loading && <div className="text-center py-8 text-gray-400">Проверяем...</div>}
      {error && <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-700">{error}</div>}

      {data && !loading && (
        <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
          <div className="px-4 py-3 border-b border-gray-100 text-sm font-semibold text-gray-700">Компоненты</div>
          <div className="divide-y divide-gray-100">
            <div className="flex items-center justify-between px-4 py-3">
              <span className="text-sm text-gray-700">Приложение (Next.js)</span>
              {statusBadge('ok')}
            </div>
            <div className="flex items-center justify-between px-4 py-3">
              <span className="text-sm text-gray-700">Supabase</span>
              {statusBadge(data.supabase)}
            </div>
          </div>
          <div className={`px-4 py-3 text-sm font-semibold ${data.ok ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
            {data.ok ? '✓ Все системы работают' : '✗ Есть проблемы'}
          </div>
        </div>
      )}
    </div>
  );
}
