import argparse
import json

from dotenv import load_dotenv

from translator.gemini_translator import GeminiTranslator


load_dotenv()


INPUT_PATH = "test/data/ocr_sample.json"
OUTPUT_PATH = "test/data/translated_gemini.json"


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

    print(f"Loaded: {len(regions)} regions")

    if not regions:
        print("Khong co region nao de dich.")
        return

    texts = [
        region["text"]
        for region in regions
    ]

    if args.live:
        print("MODE: GEMINI LIVE")
        translator = GeminiTranslator()
        output_path = OUTPUT_PATH
    else:
        print("MODE: FAKE / LOCAL")
        translator = FakeTranslator()
        output_path = "test/data/translated_fake.json"

    translations = translator.translate_batch_with_cache(
        texts
    )

    if len(translations) != len(regions):
        raise RuntimeError(
            f"So luong khong khop: "
            f"{len(regions)} regions "
            f"nhung co {len(translations)} translations"
        )

    for region, translation in zip(
        regions,
        translations
    ):
        if translation is None:
            raise RuntimeError(
                f"Thieu translation cho: {region['text']}"
            )

        region["translation"] = translation

    save_regions(
        regions,
        output_path
    )

    print()
    print("=" * 60)
    print("TRANSLATION RESULT")
    print("=" * 60)

    for region in regions:
        print()
        print(f"CN : {region['text']}")
        print(f"VI : {region['translation']}")
        print(
            f"Time: "
            f"{region['start_time']:.2f}s"
            f" -> "
            f"{region['end_time']:.2f}s"
        )

    print()
    print("=" * 60)
    print(f"Saved: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()