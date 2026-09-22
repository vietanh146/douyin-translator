from translator.gemini_translator import GeminiTranslator


def main():
    translator = GeminiTranslator()

    text = "你姥爷就是靠这手艺才娶到我的"

    result = translator.translate(text)

    print("Chinese:")
    print(text)

    print("\nVietnamese:")
    print(result)


if __name__ == "__main__":
    main()