import reflex as rx

from rento.components.navbar import navbar


def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Платформа аренды жилья в Узбекистане", size="8"),
                rx.text(
                    "Ищите квартиру или сдавайте жилье напрямую, без риелторов.",
                    size="4",
                    color=rx.color("gray", 11),
                ),
                rx.hstack(
                    rx.button("Смотреть объявления", on_click=rx.redirect("/listings")),
                    rx.button(
                        "Разместить объявление",
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
        width="100%",
        min_height="100vh",
        align_items="stretch",
    )
