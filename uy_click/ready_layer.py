"""Дополнительные ASGI-маршруты поверх Reflex (см. `api_transformer` в `uy_click.py`)."""

from __future__ import annotations

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route


def ready(_request: Request) -> JSONResponse:
    """Проверка готовности с учётом Supabase (лёгкий SELECT).

    Возвращает 200, если Supabase не настроен (локальная разработка) или запрос прошёл.
    Возвращает 503, если клиент настроен, но БД недоступна.
    """
    from uy_click.supabase_client import get_supabase

    sb = get_supabase()
    if sb is None:
        return JSONResponse(
            {
                "ok": True,
                "supabase": "not_configured",
                "hint": "Set SUPABASE_URL and SUPABASE_ANON_KEY (or SUPABASE_KEY) for a real check.",
            },
            status_code=200,
        )
    try:
        sb.table("listings").select("id").limit(1).execute()
    except Exception:
        return JSONResponse({"ok": False, "supabase": "unreachable"}, status_code=503)
    return JSONResponse({"ok": True, "supabase": "ok"}, status_code=200)


def build_api_transformer() -> Starlette:
    return Starlette(routes=[Route("/ready", endpoint=ready, methods=["GET"])])
