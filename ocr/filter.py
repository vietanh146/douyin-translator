import re


class TextFilter:

    def __init__(
        self,
        min_width=50,
        min_height=40,
    ):
        self.min_width = min_width
        self.min_height = min_height

    def filter(self, regions):
        filtered = []

        for region in regions:
            text = region.text.strip()

            if not text:
                print(
                    f"[FILTER] Bo rong: {region.text}"
                )
                continue

            if self._is_only_punctuation(text):
                print(
                    f"[FILTER] Chi la ky tu: "
                    f"{region.text}"
                )
                continue

            if region.width < self.min_width:
                print(
                    f"[FILTER] Qua nho: "
                    f"{region.text} "
                    f"{region.width}x{region.height}"
                )
                continue

            if region.height < self.min_height:
                print(
                    f"[FILTER] Qua thap: "
                    f"{region.text} "
                    f"{region.width}x{region.height}"
                )
                continue

            if self._is_small_number(region):
                print(
                    f"[FILTER] So nho: "
                    f"{region.text}"
                )
                continue

            filtered.append(region)

        return filtered

    def _is_only_punctuation(self, text):
        punctuation = r"""，。！？、；：,.!?;:"“”'‘’"""

        return all(
            char in punctuation
            for char in text
        )

    def _is_small_number(self, region):
        text = region.text.strip()

        if not re.fullmatch(r"\d+", text):
            return False

        return (
            len(text) <= 2
            and region.width < 100
            and region.height < 100
        )