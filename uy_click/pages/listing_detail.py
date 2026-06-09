import reflex as rx

from uy_click.components.footer import site_footer
from uy_click.components.navbar import navbar
from uy_click.state.chat_state import ChatState
from uy_click.state.listing_state import ListingState
from uy_click.utils.helpers import format_price_uzs


def listing_detail() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.link(
                    "← К объявлениям",
                    href="/listings",
                    size="2",
                    color=rx.color("blue", 11),
                ),
                rx.cond(
                    ListingState.error_message,
                    rx.callout(ListingState.error_message, color_scheme="red"),
                    rx.fragment(),
                ),
                rx.cond(
                    ListingState.detail_id > 0,
                    rx.card(
                        rx.vstack(
                            rx.cond(
                                ListingState.detail_image_url != "",
                                rx.image(
                                    src=ListingState.detail_image_url,
                                    width="100%",
                                    max_height="360px",
                                    object_fit="cover",
                                    border_radius="md",
                                    alt=ListingState.detail_title,
                                ),
                                rx.box(
                                    rx.center(
                                        rx.text(
                                            "Нет фото",
                                            size="2",
                                            color=rx.color("gray", 9),
                                        ),
                                        width="100%",
                                        height="200px",
                                    ),
                                    width="100%",
                                    height="200px",
                                    background=rx.color("gray", 3),
                                    border_radius="md",
                                ),
                            ),
                            rx.hstack(
                                rx.heading(ListingState.detail_title, size="7"),
                                rx.cond(
                                    ListingState.detail_is_premium,
                                    rx.badge("PREMIUM", color_scheme="amber", variant="solid"),
                                    rx.fragment(),
                                ),
                                spacing="2",
                                align_items="center",
                                flex_wrap="wrap",
                            ),
                            rx.hstack(
                                rx.text(ListingState.detail_district, weight="medium"),
                                rx.text("·", color=rx.color("gray", 9)),
                                rx.text(ListingState.detail_rooms, weight="medium"),
                                rx.text("комн.", color=rx.color("gray", 11)),
                                spacing="2",
                                align_items="center",
                            ),
                            rx.badge(
                                format_price_uzs(ListingState.detail_price),
                                color_scheme="green",
                                size="3",
                                variant="soft",
                            ),
                            rx.cond(
                                ListingState.detail_has_location,
                                rx.link(
                                    "Показать на карте",
                                    href="/map",
                                    size="2",
                                    color=rx.color("blue", 11),
                                ),
                                rx.fragment(),
                            ),
                            rx.hstack(
                                rx.button(
                                    rx.cond(
                                        ListingState.favorite_listing_ids.contains(
                                            ListingState.detail_id
                                        ),
                                        "Убрать из избранного",
                                        "В избранное",
                                    ),
                                    on_click=ListingState.toggle_favorite(
                                        ListingState.detail_id
                                    ),
                                    variant="soft",
                                ),
                                rx.button(
                                    "Написать",
                                    on_click=ChatState.create_chat_with_user(
                                        ListingState.detail_owner_id
                                    ),
                                    variant="soft",
                                ),
                                spacing="2",
                            ),
                            spacing="4",
                            align_items="stretch",
                        ),
                        width="100%",
                        max_width="640px",
                    ),
                    rx.vstack(
                        rx.heading("Объявление не найдено", size="6"),
                        rx.text(
                            "Возможно, оно удалено или ссылка неверная.",
                            color=rx.color("gray", 10),
                            size="2",
                        ),
                        rx.link(
                            "Все объявления",
                            href="/listings",
                            color=rx.color("blue", 11),
                        ),
                        spacing="2",
                        align_items="start",
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
    )
