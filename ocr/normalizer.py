class TextNormalizer:

    def normalize(self, text):
        text = text.strip()

        if not text:
            return text

        text = self._fix_quotes(text)

        return text

    def _fix_quotes(self, text):

        # Xu ly quote bi lap
        while text.startswith("““"):
            text = text[1:]

        while text.endswith("””"):
            text = text[:-1]

        left_quote = text.count("“")
        right_quote = text.count("”")

        if left_quote > right_quote:
            text += "”"

        elif right_quote > left_quote:
            text = "“" + text

        return text