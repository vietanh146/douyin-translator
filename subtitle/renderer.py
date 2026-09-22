import os
import glob

from PIL import ImageFont


class DrawTextRenderer:

    def __init__(
        self,
        text_dir="output/drawtext",
        font_path="C:/Windows/Fonts/arial.ttf",
        max_font_size=72
    ):

        self.text_dir = text_dir
        self.font_path = font_path

        self.max_font_size = (
            max_font_size
        )

        # File render trung gian.
        # Khong sua file subtitle goc.
        self.render_text_dir = os.path.join(
            os.path.dirname(
                self.text_dir.rstrip("/\\")
            ),
            "drawtext_render"
        )

    def render(
        self,
        regions,
        filter_output_path
    ):

        if not regions:

            raise ValueError(
                "Khong co subtitle de render"
            )

        # Tao thu muc render trung gian
        os.makedirs(
            self.render_text_dir,
            exist_ok=True
        )

        # Xoa cac file wrap cu
        old_files = glob.glob(
            os.path.join(
                self.render_text_dir,
                "text_*.txt"
            )
        )

        for file_path in old_files:

            try:
                os.remove(file_path)

            except OSError:
                pass

        filters = []

        text_index = 0

        for region in regions:

            # =================================================
            # FIND TEXT FILE
            # =================================================

            text_filename = (
                f"text_{text_index:03d}.txt"
            )

            text_path = os.path.join(
                self.text_dir,
                text_filename
            )

            if not os.path.exists(
                text_path
            ):

                text_index += 1

                continue

            # =================================================
            # REGION
            # =================================================

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

            # =================================================
            # READ ORIGINAL TEXT
            # =================================================

            with open(
                text_path,
                "r",
                encoding="utf-8"
            ) as f:

                text = f.read().strip()

            if not text:

                text_index += 1

                continue

            # =================================================
            # CALCULATE FONT + WRAP
            # =================================================

            wrapped_text, font_size = (
                self._prepare_text(
                    text,
                    w,
                    h
                )
            )

            # =================================================
            # SAVE WRAPPED TEXT
            # =================================================

            render_text_path = os.path.join(
                self.render_text_dir,
                text_filename
            )

            with open(
                render_text_path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(
                    wrapped_text
                )

            # =================================================
            # CENTER
            # =================================================

            center_x = (
                x + w / 2
            )

            center_y = (
                y + h / 2
            )

            # =================================================
            # FFMPEG PATH
            # =================================================

            ffmpeg_text_path = (
                self._ffmpeg_path(
                    render_text_path
                )
            )

            ffmpeg_font_path = (
                self._ffmpeg_path(
                    self.font_path
                )
            )

            # =================================================
            # DRAWTEXT
            # =================================================

            drawtext = (
                "drawtext="
                f"fontfile='{ffmpeg_font_path}':"
                f"textfile='{ffmpeg_text_path}':"
                "expansion=none:"
                f"fontsize={font_size}:"
                "fontcolor=black:"
                "borderw=1:"
                "bordercolor=black:"
                "line_spacing=4:"
                f"x={center_x}-text_w/2:"
                f"y={center_y}-text_h/2:"
                f"enable='between(t,{start:.2f},{end:.2f})'"
            )

            filters.append(
                drawtext
            )

            text_index += 1

        # =====================================================
        # SAVE FILTER
        # =====================================================

        filter_text = ",".join(
            filters
        )

        output_dir = os.path.dirname(
            filter_output_path
        )

        if output_dir:

            os.makedirs(
                output_dir,
                exist_ok=True
            )

        with open(
            filter_output_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                filter_text
            )

        print(
            f"DrawText regions: {len(filters)}"
        )

        print(
            f"Render text directory: "
            f"{self.render_text_dir}"
        )

    # =========================================================
    # PREPARE TEXT
    # =========================================================

    def _prepare_text(
        self,
        text,
        box_width,
        box_height
    ):

        # =========================================================
        # 1. UU TIEN 1 DONG
        # =========================================================

        font_size = self._find_font_size(
            [text],
            box_width,
            box_height
        )

        if self._fits_box(
            [text],
            font_size,
            box_width,
            box_height
        ):

            return (
                text,
                font_size
            )

        # =========================================================
        # 2. THU 2 DONG
        # =========================================================

        lines = self._wrap_text(
            text,
            box_width,
            self.max_font_size,
            max_lines=2
        )

        if len(lines) == 2:

            font_size = self._find_font_size(
                lines,
                box_width,
                box_height
            )

            if self._fits_box(
                lines,
                font_size,
                box_width,
                box_height
            ):

                return (
                    "\n".join(lines),
                    font_size
                )

        # =========================================================
        # 3. THU 3 DONG
        # =========================================================

        lines = self._wrap_text(
            text,
            box_width,
            self.max_font_size,
            max_lines=3
        )

        if len(lines) <= 3:

            font_size = self._find_font_size(
                lines,
                box_width,
                box_height
            )

            if self._fits_box(
                lines,
                font_size,
                box_width,
                box_height
            ):

                return (
                    "\n".join(lines),
                    font_size
                )

        # =========================================================
        # 4. FALLBACK
        # =========================================================
        # Khong duoc tran box.
        # Ep 1 dong va giam font toi khi vua.
    
        font_size = self._find_font_size(
            [text],
            box_width,
            box_height
        )

        return (
            text,
            font_size
        )

    def _find_font_size(
        self,
        lines,
        box_width,
        box_height
    ):

        # Bat dau tu font lon nhat
        font_size = self.max_font_size

        while font_size > 8:

            if self._fits_box(
                lines,
                font_size,
                box_width,
                box_height
            ):

                return font_size

            font_size -= 1

        return 8

    def _fits_box(
        self,
        lines,
        font_size,
        box_width,
        box_height
    ):

        font = self._load_font(
            font_size
        )

        # ---------------------------------------------------------
        # WIDTH
        # ---------------------------------------------------------

        max_width = box_width * 0.90

        for line in lines:

            width = self._measure_text(
                font,
                line
            )

            if width > max_width:

                return False

        # ---------------------------------------------------------
        # HEIGHT
        # ---------------------------------------------------------

        line_count = len(lines)

        line_height = font_size

        line_spacing = 4

        total_height = (
            line_count * line_height
            + (line_count - 1) * line_spacing
        )

        max_height = box_height * 0.90

        if total_height > max_height:

            return False

        return True

    # =========================================================
    # WRAP TEXT
    # =========================================================

    def _wrap_text(
        self,
        text,
        box_width,
        font_size,
        max_lines
    ):

        # Neu nguoi dung da xuong dong thu cong
        # thi giu nguyen cac dong do.
        paragraphs = text.splitlines()

        if len(paragraphs) > 1:

            result = []

            for paragraph in paragraphs:

                paragraph = paragraph.strip()

                if not paragraph:
                    continue

                result.append(
                    paragraph
                )

            return result[:max_lines]

        words = text.split()

        if not words:

            return [text]

        font = self._load_font(
            font_size
        )

        lines = []
        current = ""

        for word in words:

            if not current:

                current = word
                continue

            candidate = (
                current
                + " "
                + word
            )

            width = self._measure_text(
                font,
                candidate
            )

            if width <= box_width * 0.90:

                current = candidate

            else:

                lines.append(
                    current
                )

                current = word

        if current:

            lines.append(
                current
            )

        # -----------------------------------------------------
        # Neu van qua nhieu dong, gop bot
        # -----------------------------------------------------

        if len(lines) <= max_lines:

            return lines

        # Chia lai de co toi da max_lines
        result = []

        chunk_size = (
            len(words) / max_lines
        )

        start = 0

        for i in range(max_lines):

            if i == max_lines - 1:

                chunk_words = words[start:]

            else:

                end = round(
                    (i + 1)
                    * chunk_size
                )

                chunk_words = words[
                    start:end
                ]

            if chunk_words:

                result.append(
                    " ".join(
                        chunk_words
                    )
                )

            start += len(
                chunk_words
            )

        return result

    # =========================================================
    # FONT SIZE
    # =========================================================

    

    # =========================================================
    # CHECK TEXT FIT
    # =========================================================

    

    # =========================================================
    # CHECK MULTIPLE LINES
    # =========================================================

    

    # =========================================================
    # LOAD FONT
    # =========================================================

    def _load_font(
        self,
        font_size
    ):

        try:

            return ImageFont.truetype(
                self.font_path,
                font_size
            )

        except Exception:

            # Fallback neu Pillow khong doc duoc font
            return ImageFont.load_default()

    # =========================================================
    # MEASURE TEXT
    # =========================================================

    def _measure_text(
        self,
        font,
        text
    ):

        try:

            bbox = font.getbbox(
                text
            )

            return bbox[2] - bbox[0]

        except Exception:

            # Fallback rat don gian
            return (
                len(text)
                * font.size
                * 0.50
            )

    # =========================================================
    # FFMPEG PATH
    # =========================================================

    def _ffmpeg_path(
        self,
        path
    ):

        path = path.replace(
            "\\",
            "/"
        )

        if (
            len(path) >= 2
            and path[1] == ":"
        ):

            path = (
                path[0]
                + "\\:"
                + path[2:]
            )

        return path