import reflex as rx

from rento.components.navbar import navbar


def health() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Health Check", size="7"),
                rx.badge("OK", color_scheme="green", size="3"),
                rx.text("Приложение запущено и роутинг работает."),
                spacing="3",
                padding_y="2rem",
                align_items="start",
            ),
            size="3",
        ),
        width="100%",
        min_height="100vh",
        align_items="stretch",
    )
