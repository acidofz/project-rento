'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRequireAuth } from '@/hooks/useRequireAuth';
import { useLang } from '@/contexts/LangContext';
import { getAuthedClient } from '@/lib/supabase';
import { Listing } from '@/lib/types';
import { ListingCard } from '@/components/ListingCard';
import { validateCoords, validateFile, fileExtension } from '@/lib/utils';
import { LISTING_IMAGES_BUCKET } from '@/lib/constants';

export default function MyListingsPage() {
  const { t } = useLang();
  const auth = useRequireAuth();
  const [listings, setListings] = useState<Listing[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const [editingId, setEditingId] = useState(0);
  const [editTitle, setEditTitle] = useState('');
  const [editDistrict, setEditDistrict] = useState('');
  const [editRooms, setEditRooms] = useState('1');
  const [editPrice, setEditPrice] = useState('');
  const [editPhone, setEditPhone] = useState('');
  const [editLat, setEditLat] = useState('');
  const [editLng, setEditLng] = useState('');
  const [editImageUrl, setEditImageUrl] = useState('');
  const [uploading, setUploading] = useState(false);

  async function load() {
    if (!auth.isLoggedIn || !auth.accessToken || !auth.userId) return;
    setLoading(true);
    const { data, error: err } = await getAuthedClient(auth.accessToken).from('listings').select('id,title,district,rooms,price,owner_id,image_url,latitude,longitude,is_premium,phone').eq('owner_id', auth.userId).order('id', { ascending: false });
    if (err) setError('Не удалось загрузить объявления.');
    else setListings((data as Listing[]) ?? []);
    setLoading(false);
  }

  useEffect(() => { if (!auth.loading) load(); }, [auth.loading, auth.isLoggedIn, auth.accessToken]); // eslint-disable-line react-hooks/exhaustive-deps

  function startEdit(l: Listing) {
    setEditingId(l.id);
    setEditTitle(l.title);
    setEditDistrict(l.district);
    setEditRooms(String(l.rooms));
    setEditPrice(String(l.price));
    setEditPhone(l.phone || '');
    setEditLat(l.latitude != null ? String(l.latitude) : '');
    setEditLng(l.longitude != null ? String(l.longitude) : '');
    setEditImageUrl(l.image_url || '');
    setError('');
  }

  function cancelEdit() { setEditingId(0); setError(''); }

  async function handleEditPhoto(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file || !auth.accessToken || !auth.userId) return;
    const err = validateFile(file);
    if (err) { setError(err); return; }
    setUploading(true);
    try {
      const ext = fileExtension(file);
      const path = `${auth.userId}/${crypto.randomUUID()}${ext}`;
      const sb = getAuthedClient(auth.accessToken);
      await sb.storage.from(LISTING_IMAGES_BUCKET).upload(path, file, { contentType: file.type, upsert: true });
      const { data } = sb.storage.from(LISTING_IMAGES_BUCKET).getPublicUrl(path);
      setEditImageUrl(data.publicUrl);
    } catch (e) { setError(String(e)); }
    finally { setUploading(false); }
  }

  async function saveEdit() {
    if (!editTitle || !editDistrict || !editPrice || Number(editPrice) <= 0) { setError('Заполните все поля корректно.'); return; }
    if (!auth.accessToken || !auth.userId) return;
    const coordsResult = validateCoords(editLat, editLng);
    if (typeof coordsResult === 'string') { setError(coordsResult); return; }
    const row: Record<string, unknown> = {
      title: editTitle.slice(0, 200),
      district: editDistrict.slice(0, 100),
      rooms: Math.max(1, parseInt(editRooms) || 1),
      price: parseInt(editPrice),
      image_url: editImageUrl || null,
      phone: editPhone.trim().slice(0, 30) || null,
      latitude: Array.isArray(coordsResult) ? coordsResult[0] : null,
      longitude: Array.isArray(coordsResult) ? coordsResult[1] : null,
    };
    const { error: err } = await getAuthedClient(auth.accessToken).from('listings').update(row).eq('id', editingId).eq('owner_id', auth.userId);
    if (err) { setError('Не удалось обновить объявление.'); return; }
    setSuccess('Объявление обновлено.'); cancelEdit(); load();
  }

  async function deleteListing(id: number) {
    if (!auth.accessToken || !auth.userId) return;
    const { error: err } = await getAuthedClient(auth.accessToken).from('listings').delete().eq('id', id).eq('owner_id', auth.userId);
    if (err) { setError('Не удалось удалить объявление.'); return; }
    setSuccess('Объявление удалено.'); load();
  }

  if (auth.loading) return <div className="flex items-center justify-center min-h-[50vh]"><span className="text-gray-400">...</span></div>;

  return (
    <div className="max-w-6xl mx-auto px-4 py-6 space-y-5">
      <div className="flex items-center gap-3">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{t('my_listings_title')}</h1>
          <p className="text-sm text-gray-500 mt-0.5">{t('my_listings_subtitle')}</p>
        </div>
        <div className="flex-1" />
        <button onClick={load} className="px-3 py-1.5 border border-gray-200 rounded-lg text-sm text-gray-600 hover:bg-gray-50">{t('my_listings_refresh')}</button>
      </div>

      {error && <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-700">{error}</div>}
      {success && <div className="p-3 rounded-lg bg-green-50 border border-green-200 text-sm text-green-700">{success}</div>}

      {/* Edit form */}
      {editingId > 0 && (
        <div className="bg-white rounded-xl border border-teal-200 p-5 space-y-3">
          <h2 className="font-bold text-gray-900">{t('edit_page_title')}</h2>
          <input value={editTitle} onChange={(e) => setEditTitle(e.target.value)} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
          <div className="grid grid-cols-2 gap-3">
            <input value={editDistrict} onChange={(e) => setEditDistrict(e.target.value)} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
            <input type="number" value={editRooms} onChange={(e) => setEditRooms(e.target.value)} min={1} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
          </div>
          <input type="number" value={editPrice} onChange={(e) => setEditPrice(e.target.value)} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
          <input value={editPhone} onChange={(e) => setEditPhone(e.target.value)} placeholder={t('create_ph_phone')} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
          <div>
            <label className="text-xs font-medium text-gray-500 block mb-1">{t('edit_location_label')}</label>
            <div className="grid grid-cols-2 gap-3">
              <input value={editLat} onChange={(e) => setEditLat(e.target.value)} placeholder={t('create_ph_lat')} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
              <input value={editLng} onChange={(e) => setEditLng(e.target.value)} placeholder={t('create_ph_lng')} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
            </div>
          </div>
          <div>
            <label className="text-xs font-medium text-gray-500 block mb-1">{t('edit_photo_label')}</label>
            {editImageUrl && (
              <div className="relative mb-2">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={editImageUrl} alt="" className="w-full h-32 object-cover rounded-xl border border-gray-200" />
                <button type="button" onClick={() => setEditImageUrl('')} className="absolute top-2 right-2 bg-white/90 text-red-600 text-xs font-medium px-2 py-1 rounded-lg border border-gray-200">{t('create_photo_remove')}</button>
              </div>
            )}
            <label className="block w-full border-2 border-dashed border-gray-200 rounded-xl p-4 text-center cursor-pointer hover:border-teal-400 transition-colors">
              <span className="text-sm text-gray-400">{uploading ? 'Загрузка...' : t('edit_photo_replace')}</span>
              <input type="file" accept="image/jpeg,image/png,image/webp" onChange={handleEditPhoto} className="hidden" disabled={uploading} />
            </label>
          </div>
          <div className="flex items-center gap-3">
            <button onClick={saveEdit} className="px-5 py-2 bg-teal-600 text-white font-semibold text-sm rounded-xl hover:bg-teal-700 transition-colors">{t('edit_btn_save')}</button>
            <button onClick={cancelEdit} className="px-5 py-2 border border-gray-200 text-gray-600 text-sm rounded-xl hover:bg-gray-50 transition-colors">{t('edit_btn_cancel')}</button>
          </div>
        </div>
      )}

      {loading ? (
        <div className="text-center py-10 text-gray-400 text-sm">...</div>
      ) : listings.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {listings.map((l) => (
            <div key={l.id} className="space-y-2">
              <ListingCard listing={l} roomsSuffix={t('rooms_suffix')} />
              <div className="flex gap-2">
                <button onClick={() => startEdit(l)} className="flex-1 px-3 py-1.5 border border-gray-200 text-sm text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">{t('my_listings_edit')}</button>
                <button onClick={() => deleteListing(l.id)} className="flex-1 px-3 py-1.5 border border-red-200 text-sm text-red-600 rounded-lg hover:bg-red-50 transition-colors">{t('my_listings_delete')}</button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center py-14 space-y-3">
          <p className="text-gray-500 text-sm">{t('my_listings_empty')}</p>
          <Link href="/create" className="px-3 py-1.5 bg-teal-600 text-white text-sm rounded-lg hover:bg-teal-700 transition-colors">{t('my_listings_create')}</Link>
        </div>
      )}
    </div>
  );
}
