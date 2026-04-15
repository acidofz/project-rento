import reflex as rx

from rento.components.footer import site_footer
from rento.components.navbar import navbar
from rento.state.auth_state import AuthState


def login() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Вход", size="7"),
                rx.text(
                    "Чтобы публиковать объявления и отвечать в чате.",
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
                rx.button("Войти", on_click=AuthState.login, width="100%"),
                rx.link(
                    "Нет аккаунта? Зарегистрироваться",
                    href="/register",
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
        site_footer(),
        width="100%",
        align_items="stretch",
    )
