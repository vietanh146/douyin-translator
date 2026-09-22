import cv2

from paddleocr import PaddleOCR

from core.models import TextObservation
from ocr.tracker import TextTracker


class VideoOCR:

    def __init__(self, interval=0.5, score_threshold=0.8):
        self.interval = interval
        self.score_threshold = score_threshold

        self.ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            enable_mkldnn=False,
        )

    def process(self, video_path):

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise RuntimeError(
                f"Khong the mo video: {video_path}"
            )

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(
            cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        duration = frame_count / fps

        tracker = TextTracker()

        current_time = 0.0

        while current_time < duration:

            frame_number = int(current_time * fps)

            cap.set(
                cv2.CAP_PROP_POS_FRAMES,
                frame_number
            )

            success, frame = cap.read()

            if not success:
                break

            results = self.ocr.predict(frame)

            for res in results:

                data = res.json

                texts = data["res"]["rec_texts"]
                scores = data["res"]["rec_scores"]
                boxes = data["res"]["rec_boxes"]

                for text, score, box in zip(
                    texts,
                    scores,
                    boxes
                ):

                    if score < self.score_threshold:
                        continue

                    x1, y1, x2, y2 = map(
                        int,
                        box
                    )

                    observation = TextObservation(
                        text=text,
                        x=x1,
                        y=y1,
                        width=x2 - x1,
                        height=y2 - y1,
                        score=float(score),
                        time=current_time,
                    )

                    tracker.add(observation)

            print(
                f"OCR: {current_time:.1f}s / "
                f"{duration:.1f}s"
            )

            current_time += self.interval

        cap.release()

        return tracker.get_regions()