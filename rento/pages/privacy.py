import reflex as rx

from rento.components.footer import site_footer
from rento.components.navbar import navbar


def privacy() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.box(
            rx.container(
                rx.vstack(
                    rx.heading("Персональные данные", size="7"),
                    rx.text(
                        "Как мы обрабатываем данные в RENTO. Детали зависят от вашей настройки Supabase "
                        "и юрисдикции; при запуске на реальных пользователей согласуйте текст с юристом.",
                        size="2",
                        color=rx.color("gray", 10),
                    ),
                    rx.heading("1. Какие данные", size="5", margin_top="1rem"),
                    rx.text(
                        "Для работы сервиса обрабатываются, в частности: учётные данные аккаунта "
                        "(через Supabase Auth), профиль, объявления, сообщения в чате, избранное, "
                        "технические логи хостинга. Загрузка фото объявлений хранится в Supabase Storage.",
                        size="2",
                        color=rx.color("gray", 11),
                    ),
                    rx.heading("2. Цели обработки", size="5", margin_top="1rem"),
                    rx.text(
                        "Данные используются для предоставления функций сайта (публикация объявлений, "
                        "чат, модерация администраторами), обеспечения безопасности и выполнения требований закона.",
                        size="2",
                        color=rx.color("gray", 11),
                    ),
                    rx.heading("3. Передача третьим лицам", size="5", margin_top="1rem"),
                    rx.text(
                        "Инфраструктура (Supabase, хостинг приложения) получает данные в объёме, "
                        "необходимом для работы сервиса. Мы не продаём персональные данные рекламным сетям.",
                        size="2",
                        color=rx.color("gray", 11),
                    ),
                    rx.heading("4. Ваши действия", size="5", margin_top="1rem"),
                    rx.text(
                        "Вы можете запросить удаление аккаунта и данных у администрации сервиса "
                        "в разумных пределах и с учётом хранения, требуемого законом. Настройки сессии и "
                        "выход из аккаунта доступны в интерфейсе.",
                        size="2",
                        color=rx.color("gray", 11),
                    ),
                    rx.heading("5. Контакты", size="5", margin_top="1rem"),
                    rx.text(
                        "Вопросы по персональным данным направляйте через контакты, которые вы "
                        "укажете для проекта (почта поддержки), когда они появятся.",
                        size="2",
                        color=rx.color("gray", 11),
                    ),
                    spacing="3",
                    align_items="start",
                    padding_y="2rem",
                    width="100%",
                ),
                size="3",
            ),
            width="100%",
            flex_grow="1",
        ),
        site_footer(),
        width="100%",
        min_height="100vh",
        align_items="stretch",
    )
