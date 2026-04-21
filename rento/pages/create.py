import reflex as rx

from rento.components.footer import site_footer
from rento.components.navbar import navbar
from rento.state.listing_state import ListingState


def create() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Новое объявление", size="7"),
                rx.text(
                    "Кратко опишите жильё — так откликнутся быстрее.",
                    size="2",
                    color=rx.color("gray", 10),
                ),
                rx.input(
                    placeholder="Заголовок, например: 1-комнатная у метро",
                    value=ListingState.title,
                    on_change=ListingState.set_title,
                ),
                rx.input(
                    placeholder="Район",
                    value=ListingState.district,
                    on_change=ListingState.set_district,
                ),
                rx.input(
                    placeholder="Комнат",
                    type="number",
                    min=1,
                    value=ListingState.rooms,
                    on_change=ListingState.set_rooms,
                ),
                rx.input(
                    placeholder="Цена в сумах в месяц",
                    type="number",
                    min=0,
                    value=ListingState.price,
                    on_change=ListingState.set_price,
                ),
                rx.vstack(
                    rx.text("Тип размещения", size="2", color=rx.color("gray", 10)),
                    rx.hstack(
                        rx.badge(
                            rx.cond(ListingState.create_is_premium, "Премиум", "Обычное"),
                            color_scheme=rx.cond(
                                ListingState.create_is_premium, "amber", "gray"
                            ),
                            variant="soft",
                        ),
                        rx.button(
                            rx.cond(
                                ListingState.create_is_premium,
                                "Сделать обычным",
                                "Сделать премиум",
                            ),
                            on_click=ListingState.toggle_create_is_premium,
                            variant="soft",
                            color_scheme=rx.cond(
                                ListingState.create_is_premium, "gray", "amber"
                            ),
                            size="2",
                        ),
                        spacing="2",
                        align_items="center",
                    ),
                    rx.text(
                        "Премиум-объявления показываются выше в ленте.",
                        size="1",
                        color=rx.color("gray", 9),
                    ),
                    spacing="1",
                    align_items="start",
                ),
                rx.text(
                    "Точка на карте (необязательно)",
                    size="2",
                    color=rx.color("gray", 10),
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Широта, напр. 41.31",
                        value=ListingState.create_latitude,
                        on_change=ListingState.set_create_latitude,
                    ),
                    rx.input(
                        placeholder="Долгота, напр. 69.28",
                        value=ListingState.create_longitude,
                        on_change=ListingState.set_create_longitude,
                    ),
                    spacing="2",
                    width="100%",
                    align_items="stretch",
                ),
                rx.text(
                    "Обложка (необязательно)",
                    size="2",
                    color=rx.color("gray", 10),
                ),
                rx.upload(
                    rx.text(
                        "Перетащите фото сюда или нажмите для выбора (до 5 МБ)",
                        size="2",
                        color=rx.color("gray", 11),
                    ),
                    id="listing-photo-create",
                    multiple=False,
                    max_size=5_000_000,
                    accept={
                        "image/jpeg": [".jpg", ".jpeg"],
                        "image/png": [".png"],
                        "image/webp": [".webp"],
                    },
                    on_drop=ListingState.upload_create_photo,
                    padding="1.25rem",
                ),
                rx.cond(
                    ListingState.pending_image_url != "",
                    rx.vstack(
                        rx.image(
                            src=ListingState.pending_image_url,
                            max_height="200px",
                            width="100%",
                            object_fit="cover",
                            border_radius="md",
                            alt="Превью обложки",
                        ),
                        rx.button(
                            "Убрать фото",
                            variant="soft",
                            on_click=ListingState.clear_create_photo,
                        ),
                        spacing="2",
                        align_items="start",
                        width="100%",
                    ),
                    rx.fragment(),
                ),
                rx.button("Опубликовать", on_click=ListingState.add_listing),
                rx.cond(
                    ListingState.success_message,
                    rx.callout(ListingState.success_message, color_scheme="green"),
                    rx.fragment(),
                ),
                rx.cond(
                    ListingState.error_message,
                    rx.callout(ListingState.error_message, color_scheme="red"),
                    rx.fragment(),
                ),
                width="100%",
                max_width="520px",
                align_items="stretch",
                spacing="3",
                padding_y="2rem",
            )
        ),
        site_footer(),
        width="100%",
        align_items="stretch",
    )
