'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useRequireAuth } from '@/hooks/useRequireAuth';
import { useLang } from '@/contexts/LangContext';
import { getAuthedClient } from '@/lib/supabase';
import { validateCoords, validateFile, fileExtension } from '@/lib/utils';
import { LISTING_IMAGES_BUCKET } from '@/lib/constants';
import { MapPicker } from '@/components/MapPicker';

export default function CreatePage() {
  const { t } = useLang();
  const auth = useRequireAuth();
  const router = useRouter();

  const [listingType, setListingType] = useState<'rent' | 'sale'>('rent');
  const [title, setTitle] = useState('');
  const [district, setDistrict] = useState('');
  const [rooms, setRooms] = useState('1');
  const [price, setPrice] = useState('');
  const [phone, setPhone] = useState('');
  const [agency, setAgency] = useState('');
  const [lat, setLat] = useState('');
  const [lng, setLng] = useState('');
  const [pendingImageUrl, setPendingImageUrl] = useState('');
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [submitting, setSubmitting] = useState(false);

  if (auth.loading) return <div className="flex items-center justify-center min-h-[50vh]"><span className="text-gray-400">...</span></div>;

  async function handlePhotoChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    const err = validateFile(file);
    if (err) { setError(err); return; }
    if (!auth.accessToken || !auth.userId) { setError('Войдите в аккаунт.'); return; }
    setUploading(true);
    setError('');
    try {
      const ext = fileExtension(file);
      const path = `${auth.userId}/${crypto.randomUUID()}${ext}`;
      const sb = getAuthedClient(auth.accessToken);
      const { error: uploadError } = await sb.storage.from(LISTING_IMAGES_BUCKET).upload(path, file, { contentType: file.type, upsert: true });
      if (uploadError) throw uploadError;
      const { data } = sb.storage.from(LISTING_IMAGES_BUCKET).getPublicUrl(path);
      setPendingImageUrl(data.publicUrl);
    } catch (e) {
      setError(String(e));
    } finally {
      setUploading(false);
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!title || !district || !price || Number(price) <= 0) {
      setError('Заполните поля: заголовок, район и корректную цену.');
      return;
    }
    if (title.length > 200 || district.length > 100) {
      setError('Заголовок — не более 200 символов, район — не более 100.');
      return;
    }
    if (!auth.isLoggedIn || !auth.accessToken || !auth.userId) return;
    if (auth.isBlocked) { setError('Ваш аккаунт заблокирован.'); return; }

    const coordsResult = validateCoords(lat, lng);
    if (typeof coordsResult === 'string') { setError(coordsResult); return; }

    const sb = getAuthedClient(auth.accessToken);
    const since = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();
    const { count } = await sb.from('listings').select('id', { count: 'exact', head: true }).eq('owner_id', auth.userId).gte('created_at', since);
    if ((count ?? 0) >= 10) { setError('Максимум 10 объявлений за 24 часа. Попробуйте позже.'); return; }

    setSubmitting(true);
    setError('');
    const row: Record<string, unknown> = {
      listing_type: listingType,
      title: title.slice(0, 200),
      district: district.slice(0, 100),
      rooms: Math.max(1, parseInt(rooms) || 1),
      price: parseInt(price),
      owner_id: auth.userId,
    };
    if (phone.trim()) row.phone = phone.trim().slice(0, 30);
    if (agency.trim()) row.agency = agency.trim().slice(0, 100);
    if (pendingImageUrl) row.image_url = pendingImageUrl;
    if (Array.isArray(coordsResult)) { row.latitude = coordsResult[0]; row.longitude = coordsResult[1]; }

    const { error: insertError } = await sb.from('listings').insert(row);
    setSubmitting(false);
    if (insertError) {
      if (pendingImageUrl) {
        const path = pendingImageUrl.split(`/${LISTING_IMAGES_BUCKET}/`)[1];
        if (path) await sb.storage.from(LISTING_IMAGES_BUCKET).remove([path]);
      }
      setError('Не удалось сохранить объявление. Попробуйте ещё раз.');
      return;
    }
    setSuccess('Объявление опубликовано.');
    setTimeout(() => router.push('/my-listings'), 1500);
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 space-y-5">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">{t('create_page_title')}</h1>
        <p className="text-sm text-gray-500 mt-1">{t('create_page_subtitle')}</p>
      </div>

      {error && <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-700">{error}</div>}
      {success && <div className="p-3 rounded-lg bg-green-50 border border-green-200 text-sm text-green-700">{success}</div>}

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Listing type toggle */}
        <div className="bg-white rounded-xl border border-gray-200 p-4 space-y-2">
          <label className="text-sm font-medium text-gray-700">{t('listing_type_label')}</label>
          <div className="flex gap-2">
            <button
              type="button"
              onClick={() => setListingType('rent')}
              className={`flex-1 py-2 rounded-xl text-sm font-semibold border transition-colors ${
                listingType === 'rent'
                  ? 'bg-teal-600 text-white border-teal-600'
                  : 'border-gray-200 text-gray-600 hover:bg-gray-50'
              }`}
            >
              {t('listing_type_rent')}
            </button>
            <button
              type="button"
              onClick={() => setListingType('sale')}
              className={`flex-1 py-2 rounded-xl text-sm font-semibold border transition-colors ${
                listingType === 'sale'
                  ? 'bg-teal-600 text-white border-teal-600'
                  : 'border-gray-200 text-gray-600 hover:bg-gray-50'
              }`}
            >
              {t('listing_type_sale')}
            </button>
          </div>
        </div>

        {/* Main fields */}
        <div className="bg-white rounded-xl border border-gray-200 p-4 space-y-3">
          <input value={title} onChange={(e) => setTitle(e.target.value.slice(0, 200))} placeholder={t('create_ph_title')} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
          <div className="grid grid-cols-2 gap-3">
            <input value={district} onChange={(e) => setDistrict(e.target.value.slice(0, 100))} placeholder={t('create_ph_district')} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
            <input type="number" value={rooms} onChange={(e) => setRooms(e.target.value)} min={1} placeholder={t('create_ph_rooms')} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
          </div>
          <input type="number" value={price} onChange={(e) => setPrice(e.target.value)} placeholder={t('create_ph_price')} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
          <div>
            <label className="text-xs font-medium text-gray-500 block mb-1">{t('create_phone_label')}</label>
            <input value={phone} onChange={(e) => setPhone(e.target.value.slice(0, 30))} placeholder={t('create_ph_phone')} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
          </div>
          <div>
            <label className="text-xs font-medium text-gray-500 block mb-1">{t('create_agency_label')}</label>
            <input value={agency} onChange={(e) => setAgency(e.target.value.slice(0, 100))} placeholder={t('create_ph_agency')} className="w-full px-3 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-500" />
          </div>
        </div>

        {/* Photo */}
        <div className="bg-white rounded-xl border border-gray-200 p-4 space-y-2">
          <label className="text-sm font-medium text-gray-700">{t('create_photo_label')}</label>
          {pendingImageUrl ? (
            <div className="relative">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={pendingImageUrl} alt="" className="w-full h-40 object-cover rounded-xl border border-gray-200" />
              <button type="button" onClick={() => setPendingImageUrl('')} className="absolute top-2 right-2 bg-white/90 text-red-600 text-xs font-medium px-2 py-1 rounded-lg border border-gray-200 hover:bg-white transition-colors">
                {t('create_photo_remove')}
              </button>
            </div>
          ) : (
            <label className="block w-full border-2 border-dashed border-gray-200 rounded-xl p-6 text-center cursor-pointer hover:border-teal-400 transition-colors">
              <span className="text-sm text-gray-400">{uploading ? 'Загрузка...' : t('create_photo_drop')}</span>
              <input type="file" accept="image/jpeg,image/png,image/webp" onChange={handlePhotoChange} className="hidden" disabled={uploading} />
            </label>
          )}
        </div>

        {/* Location map picker */}
        <div className="bg-white rounded-xl border border-gray-200 p-4 space-y-2">
          <label className="text-sm font-medium text-gray-700">{t('create_location_label')}</label>
          <MapPicker lat={lat} lng={lng} onChange={(la, ln) => { setLat(la); setLng(ln); }} />
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          <button type="submit" disabled={submitting || uploading} className="flex items-center gap-1.5 px-5 py-2.5 bg-teal-600 text-white font-semibold text-sm rounded-xl hover:bg-teal-700 transition-colors disabled:opacity-50">
            {submitting ? '...' : t('create_btn_publish')}
          </button>
          <span className="text-xs text-gray-500 px-2 py-1 bg-gray-100 rounded-lg">{t('common_normal')}</span>
          <span className="text-xs text-gray-400 px-2 py-1 bg-gray-100 rounded-lg">{t('create_premium_soon')}</span>
        </div>
      </form>
    </div>
  );
}
