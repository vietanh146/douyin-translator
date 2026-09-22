from translator.mock_translator import MockTranslator


def main():
    translator = MockTranslator()

    test_texts = [
        "小鸟胃",
        "我吃饱啦",
        "女友",
    ]

    for text in test_texts:
        result = translator.translate(text)

        expected = f"[VI] {text}"

        if result != expected:
            raise AssertionError(
                f"Translation sai: "
                f"{result} != {expected}"
            )

    print(f"PASS: {len(test_texts)} translations")


if __name__ == "__main__":
    main()