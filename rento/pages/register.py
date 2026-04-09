import reflex as rx

from rento.components.navbar import navbar
from rento.state.auth_state import AuthState


def register() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Регистрация", size="7"),
                rx.text(
                    "Один пароль — и можно размещать объявления.",
                    size="2",
                    color=rx.color("gray", 10),
                ),
                rx.input(
                    placeholder="Электронная почта",
                    value=AuthState.email,
                    on_change=AuthState.set_email,
                    width="100%",
                ),
                rx.input(
                    placeholder="Пароль",
                    type="password",
                    value=AuthState.password,
                    on_change=AuthState.set_password,
                    width="100%",
                ),
                rx.button("Создать аккаунт", on_click=AuthState.register, width="100%"),
                rx.link(
                    "Уже есть аккаунт? Войти",
                    href="/login",
                    size="2",
                    color=rx.color("blue", 11),
                ),
                rx.cond(
                    AuthState.error_message,
                    rx.callout(AuthState.error_message, color_scheme="red"),
                    rx.fragment(),
                ),
                max_width="420px",
                width="100%",
                spacing="3",
                padding_y="2rem",
            )
        ),
        width="100%",
        align_items="stretch",
    )
