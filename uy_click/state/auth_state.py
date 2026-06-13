import reflex as rx

from uy_click.supabase_client import get_supabase, get_supabase_authed


def _humanize_auth_error(exc: Exception, action: str) -> str:
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
    """Auth state backed by Supabase Auth.

    access_token is stored in localStorage so it survives page reloads
    without sharing state across different browser sessions.
    """

    email: str = ""
    password: str = ""
    is_logged_in: bool = False
    user_id: str = ""
    user_name: str = "Гость"
    is_blocked: bool = False
    error_message: str = ""
    # Persisted in localStorage — survives page refresh, isolated per browser tab
    access_token: str = rx.LocalStorage("", name="uy_click_access_token")
    refresh_token: str = rx.LocalStorage("", name="uy_click_refresh_token")

    def _try_refresh_token(self) -> bool:
        if not self.refresh_token:
            return False
        from supabase import create_client
        from uy_click.supabase_client import SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_KEY
        key = SUPABASE_ANON_KEY or SUPABASE_KEY
        if not SUPABASE_URL or not key:
            return False
        try:
            fresh_sb = create_client(SUPABASE_URL, key)
            resp = fresh_sb.auth.refresh_session(self.refresh_token)
            session = getattr(resp, "session", None)
            if session and getattr(session, "access_token", None):
                self.access_token = session.access_token
                self.refresh_token = getattr(session, "refresh_token", "") or ""
                return True
        except Exception:
            pass
        self.refresh_token = ""
        return False

    @staticmethod
    def _upsert_profile(user_id: str, email: str, access_token: str) -> None:
        sb = get_supabase_authed(access_token) if access_token else get_supabase()
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
        if not self.access_token:
            self.is_logged_in = False
            self.user_id = ""
            self.user_name = "Гость"
            self.is_blocked = False
            return
        sb = get_supabase()
        if sb is None:
            return
        try:
            # Validate the stored token against Supabase without using shared session
            user_resp = sb.auth.get_user(jwt=self.access_token)
            user = getattr(user_resp, "user", None)
            if user is None or not getattr(user, "id", None):
                # Token expired — try refresh before giving up
                if self._try_refresh_token():
                    user_resp = sb.auth.get_user(jwt=self.access_token)
                    user = getattr(user_resp, "user", None)
            if user is None or not getattr(user, "id", None):
                self.access_token = ""
                self.refresh_token = ""
                self.is_logged_in = False
                self.user_id = ""
                self.user_name = "Гость"
                self.is_blocked = False
                return
            self.is_logged_in = True
            self.user_id = user.id or ""
            sb_authed = get_supabase_authed(self.access_token)
            if sb_authed is None:
                return
            row = (
                sb_authed.table("profiles")
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
        if len(self.password) < 6:
            self.error_message = "Пароль должен содержать не менее 6 символов."
            return
        # Use a fresh (non-singleton) client so sign_up doesn't pollute the shared anon client
        from supabase import create_client
        from uy_click.supabase_client import SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_KEY
        key = SUPABASE_ANON_KEY or SUPABASE_KEY
        if not SUPABASE_URL or not key:
            self.error_message = "Supabase не настроен. Проверьте .env."
            return
        try:
            fresh_sb = create_client(SUPABASE_URL, key)
            response = fresh_sb.auth.sign_up({"email": self.email, "password": self.password})
            user = getattr(response, "user", None)
            session = getattr(response, "session", None)
            if user is None:
                self.error_message = "Не удалось зарегистрировать пользователя."
                return
            self.user_name = user.email.split("@")[0] if user.email else "Пользователь"
            self.user_id = user.id or ""
            if session is not None:
                self.access_token = getattr(session, "access_token", "") or ""
                self.refresh_token = getattr(session, "refresh_token", "") or ""
                self.is_logged_in = bool(self.access_token)
            else:
                self.is_logged_in = False
            self._upsert_profile(self.user_id, user.email or "", self.access_token)
            if self.is_logged_in:
                self.load_current_user_status()
            self.password = ""
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
        if len(self.password) < 6:
            self.error_message = "Пароль должен содержать не менее 6 символов."
            return
        # Fresh client so login doesn't contaminate the shared anon singleton
        from supabase import create_client
        from uy_click.supabase_client import SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_KEY
        key = SUPABASE_ANON_KEY or SUPABASE_KEY
        if not SUPABASE_URL or not key:
            self.error_message = "Supabase не настроен. Проверьте .env."
            return
        try:
            fresh_sb = create_client(SUPABASE_URL, key)
            response = fresh_sb.auth.sign_in_with_password(
                {"email": self.email, "password": self.password}
            )
            user = getattr(response, "user", None)
            session = getattr(response, "session", None)
            if user is None or session is None:
                self.error_message = "Неверный email или пароль."
                return
            self.access_token = getattr(session, "access_token", "") or ""
            self.refresh_token = getattr(session, "refresh_token", "") or ""
            self.user_name = user.email.split("@")[0] if user.email else "Пользователь"
            self.user_id = user.id or ""
            self.is_logged_in = bool(self.access_token)
            self._upsert_profile(self.user_id, user.email or "", self.access_token)
            self.load_current_user_status()
            self.password = ""
            self.error_message = ""
        except Exception as exc:
            self.error_message = _humanize_auth_error(exc, "входа")

    def logout(self) -> None:
        if self.access_token:
            try:
                from uy_click.supabase_client import get_supabase_authed
                sb = get_supabase_authed(self.access_token)
                if sb is not None:
                    sb.auth.sign_out()
            except Exception:
                pass
        self.access_token = ""
        self.refresh_token = ""
        self.is_logged_in = False
        self.user_id = ""
        self.user_name = "Гость"
        self.is_blocked = False
        self.email = ""
        self.password = ""

    def require_login(self):
        self.load_current_user_status()
        if not self.is_logged_in:
            return rx.redirect("/login")
