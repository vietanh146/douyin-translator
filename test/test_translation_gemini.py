import argparse
import json

from translator.gemini_translator import GeminiTranslator


INPUT_PATH = "test/data/ocr_sample.json"
OUTPUT_PATH = "test/data/translated_gemini_single.json"


class FakeTranslator:

    def translate(self, text):
        return f"[VI] {text}"


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

    if args.live:
        print("MODE: GEMINI LIVE")
        translator = GeminiTranslator()
        output_path = OUTPUT_PATH
    else:
        print("MODE: FAKE / LOCAL")
        translator = FakeTranslator()
        output_path = "test/data/translated_fake_single.json"

    for i, region in enumerate(regions, start=1):

        print(
            f"[{i}/{len(regions)}] "
            f"{region['text']}"
        )

        translation = translator.translate(
            region["text"]
        )

        if translation is None:
            raise RuntimeError(
                f"Thieu translation cho: "
                f"{region['text']}"
            )

        region["translation"] = translation

        print(f"  -> {translation}")

    save_regions(
        regions,
        output_path
    )

    print()
    print("Da dich xong!")
    print(f"Ket qua: {output_path}")


if __name__ == "__main__":
    main()