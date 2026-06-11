import reflex as rx

from uy_click.components.footer import site_footer
from uy_click.components.navbar import navbar
from uy_click.i18n import t
from uy_click.state.auth_state import AuthState


def login() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading(t("login_title"), size="7"),
                rx.text(t("login_subtitle"), size="2", color=rx.color("gray", 10)),
                rx.input(
                    placeholder=t("login_ph_email"),
                    value=AuthState.email,
                    on_change=AuthState.set_email,
                    width="100%",
                ),
                rx.input(
                    placeholder=t("login_ph_password"),
                    type="password",
                    value=AuthState.password,
                    on_change=AuthState.set_password,
                    width="100%",
                ),
                rx.button(t("login_btn"), on_click=AuthState.login, width="100%", color_scheme="teal"),
                rx.link(
                    t("login_no_account"),
                    href="/register",
                    size="2",
                    color=rx.color("teal", 10),
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
