import json
import os
import glob


class SubtitleTextManager:

    def __init__(
        self,
        input_json,
        output_dir
    ):

        self.input_json = input_json
        self.output_dir = output_dir

    def generate(self):

        # =====================================================
        # LOAD TRANSLATION
        # =====================================================

        with open(
            self.input_json,
            "r",
            encoding="utf-8"
        ) as f:

            regions = json.load(f)

        if not regions:

            raise ValueError(
                "Khong co subtitle."
            )

        # =====================================================
        # CREATE DIRECTORY
        # =====================================================

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )

        # =====================================================
        # REMOVE OLD TEXT FILES
        # =====================================================

        old_files = glob.glob(
            os.path.join(
                self.output_dir,
                "text_*.txt"
            )
        )

        for file_path in old_files:

            os.remove(
                file_path
            )

        # =====================================================
        # CREATE TEXT FILES
        # =====================================================

        count = 0

        for region in regions:

            translation = (
                region.get(
                    "translation",
                    ""
                )
                .strip()
            )

            if not translation:

                continue

            filename = (
                f"text_{count:03d}.txt"
            )

            filepath = os.path.join(
                self.output_dir,
                filename
            )

            with open(
                filepath,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(
                    translation
                )

            count += 1

        print(
            f"Created {count} subtitle text files."
        )