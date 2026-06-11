import reflex as rx

from uy_click.components.footer import site_footer
from uy_click.components.navbar import navbar
from uy_click.components.listing_card import listing_card
from uy_click.i18n import t
from uy_click.state.listing_state import ListingState


def _stat_block(value: str | rx.Var, label_key: str) -> rx.Component:
    return rx.vstack(
        rx.text(value, weight="bold", size="5", color="white"),
        rx.text(t(label_key), size="1", style={"color": "rgba(255,255,255,0.6)"}),
        align_items="center",
        spacing="0",
    )


def _divider_v() -> rx.Component:
    return rx.box(width="1px", height="32px", background="rgba(255,255,255,0.25)")


def _hero_section() -> rx.Component:
    return rx.box(
        rx.container(
            rx.vstack(
                rx.badge(
                    rx.hstack(
                        rx.icon("shield-check", size=13),
                        t("hero_badge"),
                        spacing="1",
                        align="center",
                    ),
                    size="2",
                    style={
                        "background": "rgba(255,255,255,0.15)",
                        "color": "white",
                        "border": "1px solid rgba(255,255,255,0.25)",
                    },
                ),
                rx.heading(
                    t("hero_title"),
                    rx.text.span(
                        t("hero_direct"),
                        style={"color": "rgba(255,255,255,0.7)"},
                    ),
                    size="9",
                    weight="bold",
                    color="white",
                    line_height="1.05",
                    style={"letter_spacing": "-0.03em"},
                ),
                rx.text(
                    t("hero_subtitle"),
                    size="4",
                    style={"color": "rgba(255,255,255,0.8)"},
                    max_width="520px",
                    line_height="1.6",
                ),
                rx.hstack(
                    rx.link(
                        rx.button(
                            t("hero_btn_view"),
                            rx.icon("arrow-right", size=16),
                            size="3",
                            style={
                                "background": "white",
                                "color": "#0f766e",
                                "font_weight": "600",
                                "cursor": "pointer",
                            },
                        ),
                        href="/listings",
                        underline="none",
                    ),
                    rx.link(
                        rx.button(
                            rx.icon("plus", size=16),
                            t("hero_btn_post"),
                            size="3",
                            variant="outline",
                            style={
                                "border": "1px solid rgba(255,255,255,0.45)",
                                "color": "white",
                                "cursor": "pointer",
                            },
                        ),
                        href="/create",
                        underline="none",
                    ),
                    spacing="3",
                    flex_wrap="wrap",
                    padding_top="0.5rem",
                ),
                rx.hstack(
                    _stat_block(
                        ListingState.listings_filtered_count.to_string() + "+",
                        "stat_listings",
                    ),
                    _divider_v(),
                    _stat_block("0%", "stat_commission"),
                    _divider_v(),
                    _stat_block("P2P", "stat_chat"),
                    spacing="5",
                    align="center",
                    padding_top="1.5rem",
                    flex_wrap="wrap",
                ),
                align_items="start",
                spacing="4",
                padding_y=rx.breakpoints(initial="3rem", md="5rem"),
            ),
            size="4",
        ),
        width="100%",
        style={
            "background": "linear-gradient(135deg, #134e4a 0%, #0d9488 55%, #0f766e 100%)",
        },
    )


def _skeleton_card() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.skeleton(height="240px", width="100%", border_radius="0"),
            rx.vstack(
                rx.skeleton(height="18px", width="75%"),
                rx.skeleton(height="14px", width="55%"),
                rx.skeleton(height="22px", width="42%"),
                spacing="2",
                padding="0.75rem 0.875rem 0.875rem",
                width="100%",
            ),
            spacing="0",
        ),
        width="100%",
        variant="surface",
        padding="0",
        style={"overflow": "hidden"},
    )


def _listings_section() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.hstack(
                rx.heading(t("section_recent"), size="6", weight="bold"),
                rx.spacer(),
                rx.link(
                    rx.hstack(
                        t("section_all"),
                        rx.icon("arrow-right", size=14, color=rx.color("teal", 9)),
                        spacing="1",
                        align="center",
                    ),
                    href="/listings",
                    underline="none",
                    size="2",
                    color=rx.color("teal", 9),
                    font_weight="500",
                ),
                width="100%",
                align="center",
            ),
            rx.cond(
                ListingState.listings_loading,
                rx.grid(
                    _skeleton_card(),
                    _skeleton_card(),
                    _skeleton_card(),
                    _skeleton_card(),
                    _skeleton_card(),
                    _skeleton_card(),
                    columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                    spacing="4",
                    width="100%",
                ),
                rx.cond(
                    ListingState.homepage_listings.length() > 0,
                    rx.grid(
                        rx.foreach(ListingState.homepage_listings, listing_card),
                        columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                        spacing="4",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.icon("home", size=40, color=rx.color("gray", 5)),
                        rx.text(
                            t("home_empty"),
                            size="3",
                            color=rx.color("gray", 10),
                        ),
                        rx.link(
                            rx.button(t("nav_post"), color_scheme="teal", size="2"),
                            href="/create",
                            underline="none",
                        ),
                        align_items="center",
                        spacing="3",
                        padding_y="3rem",
                        width="100%",
                    ),
                ),
            ),
            spacing="5",
            padding_y="2.5rem",
            width="100%",
        ),
        size="4",
    )


def _features_row() -> rx.Component:
    features = [
        ("message-circle", "teal", "feat_chat_title", "feat_chat_desc"),
        ("heart", "crimson", "feat_fav_title", "feat_fav_desc"),
        ("map-pin", "blue", "feat_map_title", "feat_map_desc"),
    ]
    return rx.box(
        rx.container(
            rx.grid(
                *[
                    rx.hstack(
                        rx.box(
                            rx.icon(icon, size=20, color=rx.color(color, 10)),
                            padding="0.5rem",
                            border_radius="10px",
                            background=rx.color(color, 3),
                        ),
                        rx.vstack(
                            rx.text(t(title_key), weight="bold", size="3"),
                            rx.text(t(desc_key), size="2", color=rx.color("gray", 10)),
                            spacing="0",
                            align_items="start",
                        ),
                        spacing="3",
                        align="start",
                    )
                    for icon, color, title_key, desc_key in features
                ],
                columns=rx.breakpoints(initial="1", sm="3"),
                spacing="5",
                width="100%",
            ),
            size="4",
        ),
        width="100%",
        padding_y="2rem",
        border_top=f"1px solid {rx.color('gray', 4)}",
        background=rx.color("gray", 2),
    )


def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        _hero_section(),
        _features_row(),
        rx.box(
            _listings_section(),
            width="100%",
            background=rx.color("gray", 1),
        ),
        site_footer(),
        width="100%",
        min_height="100vh",
        align_items="stretch",
        spacing="0",
        background=rx.color("gray", 1),
    )
