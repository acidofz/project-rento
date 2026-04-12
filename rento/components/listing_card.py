import reflex as rx

from rento.state.listing_state import Listing
from rento.utils.helpers import format_price_uzs


def listing_card(listing: Listing) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.cond(
                listing.image_url != "",
                rx.image(
                    src=listing.image_url,
                    width="100%",
                    height="140px",
                    object_fit="cover",
                    alt=listing.title,
                    border_radius="md",
                ),
                rx.box(
                    rx.center(
                        rx.text("Нет фото", size="1", color=rx.color("gray", 9)),
                        width="100%",
                        height="100%",
                    ),
                    width="100%",
                    height="140px",
                    background=rx.color("gray", 3),
                    border_radius="md",
                ),
            ),
            rx.heading(listing.title, size="4"),
            rx.text(
                f"{listing.district} · {listing.rooms} комн.",
                color=rx.color("gray", 11),
                size="2",
            ),
            rx.badge(format_price_uzs(listing.price), color_scheme="green", variant="soft"),
            align_items="start",
            spacing="2",
        ),
        width="100%",
    )
