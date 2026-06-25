import { ALLOWED_IMAGE_TYPES, MAX_IMAGE_SIZE, SAMARKAND_BOUNDS } from './constants';

export function formatPriceUzs(value: number): string {
  return value.toLocaleString('ru-RU') + ' UZS';
}

export function formatTimestamp(iso: string): string {
  if (!iso) return '';
  return iso.replace('T', ' ').slice(0, 16);
}

// Returns null for empty pair, [lat, lng] for valid, error string for invalid.
// Normalizes comma decimal separator (users in UZ/RU often type "41,31").
export function validateCoords(
  latStr: string,
  lngStr: string,
): null | [number, number] | string {
  const a = (latStr ?? '').trim().replace(',', '.');
  const b = (lngStr ?? '').trim().replace(',', '.');
  if (!a && !b) return null;
  if (!a || !b) return 'Укажите и широту, и долготу, или оставьте оба поля пустыми.';
  const lat = parseFloat(a);
  const lng = parseFloat(b);
  if (isNaN(lat) || isNaN(lng)) return 'Широта и долгота должны быть числами (например 39.65 и 66.97).';
  if (
    lat < SAMARKAND_BOUNDS.lat.min || lat > SAMARKAND_BOUNDS.lat.max ||
    lng < SAMARKAND_BOUNDS.lng.min || lng > SAMARKAND_BOUNDS.lng.max
  ) {
    return 'Координаты вне допустимого региона (ожидается территория Самарканда).';
  }
  return [lat, lng];
}

export function validateFile(file: File): string | null {
  if (file.size > MAX_IMAGE_SIZE) return 'Файл больше 5 МБ. Выберите другое изображение.';
  if (!ALLOWED_IMAGE_TYPES.includes(file.type)) return 'Поддерживаются только JPG, PNG, WebP.';
  return null;
}

export function fileExtension(file: File): string {
  const parts = file.name.split('.');
  const ext = parts.length > 1 ? `.${parts[parts.length - 1].toLowerCase()}` : '.jpg';
  return ['.jpg', '.jpeg', '.png', '.webp'].includes(ext) ? ext : '.jpg';
}
