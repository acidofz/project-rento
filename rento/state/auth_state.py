import reflex as rx

from rento.supabase_client import get_supabase


def _humanize_auth_error(exc: Exception, action: str) -> str:
    """Map common Supabase auth errors to actionable user messages."""
    text = str(exc).lower()
    if "email rate limit exceeded" in text:
        return (
            "Слишком много попыток регистрации за короткое время. "
            "Подождите 1-5 минут или войдите в уже созданный аккаунт."
        )
    if "invalid login credentials" in text:
        return "Неверный email или пароль."
    if "email not confirmed" in text:
        return "Подтвердите email в письме от Supabase и повторите вход."
    return f"Не удалось выполнить {action}. Проверьте данные и попробуйте снова."


class AuthState(rx.State):
    """Auth state backed by Supabase Auth."""

    email: str = ""
    password: str = ""
    is_logged_in: bool = False
    user_id: str = ""
    user_name: str = "Гость"
    is_blocked: bool = False
    error_message: str = ""

    @staticmethod
    def _upsert_profile(user_id: str, email: str) -> None:
        sb = get_supabase()
        if sb is None or not user_id:
            return
        username = (email.split("@")[0] if email else "").strip() or "user"
        try:
            sb.table("profiles").upsert(
                {"id": user_id, "email": email, "username": username},
                on_conflict="id",
            ).execute()
        except Exception:
            pass

    def load_current_user_status(self) -> None:
        sb = get_supabase()
        if sb is None:
            return
        try:
            user = getattr(sb.auth.get_user(), "user", None)
            if user is None or not getattr(user, "id", None):
                self.is_logged_in = False
                self.user_id = ""
                self.user_name = "Гость"
                self.is_blocked = False
                return
            self.is_logged_in = True
            self.user_id = user.id or ""
            row = (
                sb.table("profiles")
                .select("username,email,is_blocked")
                .eq("id", self.user_id)
                .limit(1)
                .execute()
                .data
                or []
            )
            if row:
                username = str(row[0].get("username", "") or "").strip()
                email = str(row[0].get("email", "") or "").strip()
                self.user_name = username or (email.split("@")[0] if email else self.user_name)
                self.is_blocked = bool(row[0].get("is_blocked", False))
            else:
                self.is_blocked = False
        except Exception:
            pass

    def set_email(self, value: str) -> None:
        self.email = value

    def set_password(self, value: str) -> None:
        self.password = value

    def register(self) -> None:
        if not self.email or not self.password:
            self.error_message = "Заполните email и пароль."
            return
        sb = get_supabase()
        if sb is None:
            self.error_message = "Supabase не настроен. Проверьте .env."
            return
        try:
            response = sb.auth.sign_up({"email": self.email, "password": self.password})
            user = getattr(response, "user", None)
            session = getattr(response, "session", None)
            if user is None:
                self.error_message = "Не удалось зарегистрировать пользователя."
                return
            self.user_name = user.email.split("@")[0] if user.email else "Пользователь"
            self.user_id = user.id or ""
            self._upsert_profile(self.user_id, user.email or "")
            self.is_logged_in = session is not None
            self.load_current_user_status()
            self.error_message = (
                ""
                if self.is_logged_in
                else "Регистрация выполнена. Подтверди email и затем войди."
            )
        except Exception as exc:
            self.error_message = _humanize_auth_error(exc, "регистрации")

    def login(self) -> None:
        if not self.email or not self.password:
            self.error_message = "Введите email и пароль."
            return
        sb = get_supabase()
        if sb is None:
            self.error_message = "Supabase не настроен. Проверьте .env."
            return
        try:
            response = sb.auth.sign_in_with_password(
                {"email": self.email, "password": self.password}
            )
            user = getattr(response, "user", None)
            if user is None:
                self.error_message = "Неверный email или пароль."
                return
            self.user_name = user.email.split("@")[0] if user.email else "Пользователь"
            self.user_id = user.id or ""
            self._upsert_profile(self.user_id, user.email or "")
            self.is_logged_in = True
            self.load_current_user_status()
            self.error_message = ""
        except Exception as exc:
            self.error_message = _humanize_auth_error(exc, "входа")

    def logout(self) -> None:
        sb = get_supabase()
        if sb is not None:
            try:
                sb.auth.sign_out()
            except Exception:
                pass
        self.is_logged_in = False
        self.user_id = ""
        self.user_name = "Гость"
        self.is_blocked = False
        self.password = ""
