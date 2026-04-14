import reflex as rx

from rento.components.navbar import navbar
from rento.state.listing_state import ListingState


def map_page() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Карта объявлений", size="7"),
                rx.text(
                    "Точки с координатами из объявлений. Укажите широту и долготу при создании или "
                    "редактировании (например из карт: Ташкент ≈ 41.31, 69.28).",
                    size="2",
                    color=rx.color("gray", 10),
                ),
                rx.box(
                    id="rento-map",
                    width="100%",
                    height="70vh",
                    border_radius="md",
                    border=f"1px solid {rx.color('gray', 5)}",
                    overflow="hidden",
                ),
                rx.script(src="/rento_map.js"),
                rx.cond(
                    ListingState.error_message,
                    rx.callout(ListingState.error_message, color_scheme="red"),
                    rx.fragment(),
                ),
                width="100%",
                spacing="4",
                padding_y="2rem",
                align_items="stretch",
            ),
            size="4",
        ),
        width="100%",
        min_height="100vh",
        align_items="stretch",
    )
