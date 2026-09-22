from core.models import TextObservation, TextRegion


class TextTracker:

    def __init__(
        self,
        max_gap=0.8,
        max_distance=150,
        min_text_similarity=0.8
    ):
        self.max_gap = max_gap
        self.max_distance = max_distance
        self.min_text_similarity = min_text_similarity
        self.regions = []

    def add(self, observation: TextObservation):

        best_region = None
        best_score = 0

        for region in self.regions:

            gap = observation.time - region.end_time

            if gap > self.max_gap:
                continue

            if not self._is_near(region, observation):
                continue

            similarity = self._text_similarity(
                region.text,
                observation.text
            )

            if similarity < self.min_text_similarity:
                continue

            if similarity > best_score:
                best_score = similarity
                best_region = region

        if best_region is not None:

            best_region.end_time = observation.time

            # Cap nhat vi tri moi nhat
            best_region.x = observation.x
            best_region.y = observation.y
            best_region.width = observation.width
            best_region.height = observation.height

            return

        self.regions.append(
            TextRegion(
                text=observation.text,
                x=observation.x,
                y=observation.y,
                width=observation.width,
                height=observation.height,
                start_time=observation.time,
                end_time=observation.time,
            )
        )

    def _is_near(self, region, observation):

        center_x_region = (
            region.x + region.width / 2
        )

        center_y_region = (
            region.y + region.height / 2
        )

        center_x_obs = (
            observation.x + observation.width / 2
        )

        center_y_obs = (
            observation.y + observation.height / 2
        )

        distance_x = abs(
            center_x_region - center_x_obs
        )

        distance_y = abs(
            center_y_region - center_y_obs
        )

        return (
            distance_x <= self.max_distance
            and
            distance_y <= self.max_distance
        )

    def _text_similarity(self, text1, text2):

        text1 = self._normalize_text(text1)
        text2 = self._normalize_text(text2)

        if not text1 or not text2:
            return 0.0

        if text1 == text2:
            return 1.0

        same = 0

        for a, b in zip(text1, text2):
            if a == b:
                same += 1

        max_length = max(
            len(text1),
            len(text2)
        )

        return same / max_length

    def _normalize_text(self, text):

        punctuation = "，。！？、；：,.!?;:"

        for char in punctuation:
            text = text.replace(char, "")

        return text.strip()

    def get_regions(self):
        return self.regions