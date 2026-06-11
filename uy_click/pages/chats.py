import reflex as rx

from uy_click.components.footer import site_footer
from uy_click.components.navbar import navbar
from uy_click.i18n import t
from uy_click.state.chat_state import ChatState


def chat_item(chat) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.text(
                    rx.cond(
                        chat.peer_user_id,
                        rx.hstack(t("chats_chat_with"), " ", chat.peer_label, spacing="0"),
                        rx.hstack(t("chats_chat_id"), chat.id.to_string(), spacing="0"),
                    ),
                    weight="medium",
                ),
                rx.text(chat.created_at_label, size="1", color=rx.color("gray", 10)),
                align_items="start",
                spacing="1",
            ),
            rx.spacer(),
            rx.button(t("chats_open"), on_click=ChatState.select_chat(chat.id), variant="soft"),
            width="100%",
            align="center",
        ),
        width="100%",
    )


def message_item(message) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.text(message.sender_label, size="1", color=rx.color("gray", 10)),
                rx.spacer(),
                rx.text(message.created_at_label, size="1", color=rx.color("gray", 10)),
                width="100%",
            ),
            rx.text(message.body),
            align_items="start",
            spacing="1",
        ),
        width="100%",
    )


def quick_contact_item(contact) -> rx.Component:
    return rx.button(
        contact.label,
        on_click=ChatState.create_chat_with_user(contact.user_id),
        variant="soft",
        width="100%",
    )


def chats() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.hstack(
                    rx.heading(t("chats_title"), size="7"),
                    rx.spacer(),
                    rx.button(
                        t("chats_refresh"),
                        on_click=[ChatState.load_chats, ChatState.load_messages, ChatState.load_quick_contacts],
                        variant="soft",
                    ),
                    width="100%",
                ),
                rx.text(t("chats_hint"), size="2", color=rx.color("gray", 10), width="100%"),
                rx.hstack(
                    rx.text(t("chats_contacts_label"), weight="medium", size="2"),
                    rx.spacer(),
                    rx.button(t("chats_refresh_contacts"), on_click=ChatState.load_quick_contacts, variant="soft"),
                    width="100%",
                ),
                rx.vstack(
                    rx.heading(t("chats_quick_contacts"), size="4"),
                    rx.cond(
                        ChatState.quick_contacts,
                        rx.foreach(ChatState.quick_contacts, quick_contact_item),
                        rx.text(t("chats_quick_empty"), color=rx.color("gray", 10), size="2"),
                    ),
                    width="100%",
                    align_items="stretch",
                    spacing="2",
                ),
                rx.cond(
                    ChatState.error_message,
                    rx.callout(ChatState.error_message, color_scheme="red"),
                    rx.fragment(),
                ),
                rx.cond(
                    ChatState.success_message,
                    rx.callout(ChatState.success_message, color_scheme="green"),
                    rx.fragment(),
                ),
                rx.grid(
                    rx.vstack(
                        rx.heading(t("chats_dialogs"), size="5"),
                        rx.foreach(ChatState.chats, chat_item),
                        spacing="2",
                        width="100%",
                        align_items="stretch",
                    ),
                    rx.vstack(
                        rx.heading(t("chats_messages"), size="5"),
                        rx.foreach(ChatState.messages, message_item),
                        rx.hstack(
                            rx.input(
                                placeholder=t("chats_input_ph"),
                                value=ChatState.new_message,
                                on_change=ChatState.set_new_message,
                                width="100%",
                            ),
                            rx.button(t("chats_send"), on_click=ChatState.send_message, color_scheme="teal"),
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                        align_items="stretch",
                    ),
                    columns=rx.breakpoints(initial="1", md="2"),
                    spacing="6",
                    width="100%",
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
