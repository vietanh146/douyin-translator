from ocr.normalizer import TextNormalizer


normalizer = TextNormalizer()


tests = [
    "“我吃饱啦”",
    "“炒面",
    "薯条”",
    "“这火不够大啊",
    "“焦点才好吃”",
    "普通文字",
]


for text in tests:
    result = normalizer.normalize(text)

    print(
        f"{text:<20} -> {result}"
    )