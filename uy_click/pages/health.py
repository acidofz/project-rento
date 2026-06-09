import reflex as rx

from uy_click.components.footer import site_footer
from uy_click.components.navbar import navbar


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
                rx.callout(
                    rx.vstack(
                        rx.text("Для мониторинга и скриптов:", weight="bold", size="2"),
                        rx.text("GET /ping — встроенная проверка Reflex (лучше всего для healthcheck хостинга)."),
                        rx.text("GET /_health — JSON Reflex (его БД/Redis, не Supabase)."),
                        rx.text("GET /ready — доступность Supabase (если env не задан, вернётся not_configured)."),
                        spacing="1",
                        align_items="start",
                    ),
                    icon="info",
                    color_scheme="blue",
                    variant="soft",
                    width="100%",
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
