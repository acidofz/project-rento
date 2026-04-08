import reflex as rx

from rento.pages.admin import admin
from rento.pages.create import create
from rento.pages.chats import chats
from rento.pages.favorites import favorites
from rento.pages.health import health
from rento.pages.index import index
from rento.pages.listings import listings
from rento.pages.login import login
from rento.pages.my_listings import my_listings
from rento.pages.profile import profile
from rento.pages.register import register
from rento.state.listing_state import ListingState
from rento.state.chat_state import ChatState
from rento.state.admin_state import AdminState
from rento.state.auth_state import AuthState

app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="medium",
        accent_color="indigo",
    ),
    head_components=[
        rx.el.link(rel="manifest", href="/manifest.webmanifest"),
        rx.el.meta(name="theme-color", content="#4f46e5"),
    ],
)

app.add_page(index, route="/", title="RENTO")
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
    create,
    route="/create",
    title="Создать объявление",
    on_load=AuthState.load_current_user_status,
)
app.add_page(
    chats,
    route="/chats",
    title="Чаты",
    on_load=[AuthState.load_current_user_status, ChatState.load_chats],
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
