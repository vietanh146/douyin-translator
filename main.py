import argparse
import json
import os
import subprocess

from dotenv import load_dotenv

from core.video import get_video_info

from ocr.video_ocr import VideoOCR
from ocr.merger import TextRegionMerger
from ocr.filter import TextFilter
from ocr.normalizer import TextNormalizer
from ocr.timing import TimingRefiner

from translator.gemini_translator import GeminiTranslator

from subtitle.renderer import DrawTextRenderer
from subtitle.text_manager import SubtitleTextManager

import config


# ============================================================
# UTILS
# ============================================================

def save_json(data, path):

    directory = os.path.dirname(path)

    if directory:
        os.makedirs(
            directory,
            exist_ok=True
        )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ============================================================
# OCR
# ============================================================

def run_ocr(
    input_video,
    ocr_output
):

    print()
    print("=" * 60)
    print("STEP 1: OCR")
    print("=" * 60)

    video_info = get_video_info(
        input_video
    )

    print(
        f"Video: "
        f"{video_info['width']}x"
        f"{video_info['height']}"
    )

    print(
        f"FPS: "
        f"{video_info['fps']}"
    )

    print(
        f"Duration: "
        f"{video_info['duration']:.2f}s"
    )

    # --------------------------------------------------------
    # OCR
    # --------------------------------------------------------

    ocr = VideoOCR(
        interval=config.OCR_INTERVAL,
        score_threshold=config.OCR_SCORE_THRESHOLD
    )

    regions = ocr.process(
        input_video
    )

    print(
        f"\nOCR regions: {len(regions)}"
    )

    # --------------------------------------------------------
    # MERGE
    # --------------------------------------------------------

    merger = TextRegionMerger()

    regions = merger.merge(
        regions
    )

    print(
        f"After merge: {len(regions)}"
    )

    # --------------------------------------------------------
    # FILTER
    # --------------------------------------------------------

    text_filter = TextFilter()

    regions = text_filter.filter(
        regions
    )

    print(
        f"After filter: {len(regions)}"
    )

    # --------------------------------------------------------
    # NORMALIZE
    # --------------------------------------------------------

    normalizer = TextNormalizer()

    for region in regions:

        region.text = normalizer.normalize(
            region.text
        )

    # --------------------------------------------------------
    # TIMING
    # --------------------------------------------------------

    timing = TimingRefiner(
        padding=config.TIMING_PADDING,
        video_duration=video_info["duration"]
    )

    regions = timing.refine(
        regions
    )

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    data = []

    for region in regions:

        data.append({
            "text": region.text,
            "x": region.x,
            "y": region.y,
            "width": region.width,
            "height": region.height,
            "start_time": region.start_time,
            "end_time": region.end_time
        })

    save_json(
        data,
        ocr_output
    )

    print(
        f"Saved: {ocr_output}"
    )

    return data


# ============================================================
# TRANSLATION
# ============================================================

def run_translation(
    regions,
    translation_output
):

    print()
    print("=" * 60)
    print("STEP 2: GEMINI TRANSLATION")
    print("=" * 60)

    texts = [
        region["text"]
        for region in regions
    ]

    translator = GeminiTranslator()

    translations = (
        translator.translate_batch_with_cache(
            texts
        )
    )

    for region, translation in zip(
        regions,
        translations
    ):

        region["translation"] = translation

    save_json(
        regions,
        translation_output
    )

    print(
        f"Translated: {len(regions)} regions"
    )

    print(
        f"Saved: {translation_output}"
    )

    return regions





# ============================================================
# DRAWBOX
# ============================================================

def build_drawbox_filter(
    regions
):

    filters = []

    for region in regions:

        x = int(
            region["x"]
        )

        y = int(
            region["y"]
        )

        w = int(
            region["width"]
        )

        h = int(
            region["height"]
        )

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

    directory = os.path.dirname(
        path
    )

    if directory:

        os.makedirs(
            directory,
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


# ============================================================
# BUILD SUBTITLE FILTERS
# ============================================================

def build_subtitle_filters(
    regions,
    text_dir,
    drawbox_output,
    drawtext_output
):

    print()
    print("=" * 60)
    print("STEP 4: BUILD SUBTITLE FILTERS")
    print("=" * 60)

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
        drawbox_output
    )

    # =========================================================
    # DRAWTEXT
    # =========================================================

    renderer = DrawTextRenderer(
        text_dir=text_dir,
        font_path="C:/Windows/Fonts/arial.ttf",
        max_font_size=config.SUBTITLE_MAX_SIZE
    )

    renderer.render(
        regions,
        drawtext_output
    )

    print(
        "Subtitle filters created."
    )

# ============================================================
# VIDEO RENDER
# ============================================================

def render_video(
    input_video,
    drawbox_output,
    drawtext_output,
    output_video
):

    print()
    print("=" * 60)
    print("STEP 5: VIDEO RENDER")
    print("=" * 60)

    if not os.path.exists(config.FFMPEG_PATH):
        raise FileNotFoundError(
            f"Khong tim thay FFmpeg: {config.FFMPEG_PATH}"
        )

    drawbox = load_filter_text(drawbox_output)
    drawtext = load_filter_text(drawtext_output)

    video_filter = f"{drawbox},{drawtext}"

    command = [
        config.FFMPEG_PATH,
        "-y",
        "-i", input_video,
        "-vf", video_filter,
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "medium",
        "-c:a", "copy",
        output_video
    ]

    print("Running FFmpeg...")

    subprocess.run(command, check=True)

    print()
    print("Video created:")
    print(output_video)


def load_filter_text(
    path
):

    if not os.path.exists(
        path
    ):

        raise FileNotFoundError(
            f"Khong tim thay filter: "
            f"{path}"
        )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read().strip()


# ============================================================
# FULL PIPELINE
# ============================================================

def translate_new_video(
    input_video
):

    # =========================================================
    # PROJECT NAME
    # =========================================================

    base_name = os.path.splitext(
        os.path.basename(input_video)
    )[0]

    project_dir = os.path.join(
        config.OUTPUT_DIR,
        base_name
    )

    os.makedirs(
        project_dir,
        exist_ok=True
    )

    # =========================================================
    # PROJECT PATHS
    # =========================================================

    ocr_output = os.path.join(
        project_dir,
        "ocr.json"
    )

    translation_output = os.path.join(
        project_dir,
        "translated.json"
    )

    text_dir = os.path.join(
        project_dir,
        "drawtext"
    )

    drawbox_output = os.path.join(
        project_dir,
        "drawbox_filter.txt"
    )

    drawtext_output = os.path.join(
        project_dir,
        "drawtext_filter.txt"
    )

    video_output = os.path.join(
        project_dir,
        f"{base_name}_translated.mp4"
    )

    # =========================================================
    # STEP 1: OCR
    # =========================================================

    regions = run_ocr(
        input_video,
        ocr_output
    )

    if not regions:

        print(
            "Khong tim thay text."
        )

        return

    # =========================================================
    # STEP 2: GEMINI
    # =========================================================

    regions = run_translation(
        regions,
        translation_output
    )

    # =========================================================
    # STEP 3: TEXT FILES
    # =========================================================

    print()
    print("=" * 60)
    print("STEP 3: PREPARE SUBTITLES")
    print("=" * 60)

    manager = SubtitleTextManager(
        input_json=translation_output,
        output_dir=text_dir
    )

    manager.generate()

    # =========================================================
    # STEP 4: FILTERS
    # =========================================================

    build_subtitle_filters(
        regions,
        text_dir,
        drawbox_output,
        drawtext_output
    )

    # =========================================================
    # STEP 5: VIDEO
    # =========================================================

    render_video(
        input_video,
        drawbox_output,
        drawtext_output,
        video_output
    )

    print()
    print("=" * 60)
    print("TRANSLATION COMPLETE")
    print("=" * 60)

    print()
    print(
        f"Project: {project_dir}"
    )

    print(
        f"Video: {video_output}"
    )

    print()
    print(
        "Subtitle:"
    )

    print(
        text_dir
    )

# ============================================================
# RENDER EXISTING
# ============================================================

def render_existing(
    input_video
):

    base_name = os.path.splitext(
        os.path.basename(input_video)
    )[0]

    project_dir = os.path.join(
        config.OUTPUT_DIR,
        base_name
    )

    translation_output = os.path.join(
        project_dir,
        "translated.json"
    )

    text_dir = os.path.join(
        project_dir,
        "drawtext"
    )

    drawbox_output = os.path.join(
        project_dir,
        "drawbox_filter.txt"
    )

    drawtext_output = os.path.join(
        project_dir,
        "drawtext_filter.txt"
    )

    output_video = os.path.join(
        project_dir,
        f"{base_name}_translated_final.mp4"
    )

    # =========================================================
    # CHECK PROJECT
    # =========================================================

    if not os.path.exists(
        project_dir
    ):

        raise FileNotFoundError(
            f"Khong tim thay project: "
            f"{project_dir}"
        )

    if not os.path.exists(
        translation_output
    ):

        raise FileNotFoundError(
            f"Khong tim thay: "
            f"{translation_output}"
        )

    # =========================================================
    # LOAD TRANSLATION
    # =========================================================

    regions = load_json(
        translation_output
    )

    print()
    print(
        f"Project: {project_dir}"
    )

    print(
        f"Loaded: {len(regions)} regions"
    )

    # =========================================================
    # BUILD FILTERS
    # =========================================================

    build_subtitle_filters(
        regions,
        text_dir,
        drawbox_output,
        drawtext_output
    )

    # =========================================================
    # RENDER VIDEO
    # =========================================================

    render_video(
        input_video,
        drawbox_output,
        drawtext_output,
        output_video
    )

    print()
    print("=" * 60)
    print("RENDER COMPLETE")
    print("=" * 60)

    print()
    print(
        f"Video: {output_video}"
    )


# ============================================================
# CLI
# ============================================================

def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Douyin Translator"
    )

    parser.add_argument(
        "input",
        nargs="?",
        help="Duong dan toi video"
    )

    parser.add_argument(
        "--render",
        action="store_true",
        help="Render lai subtitle hien tai"
    )

    return parser.parse_args()


# ============================================================
# MAIN
# ============================================================

def main():

    load_dotenv()

    args = parse_arguments()

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    input_video = args.input

    if not input_video:

        input_video = (
            input(
                "\nNhap duong dan video: "
            )
            .strip()
            .strip('"')
        )

    if not os.path.exists(
        input_video
    ):

        raise FileNotFoundError(
            f"Khong tim thay video: "
            f"{input_video}"
        )

    print()
    print("=" * 60)
    print("DOUYIN TRANSLATOR")
    print("=" * 60)

    print()
    print(
        f"Input: {input_video}"
    )

    try:

        # ----------------------------------------------------
        # RENDER MODE
        # ----------------------------------------------------

        if args.render:

            render_existing(
                input_video
            )

        # ----------------------------------------------------
        # FULL MODE
        # ----------------------------------------------------

        else:

            translate_new_video(
                input_video
            )

    except Exception as e:

        print()
        print("=" * 60)
        print("ERROR")
        print("=" * 60)

        print()
        print(
            str(e)
        )

        raise


if __name__ == "__main__":
    main()