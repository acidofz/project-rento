import reflex as rx

from uy_click.state.listing_state import Listing
from uy_click.utils.helpers import format_price_uzs


def listing_card_content(listing: Listing) -> rx.Component:
    """Card body without outer rx.card — reusable in listing variants."""
    return rx.vstack(
        rx.cond(
            listing.is_premium,
            rx.badge("PREMIUM", color_scheme="amber", variant="solid", size="1"),
            rx.fragment(),
        ),
        rx.cond(
            listing.image_url != "",
            rx.image(
                src=listing.image_url,
                width="100%",
                height="160px",
                object_fit="cover",
                alt=listing.title,
                border_radius="md",
            ),
            rx.center(
                rx.icon("image", size=24, color=rx.color("gray", 7)),
                width="100%",
                height="160px",
                background=rx.color("gray", 3),
                border_radius="md",
            ),
        ),
        rx.link(
            rx.text(listing.title, weight="medium", size="3"),
            href="/listing/" + listing.id.to_string(),
            color="inherit",
            underline="hover",
        ),
        rx.hstack(
            rx.icon("map-pin", size=12, color=rx.color("gray", 9)),
            rx.text(listing.district, size="2", color=rx.color("gray", 10)),
            rx.text("·", color=rx.color("gray", 7), size="2"),
            rx.text(listing.rooms, size="2", color=rx.color("gray", 10)),
            rx.text("комн.", size="2", color=rx.color("gray", 10)),
            spacing="1",
            align="center",
            flex_wrap="wrap",
        ),
        rx.badge(format_price_uzs(listing.price), color_scheme="green", variant="soft", size="2"),
        align_items="start",
        spacing="2",
        width="100%",
    )


_CARD_STYLE = {
    "box_shadow": "0 2px 12px -4px rgba(0, 0, 0, 0.08)",
    "transition": "transform 180ms ease, box-shadow 180ms ease",
}

_CARD_HOVER = {
    "transform": "translateY(-3px)",
    "box_shadow": "0 10px 28px -8px rgba(0, 0, 0, 0.16)",
}


def listing_card(listing: Listing) -> rx.Component:
    return rx.card(
        listing_card_content(listing),
        variant="surface",
        size="3",
        width="100%",
        border=rx.cond(
            listing.is_premium,
            "1px solid rgba(245, 158, 11, 0.3)",
            "1px solid rgba(148, 163, 184, 0.15)",
        ),
        style=_CARD_STYLE,
        _hover=_CARD_HOVER,
    )
