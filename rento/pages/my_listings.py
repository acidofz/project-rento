import reflex as rx

from rento.components.listing_card import listing_card
from rento.components.footer import site_footer
from rento.components.navbar import navbar
from rento.state.listing_state import ListingState


def my_listing_card(listing) -> rx.Component:
    return rx.vstack(
        listing_card(listing),
        rx.hstack(
            rx.button("Редактировать", on_click=ListingState.start_edit(listing.id), variant="soft"),
            rx.button(
                "Удалить",
                on_click=ListingState.delete_listing(listing.id),
                color_scheme="red",
                variant="soft",
            ),
            spacing="2",
            width="100%",
        ),
        spacing="2",
        width="100%",
    )


def my_listings() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.hstack(
                    rx.heading("Мои объявления", size="7"),
                    rx.spacer(),
                    rx.button("Обновить", on_click=ListingState.load_my_listings, variant="soft"),
                    width="100%",
                ),
                rx.text(
                    "Редактируйте или снимайте с публикации — изменения сразу видны в общем списке.",
                    size="2",
                    color=rx.color("gray", 10),
                    width="100%",
                ),
                rx.cond(
                    ListingState.error_message,
                    rx.callout(ListingState.error_message, color_scheme="red"),
                    rx.fragment(),
                ),
                rx.cond(
                    ListingState.success_message,
                    rx.callout(ListingState.success_message, color_scheme="green"),
                    rx.fragment(),
                ),
                rx.cond(
                    ListingState.is_editing,
                    rx.card(
                        rx.vstack(
                            rx.heading("Редактирование", size="5"),
                            rx.input(
                                placeholder="Заголовок",
                                value=ListingState.edit_title,
                                on_change=ListingState.set_edit_title,
                            ),
                            rx.input(
                                placeholder="Район",
                                value=ListingState.edit_district,
                                on_change=ListingState.set_edit_district,
                            ),
                            rx.input(
                                placeholder="Комнат",
                                type="number",
                                min=1,
                                value=ListingState.edit_rooms,
                                on_change=ListingState.set_edit_rooms,
                            ),
                            rx.input(
                                placeholder="Цена в сумах в месяц",
                                type="number",
                                min=1,
                                value=ListingState.edit_price,
                                on_change=ListingState.set_edit_price,
                            ),
                            rx.text(
                                "Точка на карте",
                                size="2",
                                color=rx.color("gray", 10),
                            ),
                            rx.hstack(
                                rx.input(
                                    placeholder="Широта",
                                    value=ListingState.edit_latitude,
                                    on_change=ListingState.set_edit_latitude,
                                ),
                                rx.input(
                                    placeholder="Долгота",
                                    value=ListingState.edit_longitude,
                                    on_change=ListingState.set_edit_longitude,
                                ),
                                spacing="2",
                                width="100%",
                                align_items="stretch",
                            ),
                            rx.text(
                                "Обложка",
                                size="2",
                                color=rx.color("gray", 10),
                            ),
                            rx.upload(
                                rx.text(
                                    "Заменить обложку — перетащите или выберите файл",
                                    size="2",
                                    color=rx.color("gray", 11),
                                ),
                                id="listing-photo-edit",
                                multiple=False,
                                max_size=5_000_000,
                                accept={
                                    "image/jpeg": [".jpg", ".jpeg"],
                                    "image/png": [".png"],
                                    "image/webp": [".webp"],
                                },
                                on_drop=ListingState.upload_edit_photo,
                                padding="1.25rem",
                            ),
                            rx.cond(
                                ListingState.edit_image_url != "",
                                rx.vstack(
                                    rx.image(
                                        src=ListingState.edit_image_url,
                                        max_height="200px",
                                        width="100%",
                                        object_fit="cover",
                                        border_radius="md",
                                        alt="Текущая обложка",
                                    ),
                                    rx.button(
                                        "Убрать фото",
                                        variant="soft",
                                        on_click=ListingState.clear_edit_photo,
                                    ),
                                    spacing="2",
                                    align_items="start",
                                    width="100%",
                                ),
                                rx.fragment(),
                            ),
                            rx.hstack(
                                rx.button("Сохранить", on_click=ListingState.save_edit),
                                rx.button("Отменить", on_click=ListingState.cancel_edit, variant="soft"),
                                spacing="2",
                            ),
                            spacing="3",
                            align_items="stretch",
                        ),
                        width="100%",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    ListingState.my_listings,
                    rx.grid(
                        rx.foreach(ListingState.my_listings, my_listing_card),
                        columns="2",
                        spacing="4",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text(
                            "Пока нет объявлений.",
                            color=rx.color("gray", 11),
                        ),
                        rx.link(
                            "Подать объявление",
                            href="/create",
                            color=rx.color("blue", 11),
                        ),
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
