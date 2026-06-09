import reflex as rx

from uy_click.pages.admin import admin
from uy_click.pages.create import create
from uy_click.pages.chats import chats
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
from uy_click.state.chat_state import ChatState
from uy_click.state.admin_state import AdminState
from uy_click.state.auth_state import AuthState
from uy_click.ready_layer import build_api_transformer

app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="medium",
        accent_color="indigo",
    ),
    api_transformer=build_api_transformer(),
    head_components=[
        rx.el.meta(name="theme-color", content="#4f46e5"),
        rx.el.link(
            rel="stylesheet",
            href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
        ),
        rx.el.script(src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"),
    ],
)

app.add_page(index, route="/", title="UY-CLICK")
app.add_page(
    login,
    route="/login",
    title="Вход",
    on_load=AuthState.load_current_user_status,
)
app.add_page(
    register,
    route="/register",
    title="Регистрация",
    on_load=AuthState.load_current_user_status,
)
app.add_page(
    listings,
    route="/listings",
    title="Объявления",
    on_load=[AuthState.load_current_user_status, ListingState.load_listings],
)
app.add_page(
    map_page,
    route="/map",
    title="Карта",
    on_load=[
        AuthState.load_current_user_status,
        ListingState.load_listings,
        ListingState.render_map_leaflet,
    ],
)
app.add_page(
    listing_detail,
    route="/listing/[listing_id]",
    title=ListingState.listing_detail_page_title,
    on_load=[
        AuthState.load_current_user_status,
        ListingState.load_listings,
        ListingState.load_listing_detail,
    ],
)
app.add_page(
    create,
    route="/create",
    title="Создать объявление",
    on_load=AuthState.load_current_user_status,
)
app.add_page(
    chats,
    route="/chats",
    title="Чаты",
    on_load=[
        AuthState.load_current_user_status,
        ChatState.load_chats,
        ChatState.start_chat_message_poll,
    ],
)
app.add_page(
    favorites,
    route="/favorites",
    title="Избранное",
    on_load=[AuthState.load_current_user_status, ListingState.load_listings],
)
app.add_page(
    my_listings,
    route="/my-listings",
    title="Мои объявления",
    on_load=[AuthState.load_current_user_status, ListingState.load_my_listings],
)
app.add_page(
    admin,
    route="/admin",
    title="Админ-панель",
    on_load=[AuthState.load_current_user_status, AdminState.load_admin_dashboard],
)
app.add_page(
    profile,
    route="/profile",
    title="Профиль",
    on_load=AuthState.load_current_user_status,
)
app.add_page(health, route="/health", title="Health")
app.add_page(terms, route="/terms", title="Правила площадки")
app.add_page(privacy, route="/privacy", title="Персональные данные")
app.add_page(monetization, route="/monetization", title="Бизнес-модель")
