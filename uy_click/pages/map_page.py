import reflex as rx

from uy_click.components.footer import site_footer
from uy_click.components.navbar import navbar
from uy_click.i18n import t
from uy_click.state.listing_state import ListingState


def map_page() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading(t("map_title"), size="7"),
                rx.text(
                    t("map_description"),
                    size="2",
                    color=rx.color("gray", 10),
                ),
                rx.box(
                    id="uy-click-map",
                    width="100%",
                    height="70vh",
                    border_radius="md",
                    border=f"1px solid {rx.color('gray', 5)}",
                    overflow="hidden",
                ),
                rx.script(src="/uy_click_map.js"),
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
        site_footer(),
        width="100%",
        min_height="100vh",
        align_items="stretch",
    )
