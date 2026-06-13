import reflex as rx

from uy_click.components.footer import site_footer
from uy_click.components.navbar import navbar
from uy_click.i18n import t
from uy_click.state.listing_state import ListingState
from uy_click.utils.helpers import format_price_uzs


def listing_detail() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.link(
                    rx.hstack(
                        rx.icon("arrow-left", size=14),
                        t("detail_back"),
                        spacing="1",
                        align="center",
                    ),
                    href="/listings",
                    size="2",
                    color=rx.color("teal", 10),
                    underline="none",
                    font_weight="500",
                ),
                rx.cond(
                    ListingState.error_message,
                    rx.callout(ListingState.error_message, color_scheme="red"),
                    rx.fragment(),
                ),
                rx.cond(
                    ListingState.detail_id > 0,
                    rx.vstack(
                        # Image
                        rx.cond(
                            ListingState.detail_image_url != "",
                            rx.image(
                                src=ListingState.detail_image_url,
                                width="100%",
                                max_height="400px",
                                object_fit="cover",
                                border_radius="var(--radius-4)",
                                alt=ListingState.detail_title,
                            ),
                            rx.box(
                                rx.center(
                                    rx.icon("image", size=40, color=rx.color("gray", 6)),
                                    rx.text(t("detail_no_photo"), size="2", color=rx.color("gray", 9)),
                                    flex_direction="column",
                                    gap="0.5rem",
                                    width="100%",
                                    height="200px",
                                ),
                                width="100%",
                                height="200px",
                                background=rx.color("gray", 2),
                                border_radius="var(--radius-4)",
                            ),
                        ),
                        # Main content card
                        rx.card(
                            rx.vstack(
                                # Title + premium badge
                                rx.hstack(
                                    rx.heading(ListingState.detail_title, size="7", line_height="1.2"),
                                    rx.cond(
                                        ListingState.detail_is_premium,
                                        rx.badge(
                                            rx.hstack(
                                                rx.icon("star", size=11),
                                                t("common_premium_badge"),
                                                spacing="1",
                                                align="center",
                                            ),
                                            color_scheme="amber",
                                            variant="solid",
                                        ),
                                        rx.fragment(),
                                    ),
                                    spacing="2",
                                    align_items="start",
                                    flex_wrap="wrap",
                                ),
                                # District + rooms
                                rx.hstack(
                                    rx.hstack(
                                        rx.icon("map-pin", size=14, color=rx.color("gray", 9)),
                                        rx.text(ListingState.detail_district, weight="medium", size="3"),
                                        spacing="1",
                                        align="center",
                                    ),
                                    rx.text("·", color=rx.color("gray", 6)),
                                    rx.hstack(
                                        rx.icon("door-open", size=14, color=rx.color("gray", 9)),
                                        rx.text(ListingState.detail_rooms, " ", t("detail_rooms_suffix"), size="3"),
                                        spacing="1",
                                        align="center",
                                    ),
                                    spacing="2",
                                    align_items="center",
                                    flex_wrap="wrap",
                                ),
                                # Price
                                rx.badge(
                                    format_price_uzs(ListingState.detail_price),
                                    color_scheme="jade",
                                    size="3",
                                    variant="soft",
                                    style={"font_size": "1rem", "font_weight": "700"},
                                ),
                                rx.separator(width="100%"),
                                # Phone block
                                rx.cond(
                                    ListingState.detail_phone != "",
                                    rx.box(
                                        rx.vstack(
                                            rx.text(
                                                t("detail_phone_label"),
                                                size="1",
                                                weight="medium",
                                                color=rx.color("gray", 9),
                                                style={"text_transform": "uppercase", "letter_spacing": "0.06em"},
                                            ),
                                            rx.hstack(
                                                rx.icon("phone", size=20, color=rx.color("teal", 10)),
                                                rx.text(
                                                    ListingState.detail_phone,
                                                    size="5",
                                                    weight="bold",
                                                    color=rx.color("gray", 12),
                                                ),
                                                spacing="2",
                                                align="center",
                                            ),
                                            rx.link(
                                                rx.button(
                                                    rx.icon("phone", size=16),
                                                    t("detail_phone_call"),
                                                    color_scheme="teal",
                                                    variant="solid",
                                                    size="3",
                                                    style={"font_weight": "600"},
                                                ),
                                                href="tel:" + ListingState.detail_phone,
                                                underline="none",
                                                width="100%",
                                            ),
                                            spacing="2",
                                            align_items="start",
                                            width="100%",
                                        ),
                                        padding="1rem",
                                        background=rx.color("teal", 2),
                                        border_radius="var(--radius-3)",
                                        border=f"1px solid {rx.color('teal', 5)}",
                                        width="100%",
                                    ),
                                    rx.hstack(
                                        rx.icon("phone-off", size=16, color=rx.color("gray", 7)),
                                        rx.text(
                                            t("detail_phone_none"),
                                            size="2",
                                            color=rx.color("gray", 9),
                                        ),
                                        spacing="2",
                                        align="center",
                                        padding="0.75rem 1rem",
                                        background=rx.color("gray", 2),
                                        border_radius="var(--radius-3)",
                                        width="100%",
                                    ),
                                ),
                                # Actions
                                rx.hstack(
                                    rx.button(
                                        rx.hstack(
                                            rx.cond(
                                                ListingState.favorite_listing_ids.contains(ListingState.detail_id),
                                                rx.icon("heart", size=15, color=rx.color("crimson", 10)),
                                                rx.icon("heart", size=15),
                                            ),
                                            rx.cond(
                                                ListingState.favorite_listing_ids.contains(ListingState.detail_id),
                                                t("detail_fav_remove"),
                                                t("detail_fav_add"),
                                            ),
                                            spacing="1",
                                            align="center",
                                        ),
                                        on_click=ListingState.toggle_favorite(ListingState.detail_id),
                                        variant="soft",
                                        color_scheme=rx.cond(
                                            ListingState.favorite_listing_ids.contains(ListingState.detail_id),
                                            "crimson",
                                            "gray",
                                        ),
                                        size="2",
                                    ),
                                    rx.cond(
                                        ListingState.detail_has_location,
                                        rx.button(
                                            rx.hstack(
                                                rx.icon("map-pin", size=15),
                                                t("detail_show_map"),
                                                spacing="1",
                                                align="center",
                                            ),
                                            on_click=ListingState.go_to_map_focused(ListingState.detail_id),
                                            variant="soft",
                                            color_scheme="blue",
                                            size="2",
                                        ),
                                        rx.fragment(),
                                    ),
                                    spacing="2",
                                    flex_wrap="wrap",
                                ),
                                spacing="4",
                                align_items="stretch",
                                width="100%",
                            ),
                            width="100%",
                            size="3",
                        ),
                        width="100%",
                        spacing="4",
                        align_items="stretch",
                    ),
                    rx.vstack(
                        rx.box(
                            rx.icon("search-x", size=36, color=rx.color("gray", 6)),
                            padding="1rem",
                            border_radius="full",
                            background=rx.color("gray", 2),
                        ),
                        rx.heading(t("detail_not_found_title"), size="6"),
                        rx.text(t("detail_not_found_desc"), color=rx.color("gray", 10), size="2"),
                        rx.link(
                            rx.button(t("detail_all_listings"), color_scheme="teal", variant="soft"),
                            href="/listings",
                            underline="none",
                        ),
                        spacing="3",
                        align_items="center",
                        padding_y="3rem",
                        width="100%",
                    ),
                ),
                width="100%",
                spacing="4",
                padding_y="2rem",
                align_items="start",
            ),
            size="3",
        ),
        site_footer(),
        width="100%",
        min_height="100vh",
        align_items="stretch",
        background=rx.color("gray", 1),
    )
