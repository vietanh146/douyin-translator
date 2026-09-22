from translator.translator import Translator


class MockTranslator(Translator):

    def translate(self, text: str) -> str:
        return f"[VI] {text}"