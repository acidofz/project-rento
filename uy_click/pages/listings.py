import reflex as rx

from uy_click.components.listing_card import listing_card_content, _CARD_STYLE, _CARD_HOVER
from uy_click.components.footer import site_footer
from uy_click.components.navbar import navbar
from uy_click.state.chat_state import ChatState
from uy_click.state.listing_state import ListingState


def skeleton_listing_card() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.skeleton(height="160px", width="100%"),
            rx.skeleton(height="18px", width="70%"),
            rx.skeleton(height="14px", width="50%"),
            rx.skeleton(height="22px", width="38%"),
            spacing="3",
        ),
        width="100%",
        variant="surface",
    )


def listing_card_with_actions(listing) -> rx.Component:
    is_fav = ListingState.favorite_listing_ids.contains(listing.id)
    return rx.card(
        rx.vstack(
            listing_card_content(listing),
            rx.spacer(),
            rx.hstack(
                rx.button(
                    rx.cond(
                        is_fav,
                        rx.hstack(rx.icon("heart", size=13), rx.text("Убрать", size="1"), spacing="1", align="center"),
                        rx.hstack(rx.icon("heart", size=13), rx.text("Избранное", size="1"), spacing="1", align="center"),
                    ),
                    on_click=ListingState.toggle_favorite(listing.id),
                    variant="soft",
                    size="1",
                    color_scheme=rx.cond(is_fav, "crimson", "gray"),
                ),
                rx.button(
                    rx.hstack(
                        rx.icon("message-circle", size=13),
                        rx.text("Написать", size="1"),
                        spacing="1",
                        align="center",
                    ),
                    on_click=ChatState.create_chat_with_user(listing.owner_id),
                    variant="soft",
                    size="1",
                    color_scheme="indigo",
                ),
                spacing="2",
                width="100%",
                padding_top="0.25rem",
            ),
            spacing="2",
            width="100%",
            height="100%",
            align_items="start",
        ),
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


def _filter_input(label: str, placeholder: str, value, on_change, type: str = "text") -> rx.Component:
    return rx.vstack(
        rx.text(label, size="1", color=rx.color("gray", 10), weight="medium"),
        rx.input(
            placeholder=placeholder,
            type=type,
            min=0 if type == "number" else None,
            value=value,
            on_change=on_change,
            width="100%",
        ),
        spacing="1",
        align_items="start",
        width="100%",
    )


def listings() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                # ── Header ──
                rx.hstack(
                    rx.vstack(
                        rx.heading("Объявления", size="7"),
                        rx.text(
                            ListingState.listings_filtered_count,
                            " объявлений",
                            size="2",
                            color=rx.color("gray", 10),
                        ),
                        spacing="0",
                        align_items="start",
                    ),
                    rx.spacer(),
                    rx.hstack(
                        rx.button(
                            rx.icon("map", size=14),
                            "Карта",
                            on_click=rx.redirect("/map"),
                            variant="soft",
                            size="2",
                        ),
                        rx.select(
                            [
                                ("Новые первые", "newest"),
                                ("Сначала дешевле", "price_asc"),
                                ("Сначала дороже", "price_desc"),
                                ("Больше комнат", "rooms_desc"),
                            ],
                            value=ListingState.sort_by,
                            on_change=ListingState.set_sort_by,
                            width="160px",
                        ),
                        spacing="2",
                        flex_wrap="wrap",
                    ),
                    width="100%",
                    align="end",
                    flex_wrap="wrap",
                    gap="3",
                ),
                # ── Filters ──
                rx.card(
                    rx.vstack(
                        rx.grid(
                            rx.vstack(
                                rx.text("Поиск", size="1", color=rx.color("gray", 10), weight="medium"),
                                rx.input(
                                    placeholder="Район или название",
                                    value=ListingState.search_query,
                                    on_change=ListingState.set_search_query,
                                    width="100%",
                                ),
                                spacing="1",
                                align_items="start",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.text("Район", size="1", color=rx.color("gray", 10), weight="medium"),
                                rx.input(
                                    placeholder="Все районы",
                                    value=ListingState.filter_district,
                                    on_change=ListingState.set_filter_district,
                                    width="100%",
                                ),
                                spacing="1",
                                align_items="start",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.text("Цена (сум/мес)", size="1", color=rx.color("gray", 10), weight="medium"),
                                rx.hstack(
                                    rx.input(
                                        placeholder="от",
                                        type="number",
                                        min=0,
                                        value=ListingState.min_price,
                                        on_change=ListingState.set_min_price,
                                        width="100%",
                                    ),
                                    rx.input(
                                        placeholder="до",
                                        type="number",
                                        min=0,
                                        value=ListingState.max_price,
                                        on_change=ListingState.set_max_price,
                                        width="100%",
                                    ),
                                    spacing="2",
                                    width="100%",
                                ),
                                spacing="1",
                                align_items="start",
                                width="100%",
                            ),
                            rx.vstack(
                                rx.text("Комнат", size="1", color=rx.color("gray", 10), weight="medium"),
                                rx.hstack(
                                    rx.input(
                                        placeholder="от",
                                        type="number",
                                        min=0,
                                        value=ListingState.min_rooms,
                                        on_change=ListingState.set_min_rooms,
                                        width="100%",
                                    ),
                                    rx.input(
                                        placeholder="до",
                                        type="number",
                                        min=0,
                                        value=ListingState.max_rooms,
                                        on_change=ListingState.set_max_rooms,
                                        width="100%",
                                    ),
                                    spacing="2",
                                    width="100%",
                                ),
                                spacing="1",
                                align_items="start",
                                width="100%",
                            ),
                            columns=rx.breakpoints(initial="1", sm="2", lg="4"),
                            spacing="3",
                            width="100%",
                        ),
                        rx.button(
                            rx.icon("x", size=14),
                            "Сбросить фильтры",
                            on_click=ListingState.reset_filters,
                            variant="ghost",
                            size="1",
                            color_scheme="gray",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    variant="surface",
                    size="2",
                    width="100%",
                ),
                # ── Error ──
                rx.cond(
                    ListingState.error_message,
                    rx.callout(ListingState.error_message, color_scheme="red"),
                    rx.fragment(),
                ),
                # ── Grid ──
                rx.cond(
                    ListingState.listings_loading,
                    rx.grid(
                        skeleton_listing_card(),
                        skeleton_listing_card(),
                        skeleton_listing_card(),
                        skeleton_listing_card(),
                        columns=rx.breakpoints(initial="1", sm="2"),
                        spacing="4",
                        width="100%",
                    ),
                    rx.cond(
                        ListingState.has_filtered_listings,
                        rx.grid(
                            rx.foreach(
                                ListingState.paginated_filtered_listings,
                                listing_card_with_actions,
                            ),
                            columns=rx.breakpoints(initial="1", sm="2"),
                            spacing="4",
                            width="100%",
                        ),
                        rx.vstack(
                            rx.icon("search-x", size=40, color=rx.color("gray", 6)),
                            rx.text(
                                "Ничего не подошло.",
                                size="3",
                                weight="medium",
                                color=rx.color("gray", 11),
                            ),
                            rx.text(
                                "Попробуйте изменить фильтры или сбросить поиск.",
                                size="2",
                                color=rx.color("gray", 9),
                            ),
                            rx.button(
                                "Сбросить фильтры",
                                on_click=ListingState.reset_filters,
                                variant="soft",
                                size="2",
                            ),
                            align_items="center",
                            spacing="2",
                            padding_y="3rem",
                            width="100%",
                        ),
                    ),
                ),
                # ── Pagination ──
                rx.cond(
                    ListingState.listings_total_pages > 1,
                    rx.hstack(
                        rx.button(
                            rx.icon("chevron-left", size=16),
                            on_click=ListingState.listings_prev_page,
                            variant="soft",
                            size="2",
                            disabled=ListingState.listings_page <= 1,
                        ),
                        rx.hstack(
                            rx.text(
                                "Страница ",
                                size="2",
                                color=rx.color("gray", 10),
                            ),
                            rx.badge(
                                ListingState.listings_page,
                                color_scheme="indigo",
                                variant="soft",
                            ),
                            rx.text(
                                " из ",
                                ListingState.listings_total_pages,
                                size="2",
                                color=rx.color("gray", 10),
                            ),
                            spacing="1",
                            align="center",
                        ),
                        rx.button(
                            rx.icon("chevron-right", size=16),
                            on_click=ListingState.listings_next_page,
                            variant="soft",
                            size="2",
                            disabled=ListingState.listings_page >= ListingState.listings_total_pages,
                        ),
                        spacing="3",
                        align_items="center",
                        width="100%",
                        justify="center",
                        padding_top="0.5rem",
                    ),
                    rx.fragment(),
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
