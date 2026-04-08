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
    """Build a Supabase client only when credentials exist.

    Priority:
    1) SUPABASE_ANON_KEY (recommended for app usage)
    2) SUPABASE_KEY (legacy fallback)
    3) SUPABASE_SERVICE_ROLE_KEY (server-side only)
    """
    key = SUPABASE_ANON_KEY or SUPABASE_KEY or SUPABASE_SERVICE_ROLE_KEY
    if not SUPABASE_URL or not key:
        return None

    _ensure_supabase_in_no_proxy(SUPABASE_URL)

    global _SUPABASE_CLIENT
    if _SUPABASE_CLIENT is not None:
        return _SUPABASE_CLIENT

    from supabase import create_client

    _SUPABASE_CLIENT = create_client(SUPABASE_URL, key)
    return _SUPABASE_CLIENT


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
