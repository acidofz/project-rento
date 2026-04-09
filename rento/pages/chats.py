import reflex as rx

from rento.components.navbar import navbar
from rento.state.chat_state import ChatState


def chat_item(chat) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.text(
                    rx.cond(chat.peer_user_id, f"Чат с {chat.peer_label}", f"Чат #{chat.id}"),
                    weight="medium",
                ),
                rx.text(chat.created_at_label, size="1", color=rx.color("gray", 10)),
                align_items="start",
                spacing="1",
            ),
            rx.spacer(),
            rx.button("Открыть чат", on_click=ChatState.select_chat(chat.id), variant="soft"),
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
                    rx.heading("Чаты", size="7"),
                    rx.spacer(),
                    rx.button(
                        "Обновить",
                        on_click=[ChatState.load_chats, ChatState.load_messages, ChatState.load_quick_contacts],
                        variant="soft",
                    ),
                    width="100%",
                ),
                rx.text(
                    "Новый диалог — кнопка «Написать» в объявлении или контакт ниже.",
                    size="2",
                    color=rx.color("gray", 10),
                    width="100%",
                ),
                rx.hstack(
                    rx.text("Контакты", weight="medium", size="2"),
                    rx.spacer(),
                    rx.button("Обновить список", on_click=ChatState.load_quick_contacts, variant="soft"),
                    width="100%",
                ),
                rx.vstack(
                    rx.heading("Быстрые контакты", size="4"),
                    rx.cond(
                        ChatState.quick_contacts,
                        rx.foreach(ChatState.quick_contacts, quick_contact_item),
                        rx.text(
                            "Пока пусто. Откройте объявления и напишите владельцу — контакт появится здесь.",
                            color=rx.color("gray", 10),
                            size="2",
                        ),
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
                        rx.heading("Ваши диалоги", size="5"),
                        rx.foreach(ChatState.chats, chat_item),
                        spacing="2",
                        width="100%",
                        align_items="stretch",
                    ),
                    rx.vstack(
                        rx.heading("Переписка", size="5"),
                        rx.foreach(ChatState.messages, message_item),
                        rx.hstack(
                            rx.input(
                                placeholder="Сообщение…",
                                value=ChatState.new_message,
                                on_change=ChatState.set_new_message,
                                width="100%",
                            ),
                            rx.button("Отправить", on_click=ChatState.send_message),
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                        align_items="stretch",
                    ),
                    columns="2",
                    spacing="6",
                    width="100%",
                ),
                spacing="4",
                width="100%",
                padding_y="2rem",
            ),
            size="4",
        ),
        width="100%",
        min_height="100vh",
        align_items="stretch",
    )
