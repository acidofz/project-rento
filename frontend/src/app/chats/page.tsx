'use client';

import { useEffect, useState, useRef, useCallback } from 'react';
import { useRequireAuth } from '@/hooks/useRequireAuth';
import { useLang } from '@/contexts/LangContext';
import { getAuthedClient } from '@/lib/supabase';
import { ChatSummary, ChatMessage, QuickContact } from '@/lib/types';
import { formatTimestamp } from '@/lib/utils';

export default function ChatsPage() {
  const { t } = useLang();
  const auth = useRequireAuth();
  const [chats, setChats] = useState<ChatSummary[]>([]);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [selectedChatId, setSelectedChatId] = useState(0);
  const [quickContacts, setQuickContacts] = useState<QuickContact[]>([]);
  const [userLabels, setUserLabels] = useState<Record<string, string>>({});
  const [newMessage, setNewMessage] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const mountedRef = useRef(true);
  useEffect(() => () => { mountedRef.current = false; }, []);

  const loadUserLabels = useCallback(async (userIds: string[]) => {
    if (!userIds.length || !auth.accessToken) return {};
    const sb = getAuthedClient(auth.accessToken);
    const { data } = await sb.from('profiles').select('id,username,email').in('id', userIds);
    const labels: Record<string, string> = {};
    for (const row of (data ?? []) as { id: string; username: string; email: string }[]) {
      labels[row.id] = row.username?.trim() || row.email?.split('@')[0] || `Пользователь ${row.id.slice(0, 8)}`;
    }
    return labels;
  }, [auth.accessToken]);

  const loadMessages = useCallback(async (chatId: number) => {
    if (!chatId || !auth.accessToken) return;
    const sb = getAuthedClient(auth.accessToken);
    const { data } = await sb.from('messages').select('id,chat_id,sender_id,body,created_at').eq('chat_id', chatId).order('id', { ascending: true });
    if (!mountedRef.current) return;
    const rows = (data ?? []) as ChatMessage[];
    const senderIds = Array.from(new Set(rows.map((r) => r.sender_id)));
    const labels = await loadUserLabels(senderIds);
    if (!mountedRef.current) return;
    setUserLabels((prev) => ({ ...prev, ...labels }));
    setMessages(rows.map((r) => ({ ...r, sender_label: labels[r.sender_id] || `Пользователь ${r.sender_id.slice(0, 8)}`, created_at_label: formatTimestamp(r.created_at) })));
  }, [auth.accessToken, loadUserLabels]);

  const loadChats = useCallback(async () => {
    if (!auth.isLoggedIn || !auth.accessToken || !auth.userId) return;
    const sb = getAuthedClient(auth.accessToken);
    const { data: memberRows } = await sb.from('chat_members').select('chat_id').eq('user_id', auth.userId);
    const chatIds = (memberRows ?? []).map((r: { chat_id: number }) => r.chat_id);
    if (!chatIds.length) { setChats([]); setQuickContacts([]); return; }
    const { data: allMembers } = await sb.from('chat_members').select('chat_id,user_id').in('chat_id', chatIds);
    const peerByChat: Record<number, string> = {};
    const allUserIds: string[] = [];
    for (const row of (allMembers ?? []) as { chat_id: number; user_id: string }[]) {
      allUserIds.push(row.user_id);
      if (row.user_id !== auth.userId) peerByChat[row.chat_id] = row.user_id;
    }
    const labels = await loadUserLabels(Array.from(new Set(allUserIds)));
    setUserLabels((prev) => ({ ...prev, ...labels }));
    const { data: chatRows } = await sb.from('chats').select('id,created_by,created_at').in('id', chatIds).order('id', { ascending: false });
    const chatList: ChatSummary[] = (chatRows ?? []).map((row: { id: number; created_by: string; created_at: string }) => ({
      id: row.id,
      created_by: row.created_by,
      peer_user_id: peerByChat[row.id] || '',
      peer_label: labels[peerByChat[row.id]] || 'Пользователь',
      created_at: row.created_at,
    }));
    setChats(chatList);
    const peerIds = Array.from(new Set(Object.values(peerByChat)));
    setQuickContacts(peerIds.map((uid) => ({ user_id: uid, label: labels[uid] || `Пользователь ${uid.slice(0, 8)}` })));
    if (chatList.length && !selectedChatId) {
      setSelectedChatId(chatList[0].id);
      await loadMessages(chatList[0].id);
    }
  }, [auth.isLoggedIn, auth.accessToken, auth.userId, loadUserLabels, loadMessages, selectedChatId]);

  useEffect(() => { if (!auth.loading) loadChats(); }, [auth.loading, auth.isLoggedIn]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (!selectedChatId) return;
    loadMessages(selectedChatId);
    pollRef.current = setInterval(() => loadMessages(selectedChatId), 6000);
    return () => { if (pollRef.current) clearInterval(pollRef.current); };
  }, [selectedChatId, loadMessages]);

  async function selectChat(chatId: number) {
    setSelectedChatId(chatId);
    await loadMessages(chatId);
  }

  async function sendMessage() {
    const text = newMessage.trim();
    if (!text || !selectedChatId || !auth.accessToken || !auth.userId) return;
    if (text.length > 2000) { setError('Сообщение слишком длинное (максимум 2000 символов).'); return; }
    if (auth.isBlocked) { setError('Ваш аккаунт заблокирован.'); return; }
    const sb = getAuthedClient(auth.accessToken);
    const since = new Date(Date.now() - 5 * 60 * 1000).toISOString();
    const { count } = await sb.from('messages').select('id', { count: 'exact', head: true }).eq('sender_id', auth.userId).gte('created_at', since);
    if ((count ?? 0) >= 30) { setError('Слишком много сообщений. Подождите несколько минут.'); return; }
    await sb.from('messages').insert({ chat_id: selectedChatId, sender_id: auth.userId, body: text });
    setNewMessage('');
    setError('');
    await loadMessages(selectedChatId);
  }

  async function startChatWith(peerId: string) {
    if (!auth.accessToken || !auth.userId) return;
    if (peerId === auth.userId) { setError('Нельзя создать чат с самим собой.'); return; }
    const sb = getAuthedClient(auth.accessToken);
    // Find existing chat
    const { data: myRows } = await sb.from('chat_members').select('chat_id').eq('user_id', auth.userId);
    const { data: peerRows } = await sb.from('chat_members').select('chat_id').eq('user_id', peerId);
    const myChatIds = new Set((myRows ?? []).map((r: { chat_id: number }) => r.chat_id));
    const existing = (peerRows ?? []).find((r: { chat_id: number }) => myChatIds.has(r.chat_id));
    if (existing) { setSelectedChatId(existing.chat_id); await loadMessages(existing.chat_id); setSuccess('Открыт существующий чат.'); return; }
    const { data: chatData } = await sb.from('chats').insert({ created_by: auth.userId }).select('id').single();
    if (!chatData?.id) { setError('Не удалось создать чат.'); return; }
    await sb.from('chat_members').insert([{ chat_id: chatData.id, user_id: auth.userId }, { chat_id: chatData.id, user_id: peerId }]);
    setSuccess('Чат создан.'); setSelectedChatId(chatData.id); await loadChats(); await loadMessages(chatData.id);
  }

  if (auth.loading) return <div className="flex items-center justify-center min-h-[50vh]"><span className="text-gray-400">...</span></div>;

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 space-y-5">
      <div className="flex items-center gap-3">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{t('chats_title')}</h1>
          <p className="text-xs text-gray-500 mt-0.5">{t('chats_hint')}</p>
        </div>
        <div className="flex-1" />
        <button onClick={loadChats} className="px-3 py-1.5 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50">{t('chats_refresh')}</button>
      </div>

      {error && <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-700">{error}</div>}
      {success && <div className="p-3 rounded-lg bg-green-50 border border-green-200 text-sm text-green-700">{success}</div>}

      {/* Quick contacts */}
      {quickContacts.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200 p-4 space-y-2">
          <p className="text-sm font-medium text-gray-700">{t('chats_quick_contacts')}</p>
          <div className="flex flex-wrap gap-2">
            {quickContacts.map((c) => (
              <button key={c.user_id} onClick={() => startChatWith(c.user_id)} className="px-3 py-1.5 bg-teal-50 border border-teal-200 text-teal-700 text-xs font-medium rounded-lg hover:bg-teal-100 transition-colors">
                {c.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Main grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Dialogs */}
        <div className="bg-white rounded-xl border border-gray-200 p-4 space-y-3">
          <p className="text-sm font-bold text-gray-900">{t('chats_dialogs')}</p>
          {chats.length === 0 ? (
            <p className="text-sm text-gray-400">{t('chats_quick_empty')}</p>
          ) : (
            <div className="space-y-2">
              {chats.map((chat) => (
                <div key={chat.id} className={`p-3 rounded-xl border cursor-pointer transition-colors ${selectedChatId === chat.id ? 'bg-teal-50 border-teal-200' : 'border-gray-100 hover:bg-gray-50'}`} onClick={() => selectChat(chat.id)}>
                  <div className="font-medium text-sm text-gray-900">{chat.peer_label || `${t('chats_chat_id')}${chat.id}`}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Messages */}
        <div className="bg-white rounded-xl border border-gray-200 flex flex-col" style={{ minHeight: '400px' }}>
          <div className="p-4 border-b border-gray-100">
            <p className="text-sm font-bold text-gray-900">{t('chats_messages')}</p>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.length === 0 ? (
              <p className="text-sm text-gray-400 text-center pt-8">Выберите чат слева</p>
            ) : (
              messages.map((msg) => (
                <div key={msg.id} className={`flex flex-col ${msg.sender_id === auth.userId ? 'items-end' : 'items-start'}`}>
                  <div className="text-xs text-gray-400 mb-0.5">{msg.sender_label || userLabels[msg.sender_id] || 'Пользователь'}</div>
                  <div className={`max-w-[85%] px-3 py-2 rounded-xl text-sm ${msg.sender_id === auth.userId ? 'bg-teal-600 text-white' : 'bg-gray-100 text-gray-900'}`}>
                    {msg.body}
                  </div>
                </div>
              ))
            )}
          </div>
          {selectedChatId > 0 && (
            <div className="p-3 border-t border-gray-100 flex gap-2">
              <input
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); } }}
                placeholder={t('chats_input_ph')}
                className="flex-1 px-3 py-2 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
              <button onClick={sendMessage} className="px-4 py-2 bg-teal-600 text-white text-sm font-medium rounded-xl hover:bg-teal-700 transition-colors">
                {t('chats_send')}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
