import cv2
from paddleocr import PaddleOCR


VIDEO_PATH = "input/video.mp4"


ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    enable_mkldnn=False,
)


cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    raise RuntimeError(f"Khong the mo video: {VIDEO_PATH}")


fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count / fps

print(f"Video: {duration:.2f} giay")
print(f"FPS: {fps:.2f}")
print()
print("Bat dau OCR moi 1 giay...")
print()


current_second = 0

while current_second < duration:

    # Di chuyen den frame tai giay hien tai
    frame_number = int(current_second * fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    success, frame = cap.read()

    if not success:
        break

    # OCR frame
    results = ocr.predict(frame)

    print("=" * 60)
    print(f"TIME: {current_second:.2f}s")

    found_text = False

    for res in results:
        data = res.json

        texts = data["res"]["rec_texts"]
        scores = data["res"]["rec_scores"]
        boxes = data["res"]["rec_boxes"]

        for text, score, box in zip(texts, scores, boxes):

            found_text = True

            x1, y1, x2, y2 = map(int, box)

            print(f"Text  : {text}")
            print(f"Score : {score:.4f}")
            print(f"Box   : ({x1}, {y1}) -> ({x2}, {y2})")

    if not found_text:
        print("Khong phat hien text")

    current_second += 1


cap.release()

print()
print("OCR video test hoan tat!")