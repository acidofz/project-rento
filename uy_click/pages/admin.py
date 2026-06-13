import reflex as rx

from uy_click.components.footer import site_footer
from uy_click.components.navbar import navbar
from uy_click.state.admin_state import AdminState


def listing_row(item) -> rx.Component:
    return rx.hstack(
        rx.text(f"#{item['id']}"),
        rx.text(item["title"]),
        rx.text(item["district"], color=rx.color("gray", 10)),
        rx.spacer(),
        rx.text(str(item["price"])),
        rx.button(
            "Удалить",
            on_click=AdminState.delete_listing_as_admin(item["id"]),
            color_scheme="red",
            variant="soft",
        ),
        width="100%",
    )


def user_row(item) -> rx.Component:
    return rx.hstack(
        rx.text(
            rx.cond(
                item["username"],
                item["username"],
                rx.cond(item["email"], item["email"], item["id"]),
            )
        ),
        rx.text(item["id"], color=rx.color("gray", 10)),
        rx.spacer(),
        rx.badge(
            rx.cond(item["is_blocked"], "Заблокирован", "Активен"),
            color_scheme=rx.cond(item["is_blocked"], "red", "green"),
            variant="soft",
        ),
        rx.cond(
            item["is_blocked"],
            rx.button(
                "Разблокировать",
                on_click=AdminState.set_user_block_status(item["id"], False),
                color_scheme="green",
                variant="soft",
            ),
            rx.button(
                "Блокировать",
                on_click=AdminState.set_user_block_status(item["id"], True),
                color_scheme="red",
                variant="soft",
            ),
        ),
        width="100%",
    )


def admin() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.hstack(
                    rx.heading("Админ-панель", size="7"),
                    rx.spacer(),
                    rx.button("Обновить", on_click=AdminState.load_admin_dashboard, variant="soft"),
                    width="100%",
                ),
                rx.text(
                    "Сводка, модерация объявлений и сообщений, статусы пользователей.",
                    size="2",
                    color=rx.color("gray", 10),
                    width="100%",
                ),
                rx.cond(
                    AdminState.error_message,
                    rx.callout(AdminState.error_message, color_scheme="red"),
                    rx.fragment(),
                ),
                rx.cond(
                    AdminState.success_message,
                    rx.callout(AdminState.success_message, color_scheme="green"),
                    rx.fragment(),
                ),
                rx.cond(
                    AdminState.is_admin,
                    rx.vstack(
                        rx.grid(
                            rx.card(
                                rx.vstack(
                                    rx.text("Пользователи", color=rx.color("gray", 10)),
                                    rx.heading(AdminState.users_count, size="7"),
                                    align_items="start",
                                )
                            ),
                            rx.card(
                                rx.vstack(
                                    rx.text("Объявления", color=rx.color("gray", 10)),
                                    rx.heading(AdminState.listings_count, size="7"),
                                    align_items="start",
                                )
                            ),
                            columns=rx.breakpoints(initial="1", sm="2"),
                            spacing="4",
                            width="100%",
                        ),
                        rx.card(
                            rx.vstack(
                                rx.heading("Последние объявления", size="5"),
                                rx.foreach(AdminState.latest_listings, listing_row),
                                spacing="2",
                                width="100%",
                                align_items="stretch",
                            ),
                            width="100%",
                        ),
                        rx.card(
                            rx.vstack(
                                rx.heading("Пользователи", size="5"),
                                rx.foreach(AdminState.latest_users, user_row),
                                spacing="2",
                                width="100%",
                                align_items="stretch",
                            ),
                            width="100%",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    rx.text(
                        "Эта страница только для администраторов.",
                        color=rx.color("gray", 11),
                    ),
                ),
                spacing="4",
                width="100%",
                padding_y="2rem",
            ),
            size="4",
        ),
        site_footer(),
        width="100%",
        min_height="100vh",
        align_items="stretch",
    )
