'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRequireAuth } from '@/hooks/useRequireAuth';
import { useLang } from '@/contexts/LangContext';
import { getAuthedClient } from '@/lib/supabase';
import { Listing } from '@/lib/types';
import { ListingCard } from '@/components/ListingCard';
import { MapPicker } from '@/components/MapPicker';
import { validateCoords, validateFile, fileExtension } from '@/lib/utils';
import { LISTING_IMAGES_BUCKET } from '@/lib/constants';

export default function MyListingsPage() {
  const { t } = useLang();
  const auth = useRequireAuth();
  const [listings, setListings] = useState<Listing[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const MAX_PHOTOS = 10;
  const [editingId, setEditingId] = useState(0);
  const [editListingType, setEditListingType] = useState<'rent' | 'sale'>('rent');
  const [editTitle, setEditTitle] = useState('');
  const [editDistrict, setEditDistrict] = useState('');
  const [editRooms, setEditRooms] = useState('1');
  const [editPrice, setEditPrice] = useState('');
  const [editPhone, setEditPhone] = useState('');
  const [editAgency, setEditAgency] = useState('');
  const [editLat, setEditLat] = useState('');
  const [editLng, setEditLng] = useState('');
  const [editImageUrls, setEditImageUrls] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  async function load() {
    if (!auth.isLoggedIn || !auth.accessToken || !auth.userId) return;
    setLoading(true);
    const { data, error: err } = await getAuthedClient(auth.accessToken)
      .from('listings')
      .select('id,title,district,rooms,price,owner_id,image_url,image_urls,latitude,longitude,is_premium,phone,agency,listing_type')
      .eq('owner_id', auth.userId)
      .order('id', { ascending: false });
    if (err) setError('Не удалось загрузить объявления.');
    else setListings((data as Listing[]) ?? []);
    setLoading(false);
  }

  useEffect(() => { if (!auth.loading) load(); }, [auth.loading, auth.isLoggedIn, auth.accessToken]); // eslint-disable-line react-hooks/exhaustive-deps

  function startEdit(l: Listing) {
    setEditingId(l.id);
    setEditListingType(l.listing_type ?? 'rent');
    setEditTitle(l.title);
    setEditDistrict(l.district);
    setEditRooms(String(l.rooms));
    setEditPrice(String(l.price));
    setEditPhone(l.phone || '');
    setEditAgency(l.agency || '');
    setEditLat(l.latitude != null ? String(l.latitude) : '');
    setEditLng(l.longitude != null ? String(l.longitude) : '');
    const imgs = l.image_urls?.length ? l.image_urls : l.image_url ? [l.image_url] : [];
    setEditImageUrls(imgs);
    setError('');
  }

  function cancelEdit() { setEditingId(0); setError(''); }

  async function handleEditPhotos(e: React.ChangeEvent<HTMLInputElement>) {
    const files = Array.from(e.target.files ?? []);
    if (!files.length || !auth.accessToken || !auth.userId) return;
    const remaining = MAX_PHOTOS - editImageUrls.length;
    if (remaining <= 0) { setError(`Максимум ${MAX_PHOTOS} фотографий.`); return; }
    const toUpload = files.slice(0, remaining);
    for (const file of toUpload) {
      const err = validateFile(file);
      if (err) { setError(err); return; }
    }
    setUploading(true);
    setUploadProgress(0);
    try {
      const sb = getAuthedClient(auth.accessToken);
      const uploaded: string[] = [];
      for (let i = 0; i < toUpload.length; i++) {
        const file = toUpload[i];
        const ext = fileExtension(file);
        const path = `${auth.userId}/${crypto.randomUUID()}${ext}`;
        const { error: uploadError } = await sb.storage.from(LISTING_IMAGES_BUCKET).upload(path, file, { contentType: file.type, upsert: true });
        if (uploadError) throw uploadError;
        const { data } = sb.storage.from(LISTING_IMAGES_BUCKET).getPublicUrl(path);
        uploaded.push(data.publicUrl);
        setUploadProgress(Math.round(((i + 1) / toUpload.length) * 100));
      }
      setEditImageUrls((prev) => [...prev, ...uploaded]);
    } catch (e) { setError(String(e)); }
    finally { setUploading(false); setUploadProgress(0); e.target.value = ''; }
  }

  async function saveEdit() {
    if (!editTitle || !editDistrict || !editPrice || Number(editPrice) <= 0) { setError('Заполните все поля корректно.'); return; }
    if (!auth.accessToken || !auth.userId) return;
    const coordsResult = validateCoords(editLat, editLng);
    if (typeof coordsResult === 'string') { setError(coordsResult); return; }
    const row: Record<string, unknown> = {
      listing_type: editListingType,
      title: editTitle.slice(0, 200),
      district: editDistrict.slice(0, 100),
      rooms: Math.max(1, parseInt(editRooms) || 1),
      price: Math.round(Number(editPrice)),
      image_url: editImageUrls[0] ?? null,
      image_urls: editImageUrls,
      phone: editPhone.trim().slice(0, 30) || null,
      agency: editAgency.trim().slice(0, 100) || null,
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

          {/* Type toggle */}
          <div className="space-y-1">
            <label className="text-xs font-medium text-gray-500">{t('listing_type_label')}</label>
            <div className="flex gap-2">
              <button type="button" onClick={() => setEditListingType('rent')} className={`flex-1 py-2 rounded-xl text-sm font-semibold border transition-colors ${editListingType === 'rent' ? 'bg-teal-600 text-white border-teal-600' : 'border-gray-200 text-gray-600 hover:bg-gray-50'}`}>{t('listing_type_rent')}</button>
              <button type="button" onClick={() => setEditListingType('sale')} className={`flex-1 py-2 rounded-xl text-sm font-semibold border transition-colors ${editListingType === 'sale' ? 'bg-teal-600 text-white border-teal-600' : 'border-gray-200 text-gray-600 hover:bg-gray-50'}`}>{t('listing_type_sale')}</button>
            </div>
          </div>

          <input value={editTitle} onChange={(e) => setEditTitle(e.target.value)} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
          <div className="grid grid-cols-2 gap-3">
            <input value={editDistrict} onChange={(e) => setEditDistrict(e.target.value)} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
            <input type="number" value={editRooms} onChange={(e) => setEditRooms(e.target.value)} min={1} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
          </div>
          <input type="number" value={editPrice} onChange={(e) => setEditPrice(e.target.value)} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
          <input value={editPhone} onChange={(e) => setEditPhone(e.target.value)} placeholder={t('create_ph_phone')} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
          <div>
            <label className="text-xs font-medium text-gray-500 block mb-1">{t('edit_agency_label')}</label>
            <input value={editAgency} onChange={(e) => setEditAgency(e.target.value.slice(0, 100))} placeholder={t('create_ph_agency')} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
          </div>
          <div>
            <label className="text-xs font-medium text-gray-500 block mb-1">{t('edit_location_label')}</label>
            <MapPicker lat={editLat} lng={editLng} onChange={(la, ln) => { setEditLat(la); setEditLng(ln); }} />
          </div>
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs font-medium text-gray-500">{t('edit_photo_label')}</label>
              <span className="text-xs text-gray-400">{editImageUrls.length}/{MAX_PHOTOS}</span>
            </div>
            {editImageUrls.length > 0 && (
              <div className="grid grid-cols-3 gap-2 mb-2">
                {editImageUrls.map((url, i) => (
                  <div key={url} className="relative aspect-square rounded-xl overflow-hidden border border-gray-200">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src={url} alt="" className="w-full h-full object-cover" />
                    {i === 0 && <span className="absolute top-1 left-1 bg-teal-600 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full">Обложка</span>}
                    <button type="button" onClick={() => setEditImageUrls((prev) => prev.filter((_, j) => j !== i))} className="absolute top-1 right-1 w-5 h-5 bg-black/60 text-white rounded-full flex items-center justify-center text-xs hover:bg-black/80">×</button>
                  </div>
                ))}
              </div>
            )}
            {editImageUrls.length < MAX_PHOTOS && (
              <label className="block w-full border-2 border-dashed border-gray-200 rounded-xl p-4 text-center cursor-pointer hover:border-teal-400 transition-colors">
                {uploading ? (
                  <div className="space-y-1">
                    <span className="text-sm text-gray-400">Загрузка... {uploadProgress}%</span>
                    <div className="w-full bg-gray-100 rounded-full h-1.5"><div className="bg-teal-500 h-1.5 rounded-full transition-all" style={{ width: `${uploadProgress}%` }} /></div>
                  </div>
                ) : (
                  <span className="text-sm text-gray-400">{editImageUrls.length === 0 ? 'Добавить фото' : 'Добавить ещё'} — перетащите или выберите</span>
                )}
                <input type="file" accept="image/jpeg,image/png,image/webp" multiple onChange={handleEditPhotos} className="hidden" disabled={uploading} />
              </label>
            )}
          </div>
          <div className="flex items-center gap-3">
            <button onClick={saveEdit} disabled={uploading} className="px-5 py-2 bg-teal-600 text-white font-semibold text-sm rounded-xl hover:bg-teal-700 transition-colors disabled:opacity-50">{t('edit_btn_save')}</button>
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
