"""Бенто-сетка: плитки с единым визуальным языком (карточки, скругления, акценты)."""

import reflex as rx


def bento_tile(
    *,
    title: str,
    subtitle: str,
    icon_tag: str,
    accent: str = "indigo",
    min_height: str | None = "148px",
    child: rx.Component | None = None,
) -> rx.Component:
    """Одна плитка бенто-сетки."""
    body = (
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon(tag=icon_tag, size=22, color=rx.color(accent, 11)),
                    padding="0.45rem",
                    border_radius="10px",
                    background=rx.color(accent, 3),
                ),
                rx.spacer(),
                width="100%",
            ),
            rx.heading(title, size="5", weight="bold"),
            rx.text(subtitle, size="2", color=rx.color("gray", 11), line_height="1.45"),
            rx.spacer(),
            child if child is not None else rx.fragment(),
            align_items="start",
            spacing="2",
            width="100%",
            min_height="0",
            flex="1",
        ),
    )
    return rx.card(
        body,
        variant="surface",
        size="3",
        width="100%",
        min_height=min_height,
        style={"box_shadow": "0 2px 12px -4px rgba(0, 0, 0, 0.08)"},
    )


def bento_hero(
    *,
    title: str,
    subtitle: str,
    child: rx.Component | None = None,
) -> rx.Component:
    """Крупная герой-плитка на всю ширину сетки."""
    inner = rx.vstack(
        rx.badge("RENTO", color_scheme="indigo", variant="soft", size="2"),
        rx.heading(title, size="8", weight="bold", style={"letter_spacing": "-0.02em"}),
        rx.text(
            subtitle,
            size="4",
            color=rx.color("gray", 11),
            line_height="1.5",
            max_width="36rem",
        ),
        child if child is not None else rx.fragment(),
        align_items="start",
        spacing="4",
        width="100%",
    )
    return rx.box(
        rx.card(
            inner,
            variant="surface",
            size="4",
            width="100%",
            background=rx.color("indigo", 2),
            style={
                "border": "1px solid rgba(79, 70, 229, 0.12)",
                "box_shadow": "0 12px 40px -18px rgba(79, 70, 229, 0.25)",
            },
        ),
        width="100%",
    )
