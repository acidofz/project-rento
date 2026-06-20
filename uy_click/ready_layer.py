"""Дополнительные ASGI-маршруты поверх Reflex (см. `api_transformer` в `uy_click.py`)."""

from __future__ import annotations

import asyncio
import html as html_lib
import re

from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

SITE_URL = "https://uy-click.uz"
SITE_OG_IMAGE = f"{SITE_URL}/icon.svg"

_BOT_AGENTS = (
    "facebookexternalhit",
    "whatsapp",
    "telegrambot",
    "twitterbot",
    "linkedinbot",
    "slackbot",
    "discordbot",
    "vkshare",
    "okhttp",
)
_LISTING_RE = re.compile(r"^/listing/(\d+)/?$")


def _is_social_bot(user_agent: str) -> bool:
    ua = user_agent.lower()
    return any(bot in ua for bot in _BOT_AGENTS)


def _fetch_listing_sync(listing_id: int) -> dict | None:
    from uy_click.supabase_client import get_supabase

    sb = get_supabase()
    if sb is None:
        return None
    result = (
        sb.table("listings")
        .select("title,district,rooms,price,image_url")
        .eq("id", listing_id)
        .limit(1)
        .execute()
    )
    rows = result.data or []
    return rows[0] if rows else None


def _build_og_html(listing_id: int, row: dict) -> str:
    title = html_lib.escape((row.get("title") or "").strip())
    district = html_lib.escape((row.get("district") or "").strip())
    rooms = int(row.get("rooms") or 1)
    price = int(row.get("price") or 0)
    image_url = (row.get("image_url") or "").strip()

    desc_parts: list[str] = [title] if title else []
    if district:
        desc_parts.append(f"район {district}")
    if rooms:
        desc_parts.append(f"{rooms} комн.")
    if price:
        desc_parts.append(f"{price:,}".replace(",", " ") + " сум/мес")
    desc_parts.append("Аренда напрямую от владельца")
    description = html_lib.escape(" · ".join(desc_parts))

    og_image = html_lib.escape(image_url or SITE_OG_IMAGE)
    og_url = html_lib.escape(f"{SITE_URL}/listing/{listing_id}")
    page_title = html_lib.escape(f"{title} · UY-CLICK" if title else "Объявление · UY-CLICK")

    return (
        "<!DOCTYPE html>\n"
        '<html lang="ru">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        f"<title>{page_title}</title>\n"
        f'<meta name="description" content="{description}">\n'
        f'<meta property="og:type" content="article">\n'
        f'<meta property="og:url" content="{og_url}">\n'
        f'<meta property="og:title" content="{page_title}">\n'
        f'<meta property="og:description" content="{description}">\n'
        f'<meta property="og:image" content="{og_image}">\n'
        f'<meta property="og:site_name" content="UY-CLICK">\n'
        f'<meta name="twitter:card" content="summary_large_image">\n'
        f'<meta name="twitter:title" content="{page_title}">\n'
        f'<meta name="twitter:description" content="{description}">\n'
        f'<meta name="twitter:image" content="{og_image}">\n'
        "</head>\n"
        "<body></body>\n"
        "</html>"
    )


class BotPreviewMiddleware(BaseHTTPMiddleware):
    """Return static OG-tag HTML to social-media crawlers for listing pages.

    Regular browsers get the normal Reflex SPA. Bots get a minimal HTML page
    with proper Open Graph tags so WhatsApp/Telegram previews work correctly.
    """

    async def dispatch(self, request: Request, call_next):
        user_agent = request.headers.get("user-agent", "")
        path = request.url.path
        match = _LISTING_RE.match(path)

        if match and _is_social_bot(user_agent):
            listing_id = int(match.group(1))
            try:
                row = await asyncio.to_thread(_fetch_listing_sync, listing_id)
            except Exception:
                row = None

            if row:
                return Response(
                    _build_og_html(listing_id, row),
                    media_type="text/html; charset=utf-8",
                )

        return await call_next(request)


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
    app = Starlette(routes=[Route("/ready", endpoint=ready, methods=["GET"])])
    app.add_middleware(BotPreviewMiddleware)
    return app
