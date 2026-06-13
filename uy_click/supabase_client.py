import os
from typing import Any
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
_SUPABASE_CLIENT: Any | None = None
_SUPABASE_ADMIN_CLIENT: Any | None = None


def _ensure_supabase_in_no_proxy(url: str) -> None:
    """Avoid broken local proxy settings for direct Supabase calls."""
    if not url:
        return
    host = urlparse(url).hostname
    if not host:
        return
    for env_key in ("NO_PROXY", "no_proxy"):
        current = os.getenv(env_key, "")
        entries = [item.strip() for item in current.split(",") if item.strip()]
        if host not in entries:
            entries.append(host)
            os.environ[env_key] = ",".join(entries)


def get_supabase() -> Any:
    """Anon Supabase client for public reads (listings, etc.).

    NEVER call sign_in/sign_up on this client — it is a module-level
    singleton shared across all user sessions. Auth must go through
    get_supabase_authed() instead.
    """
    key = SUPABASE_ANON_KEY or SUPABASE_KEY
    if not SUPABASE_URL or not key:
        return None

    _ensure_supabase_in_no_proxy(SUPABASE_URL)

    global _SUPABASE_CLIENT
    if _SUPABASE_CLIENT is not None:
        return _SUPABASE_CLIENT

    from supabase import create_client

    _SUPABASE_CLIENT = create_client(SUPABASE_URL, key)
    return _SUPABASE_CLIENT


def get_supabase_authed(access_token: str) -> Any:
    """Fresh per-request Supabase client authenticated as the given user.

    Creates a new client on every call with the user's JWT in the
    Authorization header so that Supabase RLS sees the correct identity.
    Never cached — each call gets an isolated client.
    """
    key = SUPABASE_ANON_KEY or SUPABASE_KEY
    if not SUPABASE_URL or not key or not access_token:
        return None

    _ensure_supabase_in_no_proxy(SUPABASE_URL)

    from supabase import create_client, ClientOptions

    return create_client(
        SUPABASE_URL,
        key,
        options=ClientOptions(
            headers={"Authorization": f"Bearer {access_token}"}
        ),
    )


def get_supabase_admin() -> Any:
    """Build a privileged Supabase client for admin moderation."""
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        return None

    _ensure_supabase_in_no_proxy(SUPABASE_URL)

    global _SUPABASE_ADMIN_CLIENT
    if _SUPABASE_ADMIN_CLIENT is not None:
        return _SUPABASE_ADMIN_CLIENT

    from supabase import create_client

    _SUPABASE_ADMIN_CLIENT = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    return _SUPABASE_ADMIN_CLIENT
