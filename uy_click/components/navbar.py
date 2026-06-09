import reflex as rx

from uy_click.state.auth_state import AuthState


class NavbarState(rx.State):
    menu_open: bool = False

    def toggle_menu(self) -> None:
        self.menu_open = not self.menu_open

    def close_menu(self) -> None:
        self.menu_open = False


_NAV_LINKS = [
    ("Объявления", "/listings"),
    ("Карта", "/map"),
    ("Подать", "/create"),
    ("Чаты", "/chats"),
    ("Избранное", "/favorites"),
    ("Мои объявления", "/my-listings"),
    ("Профиль", "/profile"),
]


def _desktop_link(label: str, href: str) -> rx.Component:
    return rx.link(
        label,
        href=href,
        color=rx.color("gray", 11),
        font_size="0.875rem",
        font_weight="500",
        _hover={"color": rx.color("gray", 12)},
        white_space="nowrap",
    )


def _mobile_link(label: str, href: str) -> rx.Component:
    return rx.link(
        label,
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


def navbar() -> rx.Component:
    logo = rx.link(
        rx.hstack(
            rx.heading("UY-CLICK", size="5", weight="bold", color=rx.color("gray", 12)),
            rx.text(
                "Прямая аренда",
                size="1",
                color=rx.color("gray", 9),
                display=rx.breakpoints(initial="none", sm="block"),
            ),
            spacing="2",
            align="center",
        ),
        href="/",
        underline="none",
        color="inherit",
    )

    desktop_links = rx.hstack(
        *[_desktop_link(label, href) for label, href in _NAV_LINKS[:5]],
        spacing="5",
        display=rx.breakpoints(initial="none", lg="flex"),
    )

    user_section = rx.cond(
        AuthState.is_logged_in,
        rx.hstack(
            rx.cond(
                AuthState.is_blocked,
                rx.badge("Заблокирован", color_scheme="red", variant="soft", size="1"),
                rx.text(
                    AuthState.user_name,
                    size="2",
                    color=rx.color("gray", 10),
                    display=rx.breakpoints(initial="none", sm="block"),
                    max_width="120px",
                    overflow="hidden",
                    text_overflow="ellipsis",
                    white_space="nowrap",
                ),
            ),
            rx.button(
                "Выйти",
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
                "Войти",
                href="/login",
                size="2",
                color=rx.color("gray", 11),
                font_weight="500",
            ),
            rx.link(
                rx.button("Регистрация", size="1", variant="soft", color_scheme="indigo"),
                href="/register",
                underline="none",
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
        aria_label="Меню",
    )

    mobile_menu = rx.cond(
        NavbarState.menu_open,
        rx.vstack(
            *[_mobile_link(label, href) for label, href in _NAV_LINKS],
            rx.divider(),
            rx.cond(
                AuthState.is_logged_in,
                rx.button(
                    "Выйти",
                    on_click=[AuthState.logout, NavbarState.close_menu],
                    variant="soft",
                    color_scheme="gray",
                    size="2",
                    width="100%",
                ),
                rx.hstack(
                    rx.link(
                        rx.button("Войти", variant="soft", color_scheme="gray", size="2", width="100%"),
                        href="/login",
                        on_click=NavbarState.close_menu,
                        width="100%",
                        underline="none",
                    ),
                    rx.link(
                        rx.button("Регистрация", variant="soft", color_scheme="indigo", size="2", width="100%"),
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
            user_section,
            hamburger,
            width="100%",
            padding_x="1.25rem",
            padding_y="0.75rem",
            align="center",
        ),
        mobile_menu,
        width="100%",
        spacing="0",
        position="sticky",
        top="0",
        bg=rx.color("gray", 1),
        z_index="100",
        border_bottom=f"1px solid {rx.color('gray', 4)}",
    )
