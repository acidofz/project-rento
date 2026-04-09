import reflex as rx

from rento.components.navbar import navbar
from rento.state.auth_state import AuthState


def profile() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Профиль", size="7"),
                rx.text("Имя в сервисе", size="2", color=rx.color("gray", 10)),
                rx.badge(AuthState.user_name, size="3", color_scheme="blue"),
                rx.text("Вход", size="2", color=rx.color("gray", 10)),
                rx.badge(
                    rx.cond(AuthState.is_logged_in, "Авторизован", "Гость"),
                    color_scheme=rx.cond(AuthState.is_logged_in, "green", "gray"),
                    size="3",
                ),
                rx.cond(
                    AuthState.is_blocked,
                    rx.callout(
                        "Аккаунт заблокирован: чат и новые объявления недоступны.",
                        color_scheme="red",
                    ),
                    rx.fragment(),
                ),
                spacing="3",
                padding_y="2rem",
                align_items="start",
            )
        ),
        width="100%",
        align_items="stretch",
    )
