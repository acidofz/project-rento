import reflex as rx

from rento.components.listing_card import listing_card
from rento.components.footer import site_footer
from rento.components.navbar import navbar
from rento.state.listing_state import ListingState


def favorite_card(listing) -> rx.Component:
    return rx.vstack(
        listing_card(listing),
        rx.button(
            "Убрать",
            on_click=ListingState.toggle_favorite(listing.id),
            variant="soft",
        ),
        spacing="2",
        width="100%",
    )


def favorites() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.hstack(
                    rx.heading("Избранное", size="7"),
                    rx.spacer(),
                    rx.button("Обновить", on_click=ListingState.load_listings, variant="soft"),
                    width="100%",
                ),
                rx.text(
                    "Сохранённые объявления — только у вас в аккаунте.",
                    size="2",
                    color=rx.color("gray", 10),
                    width="100%",
                ),
                rx.cond(
                    ListingState.error_message,
                    rx.callout(ListingState.error_message, color_scheme="red"),
                    rx.fragment(),
                ),
                rx.cond(
                    ListingState.favorite_listings,
                    rx.grid(
                        rx.foreach(ListingState.favorite_listings, favorite_card),
                        columns="2",
                        spacing="4",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text(
                            "Здесь появятся объявления, которые вы добавите через «В избранное».",
                            color=rx.color("gray", 11),
                        ),
                        rx.link(
                            "К объявлениям",
                            href="/listings",
                            color=rx.color("blue", 11),
                        ),
                        spacing="2",
                        align_items="start",
                    ),
                ),
                width="100%",
                spacing="4",
                padding_y="2rem",
            ),
            size="4",
        ),
        site_footer(),
        width="100%",
        min_height="100vh",
        align_items="stretch",
    )
