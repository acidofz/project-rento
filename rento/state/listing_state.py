import json
import uuid
from pathlib import Path
from typing import Any

from pydantic import BaseModel
import reflex as rx
from storage3.exceptions import StorageApiError

from rento.supabase_client import get_supabase
from rento.utils.helpers import format_price_uzs

LISTING_IMAGES_BUCKET = "listing-images"
LISTINGS_PAGE_SIZE = 12
_ALLOWED_IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp"}


def _content_type_for_ext(ext: str) -> str:
    if ext in (".jpg", ".jpeg"):
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    return "image/webp"


def _ensure_supabase_storage_uses_current_jwt(sb: Any) -> None:
    """Recreate the Storage client so requests use the latest Authorization header.

    The underlying httpx client snapshots headers at construction; if Storage was
    first touched before login, uploads would still use the anon key and RLS
    would reject them.
    """
    try:
        session = sb.auth.get_session()
    except Exception:
        session = None
    if session is None or not getattr(session, "access_token", None):
        return
    auth_header = f"Bearer {session.access_token}"
    sb.options.headers["Authorization"] = auth_header
    if getattr(sb.auth, "_headers", None) is not None:
        sb.auth._headers["Authorization"] = auth_header
    sb._storage = None


def _humanize_storage_upload_error(exc: Exception) -> str:
    if isinstance(exc, StorageApiError):
        msg = (exc.message or "").lower()
        code = str(exc.code or "").lower()
        status = int(exc.status) if str(exc.status).isdigit() else 0
        if status in (401, 403) or "jwt" in msg or "unauthorized" in msg:
            return (
                "Сессия устарела или нет прав на загрузку. "
                "Выйдите из аккаунта и войдите снова, затем повторите загрузку."
            )
        if "row-level security" in msg or "rls" in msg or "policy" in msg:
            return (
                "Отказ хранилища (политики доступа). "
                "Проверьте, что в Supabase выполнен актуальный блок Storage из supabase_schema.sql."
            )
        if "bucket" in msg and ("not found" in msg or "does not exist" in msg):
            return "Бакет listing-images не найден. Создайте его в Supabase (см. supabase_schema.sql)."
        if exc.message:
            return f"Не удалось загрузить фото: {exc.message}"
    text = str(exc).strip()
    if text:
        return f"Не удалось загрузить фото: {text[:200]}"
    return "Не удалось загрузить фото. Попробуйте ещё раз или выберите другой файл."


def _optional_lat_lng_from_form(lat_s: str, lng_s: str) -> tuple[float | None, float | None] | str:
    """Return (lat, lng) or (None, None) if empty; otherwise an error message string."""
    a = (lat_s or "").strip().replace(",", ".")
    b = (lng_s or "").strip().replace(",", ".")
    if not a and not b:
        return (None, None)
    if not a or not b:
        return "Укажите и широту, и долготу, или оставьте оба поля пустыми."
    try:
        lat = float(a)
        lng = float(b)
    except ValueError:
        return "Широта и долгота должны быть числами (например 41.31 и 69.28)."
    if not (40.8 <= lat <= 42.2 and 68.0 <= lng <= 70.5):
        return "Координаты вне допустимого региона (ожидается территория вокруг Ташкента)."
    return (lat, lng)


def _row_float_or_none(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


async def _read_upload_bytes(upload: rx.UploadFile) -> bytes:
    # Reflex may set path to the original filename only, not a temp path — then Path().read_bytes() fails.
    if upload.path is not None:
        p = Path(upload.path)
        if p.is_file():
            return p.read_bytes()
    await upload.seek(0)
    return await upload.read()


class Listing(BaseModel):
    id: int
    title: str
    district: str
    rooms: int
    price: int
    owner_id: str = ""
    image_url: str = ""
    latitude: float | None = None
    longitude: float | None = None


class ListingState(rx.State):
    """Listings state backed by Supabase table `listings`."""

    listings: list[Listing] = [
        Listing(
            id=1,
            title="Уютная 1-комнатная квартира",
            district="Юнусабад",
            rooms=1,
            price=3500000,
            image_url="",
            latitude=41.33,
            longitude=69.29,
        ),
        Listing(
            id=2,
            title="2-комнатная рядом с метро",
            district="Чиланзар",
            rooms=2,
            price=4800000,
            image_url="",
            latitude=41.28,
            longitude=69.22,
        ),
    ]
    title: str = ""
    district: str = ""
    rooms: int = 1
    price: int = 0
    search_query: str = ""
    filter_district: str = ""
    min_price: int = 0
    max_price: int = 0
    min_rooms: int = 0
    max_rooms: int = 0
    sort_by: str = "newest"
    listings_page: int = 1
    error_message: str = ""
    success_message: str = ""
    my_listings: list[Listing] = []
    favorite_listing_ids: list[int] = []
    edit_listing_id: int = 0
    edit_title: str = ""
    edit_district: str = ""
    edit_rooms: int = 1
    edit_price: int = 0
    pending_image_url: str = ""
    pending_image_name: str = ""
    edit_image_url: str = ""
    edit_image_url_before_upload: str = ""
    create_latitude: str = ""
    create_longitude: str = ""
    edit_latitude: str = ""
    edit_longitude: str = ""
    detail_id: int = 0
    detail_title: str = ""
    detail_district: str = ""
    detail_rooms: int = 1
    detail_price: int = 0
    detail_owner_id: str = ""
    detail_image_url: str = ""
    detail_has_location: bool = False

    def _clear_listing_detail(self) -> None:
        self.detail_id = 0
        self.detail_title = ""
        self.detail_district = ""
        self.detail_rooms = 1
        self.detail_price = 0
        self.detail_owner_id = ""
        self.detail_image_url = ""
        self.detail_has_location = False

    def load_listing_detail(self) -> None:
        """Load one listing for `/listing/[listing_id]` from router params."""
        self.error_message = ""
        raw = (self.router.page.params.get("listing_id") or "").strip()
        if not raw.isdigit():
            self._clear_listing_detail()
            return
        listing_id = int(raw)
        sb = get_supabase()
        if sb is None:
            self._clear_listing_detail()
            self.error_message = "Supabase не настроен. Проверьте .env."
            return
        try:
            response = (
                sb.table("listings")
                .select(
                    "id,title,district,rooms,price,owner_id,image_url,latitude,longitude"
                )
                .eq("id", listing_id)
                .limit(1)
                .execute()
            )
            rows = getattr(response, "data", []) or []
            if not rows:
                self._clear_listing_detail()
                return
            row = rows[0]
            self.detail_id = int(row.get("id", 0))
            self.detail_title = str(row.get("title", "") or "")
            self.detail_district = str(row.get("district", "") or "")
            self.detail_rooms = int(row.get("rooms", 1) or 1)
            self.detail_price = int(row.get("price", 0) or 0)
            self.detail_owner_id = str(row.get("owner_id", "") or "")
            self.detail_image_url = str(row.get("image_url") or "")
            self.detail_has_location = row.get("latitude") is not None and row.get(
                "longitude"
            ) is not None
        except Exception:
            self._clear_listing_detail()
            self.error_message = "Не удалось загрузить объявление."

    def _upload_listing_image_bytes(
        self,
        sb: Any,
        user_id: str,
        data: bytes,
        original_name: str | None,
    ) -> str:
        raw = (original_name or "photo.jpg").rsplit(".", 1)
        ext = f".{raw[-1].lower()}" if len(raw) > 1 else ".jpg"
        if ext not in _ALLOWED_IMAGE_EXT:
            ext = ".jpg"
        path = f"{user_id}/{uuid.uuid4().hex}{ext}"
        content_type = _content_type_for_ext(ext)
        _ensure_supabase_storage_uses_current_jwt(sb)
        sb.storage.from_(LISTING_IMAGES_BUCKET).upload(
            path,
            data,
            file_options={"content-type": content_type, "upsert": "true"},
        )
        return sb.storage.from_(LISTING_IMAGES_BUCKET).get_public_url(path)

    def _is_current_user_blocked(self) -> bool:
        sb = get_supabase()
        if sb is None:
            return False
        try:
            user = getattr(sb.auth.get_user(), "user", None)
            if user is None or not getattr(user, "id", None):
                return False
            row = (
                sb.table("profiles")
                .select("is_blocked")
                .eq("id", user.id)
                .limit(1)
                .execute()
                .data
                or []
            )
            if not row:
                return False
            return bool(row[0].get("is_blocked", False))
        except Exception:
            return False

    def set_title(self, value: str) -> None:
        self.title = value

    def set_district(self, value: str) -> None:
        self.district = value

    def set_rooms(self, value: str) -> None:
        self.rooms = int(value) if value else 1

    def set_price(self, value: str) -> None:
        self.price = int(value) if value else 0

    def set_create_latitude(self, value: str) -> None:
        self.create_latitude = value

    def set_create_longitude(self, value: str) -> None:
        self.create_longitude = value

    def set_edit_latitude(self, value: str) -> None:
        self.edit_latitude = value

    def set_edit_longitude(self, value: str) -> None:
        self.edit_longitude = value

    def set_search_query(self, value: str) -> None:
        self.search_query = value
        self.listings_page = 1

    def set_filter_district(self, value: str) -> None:
        self.filter_district = value
        self.listings_page = 1

    def set_min_price(self, value: str) -> None:
        self.min_price = int(value) if value else 0
        self.listings_page = 1

    def set_max_price(self, value: str) -> None:
        self.max_price = int(value) if value else 0
        self.listings_page = 1

    def set_min_rooms(self, value: str) -> None:
        self.min_rooms = int(value) if value else 0
        self.listings_page = 1

    def set_max_rooms(self, value: str) -> None:
        self.max_rooms = int(value) if value else 0
        self.listings_page = 1

    def reset_filters(self) -> None:
        self.search_query = ""
        self.filter_district = ""
        self.min_price = 0
        self.max_price = 0
        self.min_rooms = 0
        self.max_rooms = 0
        self.sort_by = "newest"
        self.listings_page = 1

    def set_sort_by(self, value: str) -> None:
        self.sort_by = value
        self.listings_page = 1

    def listings_prev_page(self) -> None:
        if self.listings_page > 1:
            self.listings_page -= 1

    def listings_next_page(self) -> None:
        if self.listings_page < self._listings_total_pages_int():
            self.listings_page += 1

    def set_edit_title(self, value: str) -> None:
        self.edit_title = value

    def set_edit_district(self, value: str) -> None:
        self.edit_district = value

    def set_edit_rooms(self, value: str) -> None:
        self.edit_rooms = int(value) if value else 1

    def set_edit_price(self, value: str) -> None:
        self.edit_price = int(value) if value else 0

    def start_edit(self, listing_id: int) -> None:
        target = next((item for item in self.my_listings if item.id == listing_id), None)
        if target is None:
            self.error_message = "Объявление не найдено."
            return
        self.edit_listing_id = target.id
        self.edit_title = target.title
        self.edit_district = target.district
        self.edit_rooms = target.rooms
        self.edit_price = target.price
        self.edit_image_url = target.image_url or ""
        self.edit_image_url_before_upload = self.edit_image_url
        self.edit_latitude = (
            str(target.latitude) if target.latitude is not None else ""
        )
        self.edit_longitude = (
            str(target.longitude) if target.longitude is not None else ""
        )
        self.error_message = ""

    def cancel_edit(self) -> None:
        self.edit_listing_id = 0
        self.edit_title = ""
        self.edit_district = ""
        self.edit_rooms = 1
        self.edit_price = 0
        self.edit_image_url = ""
        self.edit_image_url_before_upload = ""
        self.edit_latitude = ""
        self.edit_longitude = ""

    def render_map_leaflet(self) -> Any:
        markers: list[dict[str, Any]] = []
        for item in self.listings:
            if item.latitude is None or item.longitude is None:
                continue
            markers.append(
                {
                    "id": item.id,
                    "lat": item.latitude,
                    "lng": item.longitude,
                    "title": item.title,
                    "price": format_price_uzs(item.price),
                    "url": f"/listing/{item.id}",
                }
            )
        return rx.call_script(
            f"window.__rentoInitMap({json.dumps(markers, ensure_ascii=True)});"
        )

    async def upload_create_photo(self, files: list[rx.UploadFile]) -> None:
        self.error_message = ""
        if not files:
            return
        sb = get_supabase()
        if sb is None:
            self.error_message = "Supabase не настроен. Проверьте .env."
            return
        user = getattr(sb.auth.get_user(), "user", None)
        if user is None or not getattr(user, "id", None):
            self.error_message = "Войдите в аккаунт, чтобы загрузить фото."
            return
        try:
            data = await _read_upload_bytes(files[0])
            if len(data) > 5_000_000:
                self.error_message = "Файл больше 5 МБ. Выберите другое изображение."
                return
            name = files[0].filename or "photo.jpg"
            url = self._upload_listing_image_bytes(sb, str(user.id), data, name)
            self.pending_image_url = url
            self.pending_image_name = name
        except Exception as exc:
            self.error_message = _humanize_storage_upload_error(exc)

    async def upload_edit_photo(self, files: list[rx.UploadFile]) -> None:
        self.error_message = ""
        if not files or self.edit_listing_id <= 0:
            return
        sb = get_supabase()
        if sb is None:
            self.error_message = "Supabase не настроен. Проверьте .env."
            return
        user = getattr(sb.auth.get_user(), "user", None)
        if user is None or not getattr(user, "id", None):
            self.error_message = "Войдите в аккаунт, чтобы загрузить фото."
            return
        try:
            data = await _read_upload_bytes(files[0])
            if len(data) > 5_000_000:
                self.error_message = "Файл больше 5 МБ. Выберите другое изображение."
                return
            name = files[0].filename or "photo.jpg"
            url = self._upload_listing_image_bytes(sb, str(user.id), data, name)
            self.edit_image_url = url
        except Exception as exc:
            self.error_message = _humanize_storage_upload_error(exc)

    def clear_create_photo(self):
        self.pending_image_url = ""
        self.pending_image_name = ""
        return rx.clear_selected_files("listing-photo-create")

    def clear_edit_photo(self):
        self.edit_image_url = ""
        return rx.clear_selected_files("listing-photo-edit")

    def save_edit(self) -> None:
        if self.edit_listing_id <= 0:
            return
        if not self.edit_title or not self.edit_district or self.edit_price <= 0:
            self.error_message = "Для редактирования заполните все поля корректно."
            return
        sb = get_supabase()
        if sb is None:
            self.error_message = "Supabase не настроен. Проверьте .env."
            return
        try:
            coords = _optional_lat_lng_from_form(self.edit_latitude, self.edit_longitude)
            if isinstance(coords, str):
                self.error_message = coords
                return
            lat, lng = coords
            update_row: dict[str, Any] = {
                "title": self.edit_title,
                "district": self.edit_district,
                "rooms": self.edit_rooms,
                "price": self.edit_price,
                "image_url": self.edit_image_url or None,
            }
            if lat is not None:
                update_row["latitude"] = lat
                update_row["longitude"] = lng
            else:
                update_row["latitude"] = None
                update_row["longitude"] = None
            sb.table("listings").update(update_row).eq("id", self.edit_listing_id).execute()
            self.success_message = "Объявление обновлено."
            self.error_message = ""
            self.cancel_edit()
            self.load_my_listings()
            self.load_listings()
            return rx.clear_selected_files("listing-photo-edit")
        except Exception:
            self.error_message = "Не удалось обновить объявление. Попробуйте еще раз."

    def delete_listing(self, listing_id: int) -> None:
        sb = get_supabase()
        if sb is None:
            self.error_message = "Supabase не настроен. Проверьте .env."
            return
        try:
            sb.table("listings").delete().eq("id", listing_id).execute()
            if self.edit_listing_id == listing_id:
                self.cancel_edit()
            self.success_message = "Объявление удалено."
            self.error_message = ""
            self.load_my_listings()
            self.load_listings()
        except Exception:
            self.error_message = "Не удалось удалить объявление. Попробуйте еще раз."

    def add_listing(self) -> None:
        if not self.title or not self.district or self.price <= 0:
            self.error_message = "Заполните поля: заголовок, район и корректную цену."
            self.success_message = ""
            return
        sb = get_supabase()
        if sb is None:
            self.error_message = "Supabase не настроен. Проверьте .env."
            self.success_message = ""
            return
        try:
            user_response = sb.auth.get_user()
            user = getattr(user_response, "user", None)
            if user is None or not getattr(user, "id", None):
                self.error_message = "Для публикации войдите в аккаунт."
                self.success_message = ""
                return
            if self._is_current_user_blocked():
                self.error_message = "Ваш аккаунт заблокирован. Публикация объявлений недоступна."
                self.success_message = ""
                return
            coords = _optional_lat_lng_from_form(self.create_latitude, self.create_longitude)
            if isinstance(coords, str):
                self.error_message = coords
                self.success_message = ""
                return
            lat, lng = coords
            row: dict[str, Any] = {
                "title": self.title,
                "district": self.district,
                "rooms": self.rooms,
                "price": self.price,
                "owner_id": user.id,
            }
            if self.pending_image_url:
                row["image_url"] = self.pending_image_url
            if lat is not None:
                row["latitude"] = lat
                row["longitude"] = lng
            sb.table("listings").insert(row).execute()
            self.title = ""
            self.district = ""
            self.rooms = 1
            self.price = 0
            self.create_latitude = ""
            self.create_longitude = ""
            self.pending_image_url = ""
            self.pending_image_name = ""
            self.error_message = ""
            self.success_message = "Объявление опубликовано."
            self.load_listings()
            self.load_my_listings()
            return rx.clear_selected_files("listing-photo-create")
        except Exception:
            self.error_message = "Не удалось сохранить объявление. Попробуйте еще раз."
            self.success_message = ""

    def load_listings(self) -> None:
        sb = get_supabase()
        if sb is None:
            self.error_message = "Supabase не настроен. Проверьте .env."
            self.success_message = ""
            return
        try:
            response = (
                sb.table("listings")
                .select(
                    "id,title,district,rooms,price,owner_id,image_url,latitude,longitude"
                )
                .order("id", desc=True)
                .execute()
            )
            rows = getattr(response, "data", []) or []
            self.listings = [
                Listing(
                    id=int(row.get("id", 0)),
                    title=str(row.get("title", "")),
                    district=str(row.get("district", "")),
                    rooms=int(row.get("rooms", 1) or 1),
                    price=int(row.get("price", 0) or 0),
                    owner_id=str(row.get("owner_id", "") or ""),
                    image_url=str(row.get("image_url") or ""),
                    latitude=_row_float_or_none(row.get("latitude")),
                    longitude=_row_float_or_none(row.get("longitude")),
                )
                for row in rows
                if row.get("id") is not None
            ]
            self.error_message = ""
            self.listings_page = 1
            self.load_favorites()
        except Exception:
            self.error_message = "Не удалось загрузить объявления. Обновите страницу."

    def load_my_listings(self) -> None:
        sb = get_supabase()
        if sb is None:
            self.error_message = "Supabase не настроен. Проверьте .env."
            self.success_message = ""
            return
        try:
            user_response = sb.auth.get_user()
            user = getattr(user_response, "user", None)
            if user is None or not getattr(user, "id", None):
                self.my_listings = []
                self.error_message = "Войдите в аккаунт, чтобы видеть свои объявления."
                return
            response = (
                sb.table("listings")
                .select(
                    "id,title,district,rooms,price,owner_id,image_url,latitude,longitude"
                )
                .eq("owner_id", user.id)
                .order("id", desc=True)
                .execute()
            )
            rows = getattr(response, "data", []) or []
            self.my_listings = [
                Listing(
                    id=int(row.get("id", 0)),
                    title=str(row.get("title", "")),
                    district=str(row.get("district", "")),
                    rooms=int(row.get("rooms", 1) or 1),
                    price=int(row.get("price", 0) or 0),
                    owner_id=str(row.get("owner_id", "") or ""),
                    image_url=str(row.get("image_url") or ""),
                    latitude=_row_float_or_none(row.get("latitude")),
                    longitude=_row_float_or_none(row.get("longitude")),
                )
                for row in rows
                if row.get("id") is not None
            ]
            self.error_message = ""
        except Exception:
            self.error_message = "Не удалось загрузить ваши объявления. Обновите страницу."

    def load_favorites(self) -> None:
        sb = get_supabase()
        if sb is None:
            return
        try:
            user_response = sb.auth.get_user()
            user = getattr(user_response, "user", None)
            if user is None or not getattr(user, "id", None):
                self.favorite_listing_ids = []
                return
            response = (
                sb.table("favorites")
                .select("listing_id")
                .eq("user_id", user.id)
                .execute()
            )
            rows = getattr(response, "data", []) or []
            self.favorite_listing_ids = [
                int(row.get("listing_id"))
                for row in rows
                if row.get("listing_id") is not None
            ]
        except Exception:
            self.favorite_listing_ids = []

    def toggle_favorite(self, listing_id: int) -> None:
        sb = get_supabase()
        if sb is None:
            self.error_message = "Supabase не настроен. Проверьте .env."
            return
        try:
            user_response = sb.auth.get_user()
            user = getattr(user_response, "user", None)
            if user is None or not getattr(user, "id", None):
                self.error_message = "Войдите в аккаунт, чтобы добавлять в избранное."
                return
            if listing_id in self.favorite_listing_ids:
                sb.table("favorites").delete().eq("user_id", user.id).eq(
                    "listing_id", listing_id
                ).execute()
            else:
                sb.table("favorites").insert(
                    {"user_id": user.id, "listing_id": listing_id}
                ).execute()
            self.error_message = ""
            self.load_favorites()
        except Exception:
            self.error_message = "Не удалось обновить избранное. Попробуйте еще раз."

    def _filtered_listings_core(self) -> list[Listing]:
        query = self.search_query.strip().lower()
        district_query = self.filter_district.strip().lower()
        result: list[Listing] = []
        for item in self.listings:
            if query and query not in item.title.lower() and query not in item.district.lower():
                continue
            if district_query and district_query not in item.district.lower():
                continue
            if self.min_price > 0 and item.price < self.min_price:
                continue
            if self.max_price > 0 and item.price > self.max_price:
                continue
            if self.min_rooms > 0 and item.rooms < self.min_rooms:
                continue
            if self.max_rooms > 0 and item.rooms > self.max_rooms:
                continue
            result.append(item)
        if self.sort_by == "price_asc":
            return sorted(result, key=lambda item: item.price)
        if self.sort_by == "price_desc":
            return sorted(result, key=lambda item: item.price, reverse=True)
        if self.sort_by == "rooms_desc":
            return sorted(result, key=lambda item: item.rooms, reverse=True)
        return sorted(result, key=lambda item: item.id, reverse=True)

    def _listings_total_pages_int(self) -> int:
        n = len(self._filtered_listings_core())
        if n == 0:
            return 1
        return (n + LISTINGS_PAGE_SIZE - 1) // LISTINGS_PAGE_SIZE

    @rx.var(cache=False)
    def is_editing(self) -> bool:
        return self.edit_listing_id > 0

    @rx.var(cache=False)
    def filtered_listings(self) -> list[Listing]:
        return self._filtered_listings_core()

    @rx.var(cache=False)
    def paginated_filtered_listings(self) -> list[Listing]:
        full = self._filtered_listings_core()
        tp = self._listings_total_pages_int()
        page = min(max(1, self.listings_page), tp)
        start = (page - 1) * LISTINGS_PAGE_SIZE
        return full[start : start + LISTINGS_PAGE_SIZE]

    @rx.var(cache=False)
    def listings_filtered_count(self) -> int:
        return len(self._filtered_listings_core())

    @rx.var(cache=False)
    def listings_total_pages(self) -> int:
        return self._listings_total_pages_int()

    @rx.var(cache=False)
    def favorite_listings(self) -> list[Listing]:
        favorite_ids = set(self.favorite_listing_ids)
        return [item for item in self.listings if item.id in favorite_ids]

    @rx.var(cache=False)
    def has_filtered_listings(self) -> bool:
        return len(self._filtered_listings_core()) > 0
