import argparse
import json

from translator.gemini_translator import GeminiTranslator


INPUT_PATH = "test/data/ocr_sample.json"
OUTPUT_PATH = "test/data/translated_gemini_batch.json"


def load_regions(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_regions(regions, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            regions,
            f,
            ensure_ascii=False,
            indent=2
        )


class FakeTranslator:

    def translate_batch_with_cache(self, texts):
        return [
            f"[VI] {text}"
            for text in texts
        ]


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--live",
        action="store_true",
        help="Goi Gemini API that"
    )
    args = parser.parse_args()

    regions = load_regions(INPUT_PATH)

    if not regions:
        print("Khong co region nao de dich.")
        return

    texts = [
        region["text"]
        for region in regions
    ]

    print(f"Bat dau dich {len(texts)} regions...")
    print()

    if args.live:
        print("MODE: GEMINI LIVE")
        translator = GeminiTranslator()
        output_path = OUTPUT_PATH
    else:
        print("MODE: FAKE / LOCAL")
        translator = FakeTranslator()
        output_path = "test/data/translated_fake_batch.json"

    translations = translator.translate_batch_with_cache(
        texts
    )

    print()
    print("Ket qua dich:")
    print()

    if len(translations) != len(regions):
        raise RuntimeError(
            f"So luong khong khop: "
            f"{len(regions)} regions "
            f"nhung co {len(translations)} translations"
        )

    for i, region in enumerate(regions):

        translation = translations[i]

        if translation is None:
            raise RuntimeError(
                f"Thieu translation cho id {i}: "
                f"{region['text']}"
            )

        print(f"[{i}] {region['text']}")
        print(f"    -> {translation}")

        region["translation"] = translation

    save_regions(
        regions,
        output_path
    )

    print()
    print("Da dich xong!")
    print(f"Ket qua: {output_path}")


if __name__ == "__main__":
    main()