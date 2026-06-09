import reflex as rx

from uy_click.components.bento import bento_hero, bento_tile
from uy_click.components.footer import site_footer
from uy_click.components.navbar import navbar


def index() -> rx.Component:
    hero_actions = rx.hstack(
        rx.button(
            "Смотреть объявления",
            on_click=rx.redirect("/listings"),
            size="3",
            color_scheme="indigo",
        ),
        rx.button(
            "Подать объявление",
            on_click=rx.redirect("/create"),
            size="3",
            variant="soft",
            color_scheme="gray",
        ),
        spacing="3",
        flex_wrap="wrap",
    )

    return rx.vstack(
        navbar(),
        rx.box(
            rx.container(
                rx.vstack(
                    bento_hero(
                        title="Аренда жилья без посредников",
                        subtitle="Снимайте и сдавайте напрямую — объявления, чат и избранное в одном месте. Без комиссий риелтору.",
                        child=hero_actions,
                    ),
                    rx.grid(
                        bento_tile(
                            title="Объявления",
                            subtitle="Фильтры по району, цене и комнатам. Сортировка и постраничная лента.",
                            icon_tag="layout-grid",
                            accent="indigo",
                            child=rx.link(
                                rx.button("Открыть ленту", variant="soft", size="2"),
                                href="/listings",
                                underline="none",
                            ),
                        ),
                        bento_tile(
                            title="Карта",
                            subtitle="Точки на карте для объявлений с координатами — ориентир по району.",
                            icon_tag="map",
                            accent="blue",
                            child=rx.link(
                                rx.button("На карту", variant="soft", size="2"),
                                href="/map",
                                underline="none",
                            ),
                        ),
                        bento_tile(
                            title="Чаты",
                            subtitle="Пишите владельцу прямо из карточки. Диалоги в одном разделе.",
                            icon_tag="message-circle",
                            accent="cyan",
                            child=rx.link(
                                rx.button("К чатам", variant="soft", size="2"),
                                href="/chats",
                                underline="none",
                            ),
                        ),
                        bento_tile(
                            title="Избранное",
                            subtitle="Сохраняйте понравившиеся варианты и возвращайтесь к ним позже.",
                            icon_tag="heart",
                            accent="crimson",
                            child=rx.link(
                                rx.button("Избранное", variant="soft", size="2"),
                                href="/favorites",
                                underline="none",
                            ),
                        ),
                        columns=rx.breakpoints(initial="1", sm="2", lg="4"),
                        spacing="4",
                        width="100%",
                    ),
                    rx.grid(
                        bento_tile(
                            title="Новое объявление",
                            subtitle="Фото, район, цена и координаты — публикация за пару минут.",
                            icon_tag="circle-plus",
                            accent="grass",
                            min_height="160px",
                            child=rx.link(
                                rx.button("Создать", color_scheme="indigo", size="2"),
                                href="/create",
                                underline="none",
                            ),
                        ),
                        bento_tile(
                            title="Мои объявления",
                            subtitle="Редактирование, снятие с публикации и обложка в пару кликов.",
                            icon_tag="folder-open",
                            accent="orange",
                            min_height="160px",
                            child=rx.link(
                                rx.button("Мои лоты", variant="soft", size="2"),
                                href="/my-listings",
                                underline="none",
                            ),
                        ),
                        columns=rx.breakpoints(initial="1", md="2"),
                        spacing="4",
                        width="100%",
                    ),
                    spacing="5",
                    width="100%",
                    padding_y="1.5rem",
                    padding_bottom="2.5rem",
                ),
                size="4",
            ),
            width="100%",
            background=rx.color("gray", 2),
        ),
        site_footer(),
        width="100%",
        min_height="100vh",
        align_items="stretch",
        background=rx.color("gray", 2),
    )
