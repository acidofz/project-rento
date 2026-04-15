import reflex as rx

from rento.utils.helpers import current_year


def site_footer() -> rx.Component:
    return rx.box(
        rx.container(
            rx.vstack(
                rx.separator(),
                rx.hstack(
                    rx.hstack(
                        rx.link(
                            "Правила площадки",
                            href="/terms",
                            size="2",
                            color=rx.color("gray", 11),
                        ),
                        rx.link(
                            "Персональные данные",
                            href="/privacy",
                            size="2",
                            color=rx.color("gray", 11),
                        ),
                        spacing="4",
                    ),
                    rx.spacer(),
                    rx.text(
                        f"© {current_year()} RENTO",
                        size="1",
                        color=rx.color("gray", 9),
                    ),
                    width="100%",
                    align_items="center",
                    padding_y="1rem",
                ),
                spacing="0",
                width="100%",
            ),
            size="4",
        ),
        width="100%",
        bg=rx.color("gray", 2),
        border_top=f"1px solid {rx.color('gray', 4)}",
    )
