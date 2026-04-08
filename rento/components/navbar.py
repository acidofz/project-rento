import reflex as rx

from rento.state.auth_state import AuthState


def navbar() -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.heading("RENTO", size="6"),
            rx.text("Аренда без посредников", color=rx.color("gray", 10)),
            spacing="3",
            align="center",
        ),
        rx.spacer(),
        rx.hstack(
            rx.link("Главная", href="/"),
            rx.link("Объявления", href="/listings"),
            rx.link("Создать", href="/create"),
            rx.link("Чаты", href="/chats"),
            rx.link("Избранное", href="/favorites"),
            rx.link("Мои объявления", href="/my-listings"),
            rx.link("Профиль", href="/profile"),
            rx.link("Админ", href="/admin"),
            spacing="4",
        ),
        rx.spacer(),
        rx.cond(
            AuthState.is_logged_in,
            rx.hstack(
                rx.text(f"Привет, {AuthState.user_name}"),
                rx.cond(
                    AuthState.is_blocked,
                    rx.badge("Аккаунт заблокирован", color_scheme="red", variant="soft"),
                    rx.fragment(),
                ),
                rx.button("Выйти", on_click=AuthState.logout, variant="soft"),
            ),
            rx.hstack(
                rx.link("Вход", href="/login"),
                rx.link("Регистрация", href="/register"),
                spacing="3",
            ),
        ),
        width="100%",
        padding="1rem",
        border_bottom=f"1px solid {rx.color('gray', 4)}",
        position="sticky",
        top="0",
        bg=rx.color("gray", 1),
        z_index="100",
    )
