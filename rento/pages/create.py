import reflex as rx

from rento.components.navbar import navbar
from rento.state.listing_state import ListingState


def create() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Создать объявление", size="7"),
                rx.input(
                    placeholder="Заголовок",
                    value=ListingState.title,
                    on_change=ListingState.set_title,
                ),
                rx.input(
                    placeholder="Район",
                    value=ListingState.district,
                    on_change=ListingState.set_district,
                ),
                rx.input(
                    placeholder="Количество комнат",
                    type="number",
                    min=1,
                    value=ListingState.rooms,
                    on_change=ListingState.set_rooms,
                ),
                rx.input(
                    placeholder="Цена (сум)",
                    type="number",
                    min=0,
                    value=ListingState.price,
                    on_change=ListingState.set_price,
                ),
                rx.button("Опубликовать", on_click=ListingState.add_listing),
                rx.cond(
                    ListingState.success_message,
                    rx.callout(ListingState.success_message, color_scheme="green"),
                    rx.fragment(),
                ),
                rx.cond(
                    ListingState.error_message,
                    rx.callout(ListingState.error_message, color_scheme="red"),
                    rx.fragment(),
                ),
                width="100%",
                max_width="520px",
                align_items="stretch",
                spacing="3",
                padding_y="2rem",
            )
        ),
        width="100%",
        align_items="stretch",
    )
