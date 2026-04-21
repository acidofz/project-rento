import reflex as rx

from rento.components.footer import site_footer
from rento.components.navbar import navbar
from rento.state.auth_state import AuthState


class PricingPreviewState(rx.State):
    """UI-only state for pricing preview toggle."""

    billing_cycle: str = "month"

    def set_billing_cycle(self, cycle: str) -> None:
        self.billing_cycle = cycle


def _feature_item(label: str, included: bool) -> rx.Component:
    return rx.hstack(
        rx.cond(
            included,
            rx.icon(tag="check", size=16, color=rx.color("grass", 10)),
            rx.icon(tag="x", size=16, color=rx.color("gray", 9)),
        ),
        rx.text(label, size="2", color=rx.color("gray", 11)),
        spacing="2",
        align_items="center",
    )


def _animated_button(
    text: str,
    *,
    size: str = "2",
    variant: str = "soft",
    color_scheme: str = "gray",
    on_click: object | None = None,
    disabled: bool = False,
) -> rx.Component:
    return rx.button(
        text,
        size=size,
        variant=variant,
        color_scheme=color_scheme,
        on_click=on_click,
        disabled=disabled,
        style={"transition": "all 160ms ease"},
        _hover={
            "transform": "translateY(-1px)",
            "box_shadow": "0 8px 18px -10px rgba(0, 0, 0, 0.25)",
        },
        _active={"transform": "translateY(0) scale(0.98)"},
    )


def _plan_card(
    *,
    name: str,
    subtitle_badge: rx.Component,
    price_block: rx.Component,
    description: str,
    features: list[rx.Component],
    cta: rx.Component,
    background: str,
    border_style: str,
) -> rx.Component:
    return rx.card(
        rx.vstack(
            subtitle_badge,
            rx.heading(name, size="6"),
            price_block,
            rx.text(description, size="2", color=rx.color("gray", 11)),
            rx.vstack(
                *features,
                spacing="2",
                align_items="start",
                width="100%",
            ),
            cta,
            align_items="start",
            spacing="3",
            width="100%",
        ),
        variant="surface",
        size="3",
        width="100%",
        background=background,
        style={
            "border": border_style,
            "transition": "transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease",
            "box_shadow": "0 2px 12px -6px rgba(0, 0, 0, 0.12)",
        },
        _hover={
            "transform": "translateY(-3px)",
            "box_shadow": "0 16px 30px -16px rgba(0, 0, 0, 0.25)",
        },
        _active={"transform": "translateY(-1px) scale(0.997)"},
    )


def _comparison_row(feature: str, free_included: bool, pro_included: bool) -> rx.Component:
    return rx.hstack(
        rx.text(feature, size="2", color=rx.color("gray", 11)),
        rx.spacer(),
        rx.badge(
            rx.cond(free_included, "Есть", "Нет"),
            color_scheme=rx.cond(free_included, "grass", "gray"),
            variant="soft",
        ),
        rx.badge(
            rx.cond(pro_included, "Есть", "Нет"),
            color_scheme=rx.cond(pro_included, "grass", "gray"),
            variant="soft",
        ),
        width="100%",
        align_items="center",
    )


def profile() -> rx.Component:
    pro_price = rx.vstack(
        rx.hstack(
            rx.text(
                rx.cond(
                    PricingPreviewState.billing_cycle == "month",
                    "$12 / мес",
                    "$115 / год",
                ),
                size="2",
                color=rx.color("gray", 10),
            ),
            rx.cond(
                PricingPreviewState.billing_cycle == "year",
                rx.badge("Экономия 20%", color_scheme="grass", variant="soft"),
                rx.fragment(),
            ),
            spacing="2",
            align_items="center",
            flex_wrap="wrap",
        ),
        rx.text(
            rx.cond(
                PricingPreviewState.billing_cycle == "month",
                "Оплата ежемесячно, можно отменить в любой момент.",
                "Эквивалент $9.6 в месяц при оплате за год.",
            ),
            size="1",
            color=rx.color("gray", 9),
        ),
        align_items="start",
        spacing="1",
        width="100%",
    )

    free_card = _plan_card(
        name="Free",
        subtitle_badge=rx.badge("Текущий план", color_scheme="gray", variant="soft"),
        price_block=rx.text("0$ / мес", size="2", color=rx.color("gray", 10)),
        description="Для старта: публикация объявлений и базовый поиск.",
        features=[
            _feature_item("Базовое размещение", True),
            _feature_item("Фильтры и карта", True),
            _feature_item("Приоритет в выдаче", False),
            _feature_item("Расширенная аналитика", False),
        ],
        cta=_animated_button("Активен", variant="soft", color_scheme="gray", size="2"),
        background=rx.color("gray", 2),
        border_style="1px solid rgba(100, 116, 139, 0.2)",
    )

    pro_card = _plan_card(
        name="PRO",
        subtitle_badge=rx.hstack(
            rx.badge("Most popular", color_scheme="indigo", variant="solid"),
            rx.badge("Рекомендуем", color_scheme="indigo", variant="soft"),
            spacing="2",
            flex_wrap="wrap",
        ),
        price_block=pro_price,
        description="Для активных арендодателей: больше охват и больше контроля.",
        features=[
            _feature_item("Базовое размещение", True),
            _feature_item("Фильтры и карта", True),
            _feature_item("Приоритет в выдаче", True),
            _feature_item("Расширенная аналитика", True),
        ],
        cta=rx.hstack(
            rx.link(
                _animated_button(
                    "Подробнее",
                    size="2",
                    variant="solid",
                    color_scheme="indigo",
                ),
                href="/monetization",
                underline="none",
            ),
            _animated_button(
                "Оформить",
                size="2",
                variant="soft",
                color_scheme="indigo",
                disabled=True,
            ),
            spacing="2",
            flex_wrap="wrap",
        ),
        background=rx.color("indigo", 2),
        border_style="1px solid rgba(79, 70, 229, 0.2)",
    )

    comparison_table = rx.card(
        rx.vstack(
            rx.heading("Сравнение планов", size="4"),
            rx.hstack(
                rx.text("Функция", size="2", color=rx.color("gray", 10)),
                rx.spacer(),
                rx.badge("Free", color_scheme="gray", variant="soft"),
                rx.badge("PRO", color_scheme="indigo", variant="soft"),
                width="100%",
            ),
            _comparison_row("Публикация объявлений", True, True),
            _comparison_row("Карта и фильтры", True, True),
            _comparison_row("Приоритет в выдаче", False, True),
            _comparison_row("Расширенная статистика", False, True),
            spacing="2",
            align_items="start",
            width="100%",
        ),
        variant="surface",
        size="3",
        width="100%",
        style={
            "transition": "transform 180ms ease, box-shadow 180ms ease",
            "box_shadow": "0 2px 12px -6px rgba(0, 0, 0, 0.12)",
        },
        _hover={
            "transform": "translateY(-2px)",
            "box_shadow": "0 14px 24px -16px rgba(0, 0, 0, 0.22)",
        },
    )

    subscription_section = rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading("Подписка", size="5"),
                rx.spacer(),
                rx.badge("Визуальная демо-версия", color_scheme="blue", variant="soft"),
                width="100%",
                align_items="center",
            ),
            rx.text(
                "Платежи пока не подключены. Ниже — как будет выглядеть тарифная логика.",
                size="2",
                color=rx.color("gray", 10),
            ),
            rx.hstack(
                rx.button(
                    "Месяц",
                    size="2",
                    variant=rx.cond(
                        PricingPreviewState.billing_cycle == "month", "solid", "soft"
                    ),
                    color_scheme=rx.cond(
                        PricingPreviewState.billing_cycle == "month", "indigo", "gray"
                    ),
                    on_click=PricingPreviewState.set_billing_cycle("month"),
                    style={"transition": "all 160ms ease"},
                    _hover={"transform": "translateY(-1px)"},
                    _active={"transform": "translateY(0) scale(0.98)"},
                ),
                rx.button(
                    "Год",
                    size="2",
                    variant=rx.cond(
                        PricingPreviewState.billing_cycle == "year", "solid", "soft"
                    ),
                    color_scheme=rx.cond(
                        PricingPreviewState.billing_cycle == "year", "indigo", "gray"
                    ),
                    on_click=PricingPreviewState.set_billing_cycle("year"),
                    style={"transition": "all 160ms ease"},
                    _hover={"transform": "translateY(-1px)"},
                    _active={"transform": "translateY(0) scale(0.98)"},
                ),
                spacing="2",
                align_items="center",
                flex_wrap="wrap",
            ),
            rx.grid(
                free_card,
                pro_card,
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="3",
                width="100%",
            ),
            comparison_table,
            align_items="start",
            spacing="3",
            width="100%",
        ),
        variant="surface",
        size="3",
        width="100%",
        style={
            "transition": "transform 180ms ease, box-shadow 180ms ease",
            "box_shadow": "0 2px 12px -6px rgba(0, 0, 0, 0.12)",
        },
        _hover={
            "transform": "translateY(-2px)",
            "box_shadow": "0 16px 28px -16px rgba(0, 0, 0, 0.22)",
        },
    )

    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.heading("Профиль", size="7"),
                rx.text("Имя в сервисе", size="2", color=rx.color("gray", 10)),
                rx.badge(AuthState.user_name, size="3", color_scheme="blue"),
                rx.text("Вход", size="2", color=rx.color("gray", 10)),
                rx.badge(
                    rx.cond(AuthState.is_logged_in, "Авторизован", "Гость"),
                    color_scheme=rx.cond(AuthState.is_logged_in, "green", "gray"),
                    size="3",
                ),
                rx.cond(
                    AuthState.is_blocked,
                    rx.callout(
                        "Аккаунт заблокирован: чат и новые объявления недоступны.",
                        color_scheme="red",
                    ),
                    rx.fragment(),
                ),
                subscription_section,
                spacing="3",
                padding_y="2rem",
                align_items="start",
                width="100%",
            ),
            size="3",
        ),
        site_footer(),
        width="100%",
        align_items="stretch",
        background=rx.color("gray", 2),
    )
