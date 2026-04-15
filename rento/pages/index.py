import reflex as rx

from rento.components.footer import site_footer
from rento.components.navbar import navbar


def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Аренда жилья без посредников", size="8"),
                rx.text(
                    "Снимайте и сдавайте напрямую — объявления, чат и избранное в одном месте.",
                    size="4",
                    color=rx.color("gray", 11),
                ),
                rx.hstack(
                    rx.button("Смотреть объявления", on_click=rx.redirect("/listings")),
                    rx.button(
                        "Подать объявление",
                        on_click=rx.redirect("/create"),
                        variant="soft",
                    ),
                    spacing="3",
                ),
                align_items="start",
                spacing="5",
                padding_y="2rem",
            ),
            size="3",
        ),
        site_footer(),
        width="100%",
        min_height="100vh",
        align_items="stretch",
    )
