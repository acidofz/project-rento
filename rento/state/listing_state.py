from pydantic import BaseModel
import reflex as rx

from rento.supabase_client import get_supabase


class Listing(BaseModel):
    id: int
    title: str
    district: str
    rooms: int
    price: int
    owner_id: str = ""


class ListingState(rx.State):
    """Listings state backed by Supabase table `listings`."""

    listings: list[Listing] = [
        Listing(id=1, title="Уютная 1-комнатная квартира", district="Юнусабад", rooms=1, price=3500000),
        Listing(id=2, title="2-комнатная рядом с метро", district="Чиланзар", rooms=2, price=4800000),
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
    error_message: str = ""
    success_message: str = ""
    my_listings: list[Listing] = []
    favorite_listing_ids: list[int] = []
    edit_listing_id: int = 0
    edit_title: str = ""
    edit_district: str = ""
    edit_rooms: int = 1
    edit_price: int = 0

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

    def set_search_query(self, value: str) -> None:
        self.search_query = value

    def set_filter_district(self, value: str) -> None:
        self.filter_district = value

    def set_min_price(self, value: str) -> None:
        self.min_price = int(value) if value else 0

    def set_max_price(self, value: str) -> None:
        self.max_price = int(value) if value else 0

    def set_min_rooms(self, value: str) -> None:
        self.min_rooms = int(value) if value else 0

    def set_max_rooms(self, value: str) -> None:
        self.max_rooms = int(value) if value else 0

    def reset_filters(self) -> None:
        self.search_query = ""
        self.filter_district = ""
        self.min_price = 0
        self.max_price = 0
        self.min_rooms = 0
        self.max_rooms = 0
        self.sort_by = "newest"

    def set_sort_by(self, value: str) -> None:
        self.sort_by = value

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
        self.error_message = ""

    def cancel_edit(self) -> None:
        self.edit_listing_id = 0
        self.edit_title = ""
        self.edit_district = ""
        self.edit_rooms = 1
        self.edit_price = 0

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
            sb.table("listings").update(
                {
                    "title": self.edit_title,
                    "district": self.edit_district,
                    "rooms": self.edit_rooms,
                    "price": self.edit_price,
                }
            ).eq("id", self.edit_listing_id).execute()
            self.success_message = "Объявление обновлено."
            self.error_message = ""
            self.cancel_edit()
            self.load_my_listings()
            self.load_listings()
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
            sb.table("listings").insert(
                {
                    "title": self.title,
                    "district": self.district,
                    "rooms": self.rooms,
                    "price": self.price,
                    "owner_id": user.id,
                }
            ).execute()
            self.title = ""
            self.district = ""
            self.rooms = 1
            self.price = 0
            self.error_message = ""
            self.success_message = "Объявление опубликовано."
            self.load_listings()
            self.load_my_listings()
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
                .select("id,title,district,rooms,price,owner_id")
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
                )
                for row in rows
                if row.get("id") is not None
            ]
            self.error_message = ""
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
                .select("id,title,district,rooms,price,owner_id")
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

    @rx.var(cache=False)
    def is_editing(self) -> bool:
        return self.edit_listing_id > 0

    @rx.var(cache=False)
    def filtered_listings(self) -> list[Listing]:
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

    @rx.var(cache=False)
    def favorite_listings(self) -> list[Listing]:
        favorite_ids = set(self.favorite_listing_ids)
        return [item for item in self.listings if item.id in favorite_ids]

    @rx.var(cache=False)
    def has_filtered_listings(self) -> bool:
        return len(self.filtered_listings) > 0
