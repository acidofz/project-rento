import reflex as rx

from rento.components.listing_card import listing_card
from rento.components.footer import site_footer
from rento.components.navbar import navbar
from rento.state.chat_state import ChatState
from rento.state.listing_state import ListingState


def listing_card_with_favorite(listing) -> rx.Component:
    return rx.vstack(
        listing_card(listing),
        rx.button(
            rx.cond(
                ListingState.favorite_listing_ids.contains(listing.id),
                "Убрать из избранного",
                "В избранное",
            ),
            on_click=ListingState.toggle_favorite(listing.id),
            variant="soft",
        ),
        rx.button(
            "Написать",
            on_click=ChatState.create_chat_with_user(listing.owner_id),
            variant="soft",
        ),
        spacing="2",
        width="100%",
    )


def listings() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.hstack(
                    rx.heading("Объявления", size="7"),
                    rx.spacer(),
                    rx.button("Обновить", on_click=ListingState.load_listings, variant="soft"),
                    rx.button("Карта", on_click=rx.redirect("/map"), variant="soft"),
                    rx.button("Сбросить фильтры", on_click=ListingState.reset_filters, variant="soft"),
                    rx.select(
                        ["newest", "price_asc", "price_desc", "rooms_desc"],
                        value=ListingState.sort_by,
                        on_change=ListingState.set_sort_by,
                    ),
                    rx.input(
                        placeholder="Поиск по району или названию",
                        value=ListingState.search_query,
                        on_change=ListingState.set_search_query,
                        max_width="300px",
                    ),
                    width="100%",
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Район",
                        value=ListingState.filter_district,
                        on_change=ListingState.set_filter_district,
                    ),
                    rx.input(
                        placeholder="Мин. цена",
                        type="number",
                        min=0,
                        value=ListingState.min_price,
                        on_change=ListingState.set_min_price,
                    ),
                    rx.input(
                        placeholder="Макс. цена",
                        type="number",
                        min=0,
                        value=ListingState.max_price,
                        on_change=ListingState.set_max_price,
                    ),
                    rx.input(
                        placeholder="Мин. комнат",
                        type="number",
                        min=0,
                        value=ListingState.min_rooms,
                        on_change=ListingState.set_min_rooms,
                    ),
                    rx.input(
                        placeholder="Макс. комнат",
                        type="number",
                        min=0,
                        value=ListingState.max_rooms,
                        on_change=ListingState.set_max_rooms,
                    ),
                    width="100%",
                ),
                rx.cond(
                    ListingState.error_message,
                    rx.callout(ListingState.error_message, color_scheme="red"),
                    rx.fragment(),
                ),
                rx.hstack(
                    rx.text("Найдено:", size="2", color=rx.color("gray", 10)),
                    rx.text(
                        ListingState.listings_filtered_count,
                        size="2",
                        weight="bold",
                    ),
                    rx.spacer(),
                    width="100%",
                    align_items="center",
                ),
                rx.cond(
                    ListingState.has_filtered_listings,
                    rx.grid(
                        rx.foreach(
                            ListingState.paginated_filtered_listings,
                            listing_card_with_favorite,
                        ),
                        columns="2",
                        spacing="4",
                        width="100%",
                    ),
                    rx.text(
                        "Ничего не подошло. Сбросьте фильтры или измените поиск.",
                        color=rx.color("gray", 10),
                    ),
                ),
                rx.cond(
                    ListingState.listings_total_pages > 1,
                    rx.hstack(
                        rx.button(
                            "Назад",
                            on_click=ListingState.listings_prev_page,
                            variant="soft",
                            disabled=ListingState.listings_page <= 1,
                        ),
                        rx.text(
                            ListingState.listings_page,
                            " / ",
                            ListingState.listings_total_pages,
                            size="2",
                            color=rx.color("gray", 11),
                        ),
                        rx.button(
                            "Вперёд",
                            on_click=ListingState.listings_next_page,
                            variant="soft",
                            disabled=ListingState.listings_page >= ListingState.listings_total_pages,
                        ),
                        spacing="3",
                        align_items="center",
                        width="100%",
                        justify="center",
                        padding_top="2",
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
