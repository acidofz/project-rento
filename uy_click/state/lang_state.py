import reflex as rx


class LangState(rx.State):
    lang: str = rx.LocalStorage("uz", name="uy_click_lang")

    def set_lang(self, lang: str) -> None:
        self.lang = lang
