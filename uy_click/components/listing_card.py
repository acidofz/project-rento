import reflex as rx

from uy_click.state.listing_state import Listing
from uy_click.utils.helpers import format_price_uzs


def listing_card_content(listing: Listing) -> rx.Component:
    return rx.vstack(
        # Image — bleeds to card edges, top corners clipped
        rx.box(
            # Placeholder always in background — visible when image_url is
            # empty OR when the URL is set but the image fails to load (404)
            rx.center(
                rx.icon("image", size=32, color=rx.color("gray", 6)),
                width="100%",
                height="200px",
                background=rx.color("gray", 2),
                position="absolute",
                top="0",
                left="0",
            ),
            rx.cond(
                listing.image_url != "",
                rx.image(
                    src=listing.image_url,
                    width="100%",
                    height="200px",
                    object_fit="cover",
                    alt=listing.title,
                    display="block",
                    position="relative",
                ),
                rx.fragment(),
            ),
            rx.cond(
                listing.is_premium,
                rx.box(
                    rx.badge(
                        rx.hstack(
                            rx.icon("star", size=10),
                            rx.text("PREMIUM", size="1"),
                            spacing="1",
                            align="center",
                        ),
                        color_scheme="amber",
                        variant="solid",
                        size="1",
                    ),
                    position="absolute",
                    top="0.6rem",
                    left="0.6rem",
                ),
                rx.fragment(),
            ),
            position="relative",
            width="100%",
            overflow="hidden",
            border_radius="var(--radius-3) var(--radius-3) 0 0",
        ),
        # Content
        rx.vstack(
            rx.link(
                rx.text(
                    listing.title,
                    weight="medium",
                    size="3",
                    color=rx.color("gray", 12),
                    line_height="1.4",
                ),
                href="/listing/" + listing.id.to_string(),
                underline="none",
                color="inherit",
                width="100%",
            ),
            rx.hstack(
                rx.icon("map-pin", size=11, color=rx.color("gray", 8)),
                rx.text(listing.district, size="2", color=rx.color("gray", 9)),
                rx.text("·", color=rx.color("gray", 5), size="2"),
                rx.icon("door-open", size=11, color=rx.color("gray", 8)),
                rx.text(listing.rooms, " комн.", size="2", color=rx.color("gray", 9)),
                spacing="1",
                align="center",
                flex_wrap="wrap",
            ),
            rx.text(
                format_price_uzs(listing.price),
                weight="bold",
                size="4",
                color=rx.color("jade", 10),
            ),
            align_items="start",
            spacing="2",
            padding="0.75rem 0.875rem 0.875rem",
            width="100%",
        ),
        spacing="0",
        width="100%",
        align_items="start",
    )


_CARD_STYLE = {
    "box_shadow": "0 1px 4px rgba(0,0,0,0.06), 0 0 0 1px rgba(0,0,0,0.05)",
    "transition": "box-shadow 200ms ease, transform 200ms ease",
    "overflow": "hidden",
}

_CARD_HOVER = {
    "transform": "translateY(-3px)",
    "box_shadow": "0 8px 24px -4px rgba(0,0,0,0.12), 0 0 0 1px rgba(0,0,0,0.07)",
}


def listing_card(listing: Listing) -> rx.Component:
    return rx.card(
        listing_card_content(listing),
        variant="surface",
        padding="0",
        width="100%",
        border=rx.cond(
            listing.is_premium,
            "1px solid rgba(245, 158, 11, 0.3)",
            "none",
        ),
        style=_CARD_STYLE,
        _hover=_CARD_HOVER,
    )
