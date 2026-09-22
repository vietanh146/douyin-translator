from paddleocr import PaddleOCR
from PIL import Image, ImageDraw

INPUT_IMAGE = "test/test.png"
OUTPUT_IMAGE = "test/output.png"

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    enable_mkldnn=False,
)

result = ocr.predict(INPUT_IMAGE)

image = Image.open(INPUT_IMAGE).convert("RGB")
draw = ImageDraw.Draw(image)

for res in result:
    data = res.json

    texts = data["res"]["rec_texts"]
    scores = data["res"]["rec_scores"]
    boxes = data["res"]["rec_boxes"]

    for text, score, box in zip(texts, scores, boxes):
        x1, y1, x2, y2 = map(int, box)

        # Ve bounding box
        draw.rectangle(
            [x1, y1, x2, y2],
            outline="red",
            width=3
        )

        # Ve text + confidence
        label = f"{text} ({score:.2f})"

        draw.text(
            (x1, max(0, y1 - 20)),
            label,
            fill="red"
        )

image.save(OUTPUT_IMAGE)

print(f"Da luu anh: {OUTPUT_IMAGE}")