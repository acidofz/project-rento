import reflex as rx

from uy_click.components.listing_card import listing_card
from uy_click.components.footer import site_footer
from uy_click.components.navbar import navbar
from uy_click.i18n import t
from uy_click.state.listing_state import ListingState


def favorite_card(listing) -> rx.Component:
    return rx.vstack(
        listing_card(listing),
        rx.button(
            t("favorites_remove"),
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
                    rx.heading(t("favorites_title"), size="7"),
                    rx.spacer(),
                    rx.button(t("favorites_refresh"), on_click=ListingState.load_listings, variant="soft"),
                    width="100%",
                ),
                rx.text(t("favorites_subtitle"), size="2", color=rx.color("gray", 10), width="100%"),
                rx.cond(
                    ListingState.error_message,
                    rx.callout(ListingState.error_message, color_scheme="red"),
                    rx.fragment(),
                ),
                rx.cond(
                    ListingState.favorite_listings,
                    rx.grid(
                        rx.foreach(ListingState.favorite_listings, favorite_card),
                        columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                        spacing="4",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text(t("favorites_empty"), color=rx.color("gray", 11)),
                        rx.link(t("favorites_go_listings"), href="/listings", color=rx.color("teal", 10)),
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
