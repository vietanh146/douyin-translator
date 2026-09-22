import json
import os

from subtitle.renderer import DrawTextRenderer


INPUT_PATH = "test/data/translated_sample.json"

DRAWBOX_OUTPUT_PATH = (
    "test/data/drawbox_filter.txt"
)

DRAWTEXT_OUTPUT_PATH = (
    "test/data/drawtext_filter.txt"
)


def load_regions(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def build_drawbox_filter(
    regions
):

    filters = []

    for region in regions:

        x = int(region["x"])
        y = int(region["y"])

        w = int(region["width"])
        h = int(region["height"])

        start = float(
            region["start_time"]
        )

        end = float(
            region["end_time"]
        )

        drawbox = (
            f"drawbox="
            f"x={x}:"
            f"y={y}:"
            f"w={w}:"
            f"h={h}:"
            f"color=white:"
            f"t=fill:"
            f"enable='between(t,{start:.2f},{end:.2f})'"
        )

        filters.append(
            drawbox
        )

    return ",".join(
        filters
    )


def save_filter(
    filter_text,
    path
):

    output_dir = os.path.dirname(
        path
    )

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True
        )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            filter_text
        )


def main():

    regions = load_regions(
        INPUT_PATH
    )

    print(
        f"Loaded: {len(regions)} regions"
    )

    if not regions:

        print(
            "Khong co subtitle de render."
        )

        return

    # =========================================================
    # DRAWBOX
    # =========================================================

    drawbox_filter = (
        build_drawbox_filter(
            regions
        )
    )

    save_filter(
        drawbox_filter,
        DRAWBOX_OUTPUT_PATH
    )

    # =========================================================
    # DRAWTEXT
    # =========================================================

    renderer = DrawTextRenderer(
        text_dir="test/data/drawtext",
        font_path="C:/Windows/Fonts/arial.ttf",
        max_font_size=72
    )

    renderer.render(
        regions,
        DRAWTEXT_OUTPUT_PATH
    )

    # =========================================================
    # INFO
    # =========================================================

    print()
    print("=" * 60)
    print("SUBTITLE RENDER")
    print("=" * 60)

    print(
        f"Regions       : {len(regions)}"
    )

    print(
        f"Drawbox       : {DRAWBOX_OUTPUT_PATH}"
    )

    print(
        f"Drawtext      : {DRAWTEXT_OUTPUT_PATH}"
    )

    print()
    print(
        "Render filter da tao thanh cong."
    )


if __name__ == "__main__":
    main()