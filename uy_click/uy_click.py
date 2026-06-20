import reflex as rx

from uy_click.pages.admin import admin
from uy_click.pages.create import create
from uy_click.pages.favorites import favorites
from uy_click.pages.health import health
from uy_click.pages.index import index
from uy_click.pages.listing_detail import listing_detail
from uy_click.pages.map_page import map_page
from uy_click.pages.listings import listings
from uy_click.pages.login import login
from uy_click.pages.my_listings import my_listings
from uy_click.pages.privacy import privacy
from uy_click.pages.profile import profile
from uy_click.pages.register import register
from uy_click.pages.monetization import monetization
from uy_click.pages.terms import terms
from uy_click.state.listing_state import ListingState
from uy_click.state.admin_state import AdminState
from uy_click.state.auth_state import AuthState
from uy_click.ready_layer import build_api_transformer

SITE_URL = "https://uy-click.uz"
SITE_OG_IMAGE = f"{SITE_URL}/icon.svg"

app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="medium",
        accent_color="teal",
    ),
    api_transformer=build_api_transformer(),
    head_components=[
        rx.el.meta(name="theme-color", content="#0d9488"),
        rx.el.meta(name="robots", content="index, follow"),
        rx.el.meta(property="og:site_name", content="UY-CLICK"),
        rx.el.meta(property="og:locale", content="ru_RU"),
        rx.el.link(
            rel="stylesheet",
            href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
        ),
        rx.el.script(src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"),
    ],
)

app.add_page(
    index,
    route="/",
    title="UY-CLICK — Аренда жилья без посредников в Ташкенте",
    description="Снимайте и сдавайте квартиры по всему Узбекистану напрямую без посредников и комиссий. Найдите жильё в Ташкенте — P2P аренда с картой и избранным.",
    meta=[
        {"property": "og:type", "content": "website"},
        {"property": "og:url", "content": SITE_URL},
        {"property": "og:title", "content": "UY-CLICK — Аренда жилья без посредников в Ташкенте"},
        {"property": "og:description", "content": "Снимайте и сдавайте квартиры по всему Узбекистану напрямую без посредников и комиссий."},
        {"property": "og:image", "content": SITE_OG_IMAGE},
        {"name": "twitter:card", "content": "summary"},
        {"name": "twitter:title", "content": "UY-CLICK — Аренда жилья без посредников"},
        {"name": "twitter:description", "content": "P2P аренда жилья в Узбекистане без комиссий."},
    ],
    on_load=[AuthState.load_current_user_status, ListingState.load_listings],
)
app.add_page(
    login,
    route="/login",
    title="Вход — UY-CLICK",
    description="Войдите в аккаунт UY-CLICK, чтобы сдавать и снимать жильё без посредников.",
    on_load=AuthState.load_current_user_status,
)
app.add_page(
    register,
    route="/register",
    title="Регистрация — UY-CLICK",
    description="Создайте бесплатный аккаунт на UY-CLICK и начните сдавать или снимать жильё без посредников.",
    on_load=AuthState.load_current_user_status,
)
app.add_page(
    listings,
    route="/listings",
    title="Объявления об аренде жилья в Узбекистане — UY-CLICK",
    description="Все объявления об аренде квартир и домов в Ташкенте и по всему Узбекистану. Фильтры по району, цене и количеству комнат.",
    meta=[
        {"property": "og:type", "content": "website"},
        {"property": "og:url", "content": f"{SITE_URL}/listings"},
        {"property": "og:title", "content": "Объявления об аренде жилья — UY-CLICK"},
        {"property": "og:description", "content": "Все объявления аренды квартир в Ташкенте и Узбекистане. Без посредников, без комиссий."},
        {"property": "og:image", "content": SITE_OG_IMAGE},
    ],
    on_load=[AuthState.load_current_user_status, ListingState.load_listings],
)
app.add_page(
    map_page,
    route="/map",
    title="Карта аренды жилья в Ташкенте — UY-CLICK",
    description="Смотрите объявления об аренде квартир на интерактивной карте Ташкента и Узбекистана.",
    on_load=[
        AuthState.load_current_user_status,
        ListingState.load_listings,
        ListingState.render_map_leaflet,
        ListingState.clear_map_focus,
    ],
)
app.add_page(
    listing_detail,
    route="/listing/[listing_id]",
    title=ListingState.listing_detail_page_title,
    description=ListingState.listing_detail_page_description,
    meta=[
        {"property": "og:type", "content": "article"},
        {"property": "og:title", "content": ListingState.listing_detail_page_title},
        {"property": "og:description", "content": ListingState.listing_detail_page_description},
        {"property": "og:image", "content": ListingState.detail_image_url},
    ],
    on_load=[
        AuthState.load_current_user_status,
        ListingState.load_listing_detail,
    ],
)
app.add_page(
    create,
    route="/create",
    title="Подать объявление об аренде — UY-CLICK",
    description="Разместите объявление об аренде квартиры или дома бесплатно. Прямой контакт с арендатором без посредников.",
    on_load=[AuthState.require_login, ListingState.reset_create_form],
)
app.add_page(
    favorites,
    route="/favorites",
    title="Избранное — UY-CLICK",
    description="Сохранённые объявления об аренде жилья.",
    on_load=[AuthState.require_login, ListingState.load_favorite_listings],
)
app.add_page(
    my_listings,
    route="/my-listings",
    title="Мои объявления — UY-CLICK",
    description="Управляйте своими объявлениями об аренде на UY-CLICK.",
    on_load=[AuthState.require_login, ListingState.load_my_listings],
)
app.add_page(
    admin,
    route="/admin",
    title="Админ-панель — UY-CLICK",
    meta=[{"name": "robots", "content": "noindex, nofollow"}],
    on_load=[AuthState.require_login, AdminState.load_admin_dashboard],
)
app.add_page(
    profile,
    route="/profile",
    title="Профиль — UY-CLICK",
    on_load=AuthState.require_login,
)
app.add_page(health, route="/health", title="Health")
app.add_page(
    terms,
    route="/terms",
    title="Правила площадки — UY-CLICK",
    description="Правила использования платформы UY-CLICK для аренды жилья без посредников.",
)
app.add_page(
    privacy,
    route="/privacy",
    title="Персональные данные — UY-CLICK",
    description="Политика конфиденциальности и обработки персональных данных на платформе UY-CLICK.",
)
app.add_page(monetization, route="/monetization", title="Бизнес-модель — UY-CLICK")
