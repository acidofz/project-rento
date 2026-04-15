import reflex as rx

from rento.components.footer import site_footer
from rento.components.navbar import navbar


def health() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Сервис в порядке", size="7"),
                rx.badge("OK", color_scheme="green", size="3"),
                rx.text(
                    "Приложение отвечает, маршруты доступны. Используйте для проверки после деплоя.",
                    size="2",
                    color=rx.color("gray", 10),
                ),
                spacing="3",
                padding_y="2rem",
                align_items="start",
            ),
            size="3",
        ),
        site_footer(),
        width="100%",
        min_height="100vh",
        align_items="stretch",
    )
