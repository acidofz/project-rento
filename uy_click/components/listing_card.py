import reflex as rx

from uy_click.state.listing_state import Listing
from uy_click.utils.helpers import format_price_uzs


def listing_card(listing: Listing) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.cond(
                listing.is_premium,
                rx.badge("PREMIUM", color_scheme="amber", variant="solid"),
                rx.fragment(),
            ),
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
            rx.link(
                rx.heading(listing.title, size="4"),
                href="/listing/" + listing.id.to_string(),
                color="inherit",
                underline="hover",
            ),
            rx.text(
                f"{listing.district} · {listing.rooms} комн.",
                color=rx.color("gray", 11),
                size="2",
            ),
            rx.badge(format_price_uzs(listing.price), color_scheme="green", variant="soft"),
            align_items="start",
            spacing="2",
        ),
        variant="surface",
        size="3",
        width="100%",
        border=rx.cond(
            listing.is_premium,
            "1px solid rgba(245, 158, 11, 0.28)",
            "1px solid rgba(148, 163, 184, 0.18)",
        ),
        style={"box_shadow": "0 2px 12px -4px rgba(0, 0, 0, 0.08)"},
    )
