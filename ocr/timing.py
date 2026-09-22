class TimingRefiner:

    def __init__(
        self,
        padding=0.25,
        video_duration=None
    ):
        self.padding = padding
        self.video_duration = video_duration

    def refine(self, regions):

        for region in regions:

            region.start_time = max(
                0,
                region.start_time - self.padding
            )

            region.end_time = (
                region.end_time +
                self.padding
            )

            if self.video_duration is not None:
                region.end_time = min(
                    region.end_time,
                    self.video_duration
                )

        return regions