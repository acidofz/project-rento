import os

import reflex as rx

from uy_click.supabase_client import get_supabase, get_supabase_admin


def _admin_ids_from_env() -> set[str]:
    raw = os.getenv("ADMIN_USER_IDS", "")
    return {item.strip() for item in raw.split(",") if item.strip()}


class AdminState(rx.State):
    is_admin: bool = False
    listings_count: int = 0
    chats_count: int = 0
    messages_count: int = 0
    users_count: int = 0
    error_message: str = ""
    success_message: str = ""
    latest_listings: list[dict] = []
    latest_messages: list[dict] = []
    latest_users: list[dict] = []

    def _check_admin(self):
        sb = get_supabase()
        if sb is None:
            self.is_admin = False
            self.error_message = "База не подключена. Проверьте переменные окружения Supabase."
            return None
        user = getattr(sb.auth.get_user(), "user", None)
        if user is None or not getattr(user, "id", None):
            self.is_admin = False
            self.error_message = "Войдите под учётной записью администратора."
            return None
        self.is_admin = user.id in _admin_ids_from_env()
        if not self.is_admin:
            self.error_message = "Недостаточно прав для этой страницы."
            return None
        return user

    def load_admin_dashboard(self) -> None:
        user = self._check_admin()
        if user is None:
            return
        sb_admin = get_supabase_admin()
        if sb_admin is None:
            self.error_message = "Сервисный ключ Supabase не задан — админ-режим недоступен."
            return
        try:
            self.listings_count = (
                sb_admin.table("listings").select("id", count="exact").limit(0).execute().count or 0
            )
            self.chats_count = (
                sb_admin.table("chats").select("id", count="exact").limit(0).execute().count or 0
            )
            self.messages_count = (
                sb_admin.table("messages").select("id", count="exact").limit(0).execute().count or 0
            )
            self.users_count = (
                sb_admin.table("profiles").select("id", count="exact").limit(0).execute().count or 0
            )
            self.latest_listings = (
                sb_admin.table("listings")
                .select("id,title,district,price")
                .order("id", desc=True)
                .limit(8)
                .execute()
                .data
                or []
            )
            self.latest_messages = (
                sb_admin.table("messages")
                .select("id,chat_id,body,sender_id")
                .order("id", desc=True)
                .limit(8)
                .execute()
                .data
                or []
            )
            self.latest_users = (
                sb_admin.table("profiles")
                .select("id,email,username,is_blocked")
                .order("created_at", desc=True)
                .limit(12)
                .execute()
                .data
                or []
            )
            self.error_message = ""
            self.success_message = ""
        except Exception:
            self.error_message = "Не удалось загрузить админ-панель. Обновите страницу."

    def delete_listing_as_admin(self, listing_id: int) -> None:
        if self._check_admin() is None:
            return
        sb_admin = get_supabase_admin()
        if sb_admin is None:
            self.error_message = "Сервисный ключ Supabase не задан — админ-режим недоступен."
            return
        try:
            sb_admin.table("listings").delete().eq("id", listing_id).execute()
            self.success_message = f"Объявление #{listing_id} удалено."
            self.error_message = ""
            self.load_admin_dashboard()
        except Exception:
            self.error_message = "Не удалось удалить объявление. Попробуйте еще раз."

    def delete_message_as_admin(self, message_id: int) -> None:
        if self._check_admin() is None:
            return
        sb_admin = get_supabase_admin()
        if sb_admin is None:
            self.error_message = "Сервисный ключ Supabase не задан — админ-режим недоступен."
            return
        try:
            sb_admin.table("messages").delete().eq("id", message_id).execute()
            self.success_message = f"Сообщение #{message_id} удалено."
            self.error_message = ""
            self.load_admin_dashboard()
        except Exception:
            self.error_message = "Не удалось удалить сообщение. Попробуйте еще раз."

    def set_user_block_status(self, user_id: str, blocked: bool) -> None:
        if self._check_admin() is None:
            return
        sb_admin = get_supabase_admin()
        if sb_admin is None:
            self.error_message = "Сервисный ключ Supabase не задан — админ-режим недоступен."
            return
        try:
            sb_admin.table("profiles").update({"is_blocked": blocked}).eq("id", user_id).execute()
            self.success_message = (
                f"Пользователь {user_id[:8]} {'заблокирован' if blocked else 'разблокирован'}."
            )
            self.error_message = ""
            self.load_admin_dashboard()
        except Exception:
            self.error_message = "Не удалось изменить статус пользователя. Попробуйте еще раз."
