from translator.cache import TranslationCache


def main():

    cache = TranslationCache(
        "output/test_cache.json"
    )

    print("Lan 1:")

    cache.set(
        "小鸟胃",
        "Sức ăn như mèo"
    )

    print(
        cache.get("小鸟胃")
    )

    print()
    print("Lan 2:")

    cache2 = TranslationCache(
        "output/test_cache.json"
    )

    print(
        cache2.get("小鸟胃")
    )


if __name__ == "__main__":
    main()