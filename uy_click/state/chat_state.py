import asyncio
from pydantic import BaseModel
import reflex as rx
import time

from uy_click.supabase_client import get_supabase


class ChatSummary(BaseModel):
    id: int
    created_by: str
    peer_user_id: str = ""
    peer_label: str = "Пользователь"
    created_at: str = ""
    created_at_label: str = ""


class ChatMessage(BaseModel):
    id: int
    chat_id: int
    sender_id: str
    sender_label: str = "Пользователь"
    body: str
    created_at: str = ""
    created_at_label: str = ""


class QuickContact(BaseModel):
    user_id: str
    label: str


class ChatState(rx.State):
    chats: list[ChatSummary] = []
    selected_chat_id: int = 0
    messages: list[ChatMessage] = []
    new_message: str = ""
    peer_user_id: str = ""
    error_message: str = ""
    success_message: str = ""
    current_user_id: str = ""
    user_labels: dict[str, str] = {}
    quick_contacts: list[QuickContact] = []
    _n_chat_poll_tasks: int = 0

    @staticmethod
    def _normalized_route_path(path: str | None) -> str:
        p = (path or "").split("?", 1)[0].strip()
        if not p:
            return "/"
        return p.rstrip("/") or "/"

    @rx.event
    def start_chat_message_poll(self):
        """Запускает один фоновый опрос сообщений, пока открыта страница «Чаты»."""
        return ChatState.poll_chat_messages_background

    @rx.event(background=True)
    async def poll_chat_messages_background(self):
        async with self:
            if self._n_chat_poll_tasks > 0:
                return
            self._n_chat_poll_tasks += 1
        try:
            while True:
                async with self:
                    route = self._normalized_route_path(self.router.page.path)
                    if route != "/chats" or self.selected_chat_id <= 0:
                        return
                    self.load_messages()
                await asyncio.sleep(6)
        finally:
            async with self:
                self._n_chat_poll_tasks = max(0, self._n_chat_poll_tasks - 1)

    def _is_user_blocked(self) -> bool:
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

    @staticmethod
    def _format_timestamp(value: str) -> str:
        if not value:
            return ""
        # Expecting ISO from Supabase: 2026-04-08T12:34:56.000+00:00
        return value.replace("T", " ")[:16]

    @staticmethod
    def _with_retry(func, attempts: int = 3, delay_sec: float = 0.4):
        last_exc: Exception | None = None
        for attempt in range(attempts):
            try:
                return func()
            except Exception as exc:
                last_exc = exc
                if attempt < attempts - 1:
                    time.sleep(delay_sec)
                else:
                    raise
        if last_exc is not None:
            raise last_exc

    def set_new_message(self, value: str) -> None:
        self.new_message = value

    def load_chats(self) -> None:
        sb = get_supabase()
        if sb is None:
            self.error_message = "Supabase не настроен. Проверьте .env."
            return
        try:
            user = getattr(sb.auth.get_user(), "user", None)
            if user is None or not getattr(user, "id", None):
                self.error_message = "Войдите в аккаунт, чтобы использовать чат."
                self.chats = []
                return
            self.current_user_id = user.id
            member_rows = self._with_retry(
                lambda: (
                    sb.table("chat_members")
                    .select("chat_id")
                    .eq("user_id", user.id)
                    .execute()
                    .data
                    or []
                )
            )
            chat_ids = [row.get("chat_id") for row in member_rows if row.get("chat_id") is not None]
            if not chat_ids:
                self.chats = []
                self.selected_chat_id = 0
                self.messages = []
                self.error_message = ""
                return
            all_members = self._with_retry(
                lambda: (
                    sb.table("chat_members")
                    .select("chat_id,user_id")
                    .in_("chat_id", chat_ids)
                    .execute()
                    .data
                    or []
                )
            )
            peer_by_chat_id: dict[int, str] = {}
            user_ids: set[str] = set()
            for row in all_members:
                chat_id = int(row.get("chat_id", 0) or 0)
                member_user_id = str(row.get("user_id", "") or "")
                if chat_id <= 0 or not member_user_id:
                    continue
                user_ids.add(member_user_id)
                if member_user_id != user.id:
                    peer_by_chat_id[chat_id] = member_user_id
            self._load_user_labels(user_ids)
            rows = self._with_retry(
                lambda: (
                    sb.table("chats")
                    .select("id,created_by,created_at")
                    .in_("id", chat_ids)
                    .order("id", desc=True)
                    .execute()
                    .data
                    or []
                )
            )
            self.chats = [
                ChatSummary(
                    id=int(row.get("id", 0)),
                    created_by=str(row.get("created_by", "") or ""),
                    peer_user_id=peer_by_chat_id.get(int(row.get("id", 0) or 0), ""),
                    peer_label=self.user_labels.get(
                        peer_by_chat_id.get(int(row.get("id", 0) or 0), ""),
                        "Пользователь",
                    ),
                    created_at=str(row.get("created_at", "") or ""),
                    created_at_label=self._format_timestamp(
                        str(row.get("created_at", "") or "")
                    ),
                )
                for row in rows
                if row.get("id") is not None
            ]
            if self.chats and self.selected_chat_id == 0:
                self.selected_chat_id = self.chats[0].id
                self.load_messages()
            self.load_quick_contacts()
            self.error_message = ""
        except Exception:
            self.error_message = "Не удалось загрузить чаты. Обновите страницу."

    def select_chat(self, chat_id: int) -> None:
        self.selected_chat_id = chat_id
        self.load_messages()

    def load_messages(self) -> None:
        if self.selected_chat_id <= 0:
            self.messages = []
            return
        sb = get_supabase()
        if sb is None:
            self.error_message = "Supabase не настроен. Проверьте .env."
            return
        try:
            rows = self._with_retry(
                lambda: (
                    sb.table("messages")
                    .select("id,chat_id,sender_id,body,created_at")
                    .eq("chat_id", self.selected_chat_id)
                    .order("id", desc=False)
                    .execute()
                    .data
                    or []
                )
            )
            sender_ids = {
                str(row.get("sender_id", "") or "")
                for row in rows
                if row.get("sender_id")
            }
            self._load_user_labels(sender_ids)
            self.messages = [
                ChatMessage(
                    id=int(row.get("id", 0)),
                    chat_id=int(row.get("chat_id", 0)),
                    sender_id=str(row.get("sender_id", "") or ""),
                    sender_label=self.user_labels.get(
                        str(row.get("sender_id", "") or ""), "Пользователь"
                    ),
                    body=str(row.get("body", "") or ""),
                    created_at=str(row.get("created_at", "") or ""),
                    created_at_label=self._format_timestamp(
                        str(row.get("created_at", "") or "")
                    ),
                )
                for row in rows
                if row.get("id") is not None
            ]
            self.error_message = ""
        except Exception:
            self.error_message = "Не удалось загрузить сообщения. Обновите страницу."

    def create_chat(self) -> None:
        if not self.peer_user_id:
            self.error_message = "Выберите контакт для старта чата."
            return
        sb = get_supabase()
        if sb is None:
            self.error_message = "Supabase не настроен. Проверьте .env."
            return
        try:
            user = getattr(sb.auth.get_user(), "user", None)
            if user is None or not getattr(user, "id", None):
                self.error_message = "Войдите в аккаунт, чтобы создать чат."
                return
            if self._is_user_blocked():
                self.error_message = "Ваш аккаунт заблокирован. Создание чатов недоступно."
                return
            if self.peer_user_id == user.id:
                self.error_message = "Нельзя создать чат с самим собой."
                return
            existing_chat_id = self._find_existing_chat_id(user.id, self.peer_user_id)
            if existing_chat_id > 0:
                self.selected_chat_id = existing_chat_id
                self.success_message = "Открыт существующий чат."
                self.error_message = ""
                self.load_chats()
                self.load_messages()
                return
            chat_row = self._with_retry(
                lambda: (
                    sb.table("chats")
                    .insert({"created_by": user.id})
                    .execute()
                    .data
                    or []
                )
            )
            if chat_row:
                chat_id = int(chat_row[0].get("id"))
            else:
                latest_chat_rows = self._with_retry(
                    lambda: (
                        sb.table("chats")
                        .select("id")
                        .eq("created_by", user.id)
                        .order("id", desc=True)
                        .limit(1)
                        .execute()
                        .data
                        or []
                    )
                )
                if not latest_chat_rows:
                    self.error_message = "Не удалось определить созданный чат."
                    return
                chat_id = int(latest_chat_rows[0].get("id", 0))
            if chat_id <= 0:
                self.error_message = "Не удалось создать чат."
                return
            self._with_retry(
                lambda: sb.table("chat_members")
                .insert(
                    [
                        {"chat_id": chat_id, "user_id": user.id},
                        {"chat_id": chat_id, "user_id": self.peer_user_id},
                    ],
                    returning="minimal",
                )
                .execute()
            )
            self.success_message = "Чат создан."
            self.error_message = ""
            self.peer_user_id = ""
            self.selected_chat_id = chat_id
            self.load_chats()
            self.load_messages()
        except Exception:
            self.error_message = "Не удалось создать чат. Попробуйте еще раз."

    def _find_existing_chat_id(self, current_user_id: str, peer_user_id: str) -> int:
        sb = get_supabase()
        if sb is None:
            return 0
        rows = (
            self._with_retry(
                lambda: (
                    sb.table("chat_members")
                    .select("chat_id,user_id")
                    .in_("user_id", [current_user_id, peer_user_id])
                    .execute()
                    .data
                    or []
                )
            )
            or []
        )
        my_chats: set[int] = set()
        peer_chats: set[int] = set()
        for row in rows:
            chat_id = int(row.get("chat_id", 0) or 0)
            uid = str(row.get("user_id", "") or "")
            if chat_id <= 0:
                continue
            if uid == current_user_id:
                my_chats.add(chat_id)
            elif uid == peer_user_id:
                peer_chats.add(chat_id)
        common = sorted(my_chats & peer_chats, reverse=True)
        return common[0] if common else 0

    def _load_user_labels(self, user_ids: set[str]) -> None:
        if not user_ids:
            return
        sb = get_supabase()
        if sb is None:
            return
        try:
            rows = (
                self._with_retry(
                    lambda: (
                        sb.table("profiles")
                        .select("id,username,email")
                        .in_("id", list(user_ids))
                        .execute()
                        .data
                        or []
                    )
                )
                or []
            )
            labels = dict(self.user_labels)
            for row in rows:
                uid = str(row.get("id", "") or "")
                username = str(row.get("username", "") or "").strip()
                email = str(row.get("email", "") or "").strip()
                if uid:
                    labels[uid] = username or email or f"Пользователь {uid[:8]}"
            for uid in user_ids:
                if uid not in labels:
                    labels[uid] = f"Пользователь {uid[:8]}"
            self.user_labels = labels
        except Exception:
            pass

    def load_quick_contacts(self) -> None:
        sb = get_supabase()
        if sb is None:
            return
        try:
            user = getattr(sb.auth.get_user(), "user", None)
            if user is None or not getattr(user, "id", None):
                self.quick_contacts = []
                return
            listing_rows = (
                self._with_retry(
                    lambda: (
                        sb.table("listings")
                        .select("owner_id")
                        .execute()
                        .data
                        or []
                    )
                )
                or []
            )
            owner_ids = {
                str(row.get("owner_id", "") or "")
                for row in listing_rows
                if row.get("owner_id") and str(row.get("owner_id")) != user.id
            }
            # Add peers from existing chats too.
            peer_ids = {chat.peer_user_id for chat in self.chats if chat.peer_user_id}
            user_ids = owner_ids.union(peer_ids)
            self._load_user_labels(user_ids)
            self.quick_contacts = [
                QuickContact(
                    user_id=uid,
                    label=self.user_labels.get(uid, f"Пользователь {uid[:8]}"),
                )
                for uid in sorted(user_ids)
            ]
        except Exception:
            self.quick_contacts = []

    def create_chat_with_user(self, peer_user_id: str):
        self.peer_user_id = (peer_user_id or "").strip()
        if not self.peer_user_id:
            self.error_message = "У этого объявления нет контакта владельца."
            return
        self.create_chat()
        if not self.error_message and self.selected_chat_id > 0:
            return rx.redirect("/chats")

    def send_message(self) -> None:
        text = self.new_message.strip()
        if self.selected_chat_id <= 0:
            self.error_message = "Выберите чат."
            return
        if not text:
            self.error_message = "Введите сообщение."
            return
        if len(text) > 2000:
            self.error_message = "Сообщение слишком длинное (максимум 2000 символов)."
            return
        sb = get_supabase()
        if sb is None:
            self.error_message = "Supabase не настроен. Проверьте .env."
            return
        try:
            user = getattr(sb.auth.get_user(), "user", None)
            if user is None or not getattr(user, "id", None):
                self.error_message = "Войдите в аккаунт, чтобы отправлять сообщения."
                return
            if self._is_user_blocked():
                self.error_message = "Ваш аккаунт заблокирован. Отправка сообщений недоступна."
                return
            self._with_retry(
                lambda: sb.table("messages")
                .insert(
                    {
                        "chat_id": self.selected_chat_id,
                        "sender_id": user.id,
                        "body": text,
                    },
                    returning="minimal",
                )
                .execute()
            )
            self.new_message = ""
            self.error_message = ""
            self.load_messages()
        except Exception:
            self.error_message = "Не удалось отправить сообщение. Попробуйте еще раз."
