import reflex as rx

from rento.state.listing_state import Listing
from rento.utils.helpers import format_price_uzs


def listing_card(listing: Listing) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(listing.title, size="4"),
            rx.text(f"Район: {listing.district}", color=rx.color("gray", 11)),
            rx.text(f"Комнаты: {listing.rooms}", color=rx.color("gray", 11)),
            rx.badge(format_price_uzs(listing.price), color_scheme="green", variant="soft"),
            align_items="start",
            spacing="2",
        ),
        width="100%",
    )
