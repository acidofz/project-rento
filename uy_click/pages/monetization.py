import reflex as rx

from uy_click.components.footer import site_footer
from uy_click.components.navbar import navbar


def _stream(title: str, body: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(title, size="4"),
            rx.text(body, size="2", color=rx.color("gray", 11), line_height="1.55"),
            align_items="start",
            spacing="2",
            width="100%",
        ),
        variant="surface",
        size="3",
        width="100%",
    )


def monetization() -> rx.Component:
    streams = rx.grid(
        _stream(
            "Премиум-объявление",
            "Платное выделение или продвижение объявления в ленте и на карте. "
            "Ориентир цены в продуктовой модели — порядка $2–5 за размещение/пакет.",
        ),
        _stream(
            "PRO-подписка",
            "Подписка для арендодателей: расширенные лимиты, статистика просмотров, "
            "приоритет в выдаче — по мере зрелости продукта.",
        ),
        _stream(
            "Генерация договора",
            "Сервис автоматического черновика договора аренды (шаблоны, подстановка реквизитов) "
            "как отдельная опция или часть PRO.",
        ),
        _stream(
            "Комиссия с транзакций",
            "Небольшая комиссия с оплачиваемых через платформу сделок (в питче — ориентир 2–3%). "
            "Рассматривается как этап после набора доверия и объёма, не с первого дня.",
        ),
        _stream(
            "Реклама смежных услуг",
            "Нативная или баннерная реклама партнёров: мебель, ремонт, переезды, бытовая техника.",
        ),
        _stream(
            "Страхование",
            "Партнёрские программы со страховщиками (имущество, ответственность) — доход через "
            "реферальные или агентские модели.",
        ),
        columns=rx.breakpoints(initial="1", sm="2"),
        spacing="4",
        width="100%",
    )

    return rx.vstack(
        navbar(),
        rx.box(
            rx.container(
                rx.vstack(
                    rx.heading("Бизнес-модель и доход", size="7"),
                    rx.callout(
                        "Ниже — планируемые потоки дохода (дорожная карта монетизации). "
                        "В текущем MVP большинство из них не реализовано как оплата в приложении.",
                        icon="info",
                        color_scheme="blue",
                        variant="soft",
                        width="100%",
                    ),
                    rx.text(
                        "UY-CLICK остаётся платформой прямой аренды без обязательного посредника. "
                        "Монетизация не должна ломать ценность «снять/сдать напрямую».",
                        size="2",
                        color=rx.color("gray", 10),
                    ),
                    rx.heading("Шесть направлений", size="5", margin_top="0.5rem"),
                    streams,
                    spacing="4",
                    align_items="start",
                    padding_y="2rem",
                    width="100%",
                ),
                size="3",
            ),
            width="100%",
            flex_grow="1",
            background=rx.color("gray", 2),
        ),
        site_footer(),
        width="100%",
        min_height="100vh",
        align_items="stretch",
        background=rx.color("gray", 2),
    )
