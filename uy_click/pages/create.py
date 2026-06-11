import reflex as rx

from uy_click.components.footer import site_footer
from uy_click.components.navbar import navbar
from uy_click.i18n import t
from uy_click.state.listing_state import ListingState


def create() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading(t("create_page_title"), size="7"),
                rx.text(t("create_page_subtitle"), size="2", color=rx.color("gray", 10)),
                rx.input(
                    placeholder=t("create_ph_title"),
                    value=ListingState.title,
                    on_change=ListingState.set_title,
                ),
                rx.input(
                    placeholder=t("create_ph_district"),
                    value=ListingState.district,
                    on_change=ListingState.set_district,
                ),
                rx.input(
                    placeholder=t("create_ph_rooms"),
                    type="number",
                    min=1,
                    value=ListingState.rooms,
                    on_change=ListingState.set_rooms,
                ),
                rx.input(
                    placeholder=t("create_ph_price"),
                    type="number",
                    min=0,
                    value=ListingState.price,
                    on_change=ListingState.set_price,
                ),
                rx.hstack(
                    rx.badge(t("common_normal"), color_scheme="gray", variant="soft"),
                    rx.badge(t("create_premium_soon"), color_scheme="amber", variant="outline"),
                    spacing="2",
                    align_items="center",
                ),
                rx.text(t("create_premium_note"), size="1", color=rx.color("gray", 9)),
                rx.text(t("create_location_label"), size="2", color=rx.color("gray", 10)),
                rx.hstack(
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
                    spacing="2",
                    width="100%",
                    align_items="stretch",
                ),
                rx.text(t("create_photo_label"), size="2", color=rx.color("gray", 10)),
                rx.upload(
                    rx.text(t("create_photo_drop"), size="2", color=rx.color("gray", 11)),
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
                            alt="preview",
                        ),
                        rx.button(
                            t("create_photo_remove"),
                            variant="soft",
                            on_click=ListingState.clear_create_photo,
                        ),
                        spacing="2",
                        align_items="start",
                        width="100%",
                    ),
                    rx.fragment(),
                ),
                rx.button(t("create_btn_publish"), on_click=ListingState.add_listing, color_scheme="teal"),
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
