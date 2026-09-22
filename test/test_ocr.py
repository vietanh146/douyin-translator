from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    enable_mkldnn=False,
)

result = ocr.predict("test/test.png")

for res in result:
    data = res.json

    texts = data["res"]["rec_texts"]
    scores = data["res"]["rec_scores"]
    boxes = data["res"]["rec_boxes"]

    for text, score, box in zip(texts, scores, boxes):
        x1, y1, x2, y2 = box

        width = x2 - x1
        height = y2 - y1

        print("=" * 40)
        print(f"Text   : {text}")
        print(f"Score  : {score:.4f}")
        print(f"X      : {x1}")
        print(f"Y      : {y1}")
        print(f"Width  : {width}")
        print(f"Height : {height}")