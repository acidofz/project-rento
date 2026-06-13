import reflex as rx

from uy_click.components.footer import site_footer
from uy_click.components.navbar import navbar
from uy_click.i18n import t
from uy_click.state.listing_state import ListingState


def _field(label_key: str, control: rx.Component) -> rx.Component:
    return rx.vstack(
        rx.text(t(label_key), size="2", weight="medium", color=rx.color("gray", 11)),
        control,
        spacing="1",
        align_items="stretch",
        width="100%",
    )


def create() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.vstack(
                    rx.heading(t("create_page_title"), size="7"),
                    rx.text(t("create_page_subtitle"), size="2", color=rx.color("gray", 10)),
                    spacing="1",
                    align_items="start",
                ),
                rx.card(
                    rx.vstack(
                        _field(
                            "create_ph_title",
                            rx.input(
                                placeholder=t("create_ph_title"),
                                value=ListingState.title,
                                on_change=ListingState.set_title,
                            ),
                        ),
                        rx.grid(
                            _field(
                                "create_ph_district",
                                rx.input(
                                    placeholder=t("create_ph_district"),
                                    value=ListingState.district,
                                    on_change=ListingState.set_district,
                                ),
                            ),
                            _field(
                                "create_ph_rooms",
                                rx.input(
                                    placeholder=t("create_ph_rooms"),
                                    type="number",
                                    min=1,
                                    value=ListingState.rooms,
                                    on_change=ListingState.set_rooms,
                                ),
                            ),
                            columns="2",
                            spacing="3",
                            width="100%",
                        ),
                        _field(
                            "create_ph_price",
                            rx.input(
                                placeholder=t("create_ph_price"),
                                type="number",
                                min=0,
                                value=ListingState.price,
                                on_change=ListingState.set_price,
                            ),
                        ),
                        _field(
                            "create_phone_label",
                            rx.input(
                                placeholder=t("create_ph_phone"),
                                type="tel",
                                value=ListingState.create_phone,
                                on_change=ListingState.set_create_phone,
                            ),
                        ),
                        spacing="4",
                        align_items="stretch",
                        width="100%",
                    ),
                    variant="surface",
                    size="3",
                    width="100%",
                ),
                rx.card(
                    rx.vstack(
                        rx.text(t("create_photo_label"), size="2", weight="medium", color=rx.color("gray", 11)),
                        rx.upload(
                            rx.vstack(
                                rx.icon("upload", size=24, color=rx.color("gray", 8)),
                                rx.text(t("create_photo_drop"), size="2", color=rx.color("gray", 9), text_align="center"),
                                spacing="2",
                                align_items="center",
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
                            padding="1.5rem",
                            width="100%",
                            border=f"2px dashed {rx.color('gray', 5)}",
                            border_radius="var(--radius-3)",
                            _hover={"border_color": rx.color("teal", 6), "background": rx.color("teal", 2)},
                            style={"cursor": "pointer", "transition": "all 150ms ease"},
                        ),
                        rx.cond(
                            ListingState.pending_image_url != "",
                            rx.vstack(
                                rx.image(
                                    src=ListingState.pending_image_url,
                                    max_height="220px",
                                    width="100%",
                                    object_fit="cover",
                                    border_radius="var(--radius-3)",
                                    alt="preview",
                                ),
                                rx.button(
                                    rx.icon("x", size=14),
                                    t("create_photo_remove"),
                                    variant="soft",
                                    color_scheme="gray",
                                    size="1",
                                    on_click=ListingState.clear_create_photo,
                                ),
                                spacing="2",
                                align_items="start",
                                width="100%",
                            ),
                            rx.fragment(),
                        ),
                        spacing="3",
                        align_items="stretch",
                        width="100%",
                    ),
                    variant="surface",
                    size="3",
                    width="100%",
                ),
                rx.card(
                    rx.vstack(
                        rx.text(t("create_location_label"), size="2", weight="medium", color=rx.color("gray", 11)),
                        rx.grid(
                            rx.input(
                                placeholder=t("create_ph_lat"),
                                value=ListingState.create_latitude,
                                on_change=ListingState.set_create_latitude,
                            ),
                            rx.input(
                                placeholder=t("create_ph_lng"),
                                value=ListingState.create_longitude,
                                on_change=ListingState.set_create_longitude,
                            ),
                            columns="2",
                            spacing="3",
                            width="100%",
                        ),
                        spacing="2",
                        align_items="stretch",
                        width="100%",
                    ),
                    variant="surface",
                    size="3",
                    width="100%",
                ),
                rx.hstack(
                    rx.button(
                        rx.icon("send", size=16),
                        t("create_btn_publish"),
                        on_click=ListingState.add_listing,
                        color_scheme="teal",
                        size="3",
                        style={"font_weight": "600"},
                    ),
                    rx.hstack(
                        rx.badge(t("common_normal"), color_scheme="gray", variant="soft"),
                        rx.badge(t("create_premium_soon"), color_scheme="amber", variant="outline"),
                        spacing="2",
                        align_items="center",
                    ),
                    spacing="3",
                    flex_wrap="wrap",
                    align_items="center",
                    width="100%",
                ),
                rx.cond(
                    ListingState.success_message,
                    rx.callout(
                        rx.hstack(rx.icon("check-circle", size=16), ListingState.success_message, spacing="2", align="center"),
                        color_scheme="green",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    ListingState.error_message,
                    rx.callout(ListingState.error_message, color_scheme="red"),
                    rx.fragment(),
                ),
                width="100%",
                max_width="560px",
                align_items="stretch",
                spacing="4",
                padding_y="2rem",
            )
        ),
        site_footer(),
        width="100%",
        align_items="stretch",
        background=rx.color("gray", 1),
    )
