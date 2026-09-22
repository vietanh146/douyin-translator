from core.models import TextRegion


class TextRegionMerger:

    def __init__(
        self,
        max_gap=0.6,
        max_distance=300
    ):
        self.max_gap = max_gap
        self.max_distance = max_distance

    def merge(self, regions):

        merged = []

        regions = sorted(
            regions,
            key=lambda r: r.start_time
        )

        for region in regions:

            best_region = None

            for existing in reversed(merged):

                gap = (
                    region.start_time
                    - existing.end_time
                )

                if gap > self.max_gap:
                    break

                if not self._same_text(
                    existing.text,
                    region.text
                ):
                    continue

                if not self._is_near(
                    existing,
                    region
                ):
                    continue

                best_region = existing
                break

            if best_region is not None:

                best_region.end_time = max(
                    best_region.end_time,
                    region.end_time
                )

                # Cap nhat vi tri moi nhat
                best_region.x = region.x
                best_region.y = region.y
                best_region.width = region.width
                best_region.height = region.height

            else:

                merged.append(
                    TextRegion(
                        text=region.text,
                        x=region.x,
                        y=region.y,
                        width=region.width,
                        height=region.height,
                        start_time=region.start_time,
                        end_time=region.end_time
                    )
                )

        return merged

    def _same_text(self, text1, text2):

        text1 = self._normalize(text1)
        text2 = self._normalize(text2)

        return text1 == text2

    def _normalize(self, text):

        punctuation = (
            "，。！？、；：,.!?;:"
            "“”\"'"
        )

        for char in punctuation:
            text = text.replace(char, "")

        return text.strip()

    def _is_near(self, region1, region2):

        center_x_1 = (
            region1.x +
            region1.width / 2
        )

        center_y_1 = (
            region1.y +
            region1.height / 2
        )

        center_x_2 = (
            region2.x +
            region2.width / 2
        )

        center_y_2 = (
            region2.y +
            region2.height / 2
        )

        distance_x = abs(
            center_x_1 -
            center_x_2
        )

        distance_y = abs(
            center_y_1 -
            center_y_2
        )

        return (
            distance_x <= self.max_distance
            and
            distance_y <= self.max_distance
        )