import reflex as rx

from uy_click.i18n import t
from uy_click.state.auth_state import AuthState
from uy_click.state.lang_state import LangState


class NavbarState(rx.State):
    menu_open: bool = False

    def toggle_menu(self) -> None:
        self.menu_open = not self.menu_open

    def close_menu(self) -> None:
        self.menu_open = False


_NAV_LINKS = [
    ("nav_listings", "/listings"),
    ("nav_map", "/map"),
    ("nav_favorites", "/favorites"),
    ("nav_my_listings", "/my-listings"),
    ("nav_profile", "/profile"),
]


def _desktop_link(key: str, href: str) -> rx.Component:
    return rx.link(
        t(key),
        href=href,
        color=rx.color("gray", 11),
        font_size="0.875rem",
        font_weight="500",
        _hover={"color": rx.color("gray", 12)},
        white_space="nowrap",
    )


def _mobile_link(key: str, href: str) -> rx.Component:
    return rx.link(
        t(key),
        href=href,
        on_click=NavbarState.close_menu,
        width="100%",
        padding="0.6rem 0.75rem",
        border_radius="md",
        color=rx.color("gray", 11),
        font_size="0.9rem",
        font_weight="500",
        _hover={"background": rx.color("gray", 3), "color": rx.color("gray", 12)},
    )


def _lang_switcher() -> rx.Component:
    def _lang_btn(code: str, label: str) -> rx.Component:
        return rx.button(
            label,
            size="1",
            variant=rx.cond(LangState.lang == code, "solid", "ghost"),
            color_scheme=rx.cond(LangState.lang == code, "teal", "gray"),
            on_click=LangState.set_lang(code),
            style={"font_weight": "600", "min_width": "32px"},
        )

    return rx.hstack(
        _lang_btn("uz", "UZ"),
        _lang_btn("ru", "RU"),
        _lang_btn("en", "EN"),
        spacing="1",
    )


def navbar() -> rx.Component:
    logo = rx.link(
        rx.hstack(
            rx.box(
                rx.icon("house", size=18, color="white"),
                background="linear-gradient(135deg, #0d9488, #0f766e)",
                padding="0.35rem",
                border_radius="8px",
            ),
            rx.heading("UY-CLICK", size="4", weight="bold", color=rx.color("gray", 12)),
            spacing="2",
            align="center",
        ),
        href="/",
        underline="none",
        color="inherit",
    )

    desktop_links = rx.hstack(
        *[_desktop_link(key, href) for key, href in _NAV_LINKS[:4]],
        spacing="5",
        display=rx.breakpoints(initial="none", lg="flex"),
    )

    post_btn = rx.link(
        rx.button(
            rx.icon("plus", size=14),
            t("nav_post"),
            size="2",
            color_scheme="teal",
            variant="solid",
            style={"font_weight": "600"},
        ),
        href="/create",
        underline="none",
        display=rx.breakpoints(initial="none", sm="flex"),
    )

    user_section = rx.cond(
        AuthState.is_logged_in,
        rx.hstack(
            rx.cond(
                AuthState.is_blocked,
                rx.badge(t("nav_blocked"), color_scheme="red", variant="soft", size="1"),
                rx.text(
                    AuthState.user_name,
                    size="2",
                    color=rx.color("gray", 10),
                    display=rx.breakpoints(initial="none", md="block"),
                    max_width="120px",
                    overflow="hidden",
                    text_overflow="ellipsis",
                    white_space="nowrap",
                ),
            ),
            rx.button(
                t("nav_sign_out"),
                on_click=AuthState.logout,
                variant="soft",
                size="1",
                color_scheme="gray",
            ),
            spacing="2",
            align="center",
        ),
        rx.hstack(
            rx.link(
                t("nav_sign_in"),
                href="/login",
                size="2",
                color=rx.color("gray", 11),
                font_weight="500",
                display=rx.breakpoints(initial="none", sm="block"),
            ),
            spacing="3",
            align="center",
        ),
    )

    hamburger = rx.icon_button(
        rx.icon("menu", size=18),
        variant="ghost",
        color_scheme="gray",
        size="2",
        on_click=NavbarState.toggle_menu,
        display=rx.breakpoints(initial="flex", lg="none"),
        aria_label="Menu",
    )

    mobile_menu = rx.cond(
        NavbarState.menu_open,
        rx.vstack(
            rx.link(
                rx.button(
                    rx.icon("plus", size=14),
                    t("nav_post"),
                    size="2",
                    color_scheme="teal",
                    variant="solid",
                    width="100%",
                ),
                href="/create",
                on_click=NavbarState.close_menu,
                underline="none",
                width="100%",
            ),
            rx.divider(),
            *[_mobile_link(key, href) for key, href in _NAV_LINKS],
            rx.divider(),
            _lang_switcher(),
            rx.divider(),
            rx.cond(
                AuthState.is_logged_in,
                rx.button(
                    t("nav_sign_out"),
                    on_click=[AuthState.logout, NavbarState.close_menu],
                    variant="soft",
                    color_scheme="gray",
                    size="2",
                    width="100%",
                ),
                rx.hstack(
                    rx.link(
                        rx.button(t("nav_sign_in"), variant="soft", color_scheme="gray", size="2", width="100%"),
                        href="/login",
                        on_click=NavbarState.close_menu,
                        width="100%",
                        underline="none",
                    ),
                    rx.link(
                        rx.button(t("nav_register"), variant="solid", color_scheme="teal", size="2", width="100%"),
                        href="/register",
                        on_click=NavbarState.close_menu,
                        width="100%",
                        underline="none",
                    ),
                    spacing="2",
                    width="100%",
                ),
            ),
            align_items="stretch",
            spacing="1",
            padding="0.75rem 1rem 1rem",
            border_bottom=f"1px solid {rx.color('gray', 4)}",
            bg=rx.color("gray", 1),
            width="100%",
        ),
        rx.fragment(),
    )

    return rx.vstack(
        rx.hstack(
            logo,
            rx.spacer(),
            desktop_links,
            rx.spacer(),
            _lang_switcher(),
            post_btn,
            user_section,
            hamburger,
            width="100%",
            padding_x="1.25rem",
            padding_y="0.75rem",
            align="center",
            gap="3",
        ),
        mobile_menu,
        width="100%",
        spacing="0",
        position="sticky",
        top="0",
        bg=rx.color("gray", 1),
        z_index="100",
        border_bottom=f"1px solid {rx.color('gray', 4)}",
        style={"backdrop_filter": "blur(8px)"},
    )
