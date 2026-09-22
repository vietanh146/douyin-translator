import os
import cv2
import numpy as np
from paddleocr import PaddleOCR


PROJECT_DIR = "."
IMAGE_PATH = os.path.join(PROJECT_DIR, "test", "test.png")

OUTPUT_DIR = os.path.join(
    PROJECT_DIR,
    "output/text_segmentation"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# 1. PaddleOCR
# ============================================================

print("Loading PaddleOCR...")

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    enable_mkldnn=False,
)

print("Running OCR...")

results = ocr.predict(IMAGE_PATH)


# ============================================================
# 2. Load image
# ============================================================

image = cv2.imread(IMAGE_PATH)

if image is None:
    raise RuntimeError(
        f"Khong mo duoc anh: {IMAGE_PATH}"
    )


# ============================================================
# 3. Text segmentation
# ============================================================

def segment_text(crop):
    """
    Tao mask text bang phan tich pixel.

    Tra ve:
        mask: binary mask
    """

    # --------------------------------------------------------
    # A. Lam mo nhe de giam noise
    # --------------------------------------------------------

    blurred = cv2.GaussianBlur(
        crop,
        (5, 5),
        0
    )

    gray = cv2.cvtColor(
        blurred,
        cv2.COLOR_BGR2GRAY
    )

    # --------------------------------------------------------
    # B. Top-hat
    #
    # Tim cac vung sang hon background xung quanh.
    # Huu ich cho chu trang / vang.
    # --------------------------------------------------------

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (31, 31)
    )

    top_hat = cv2.morphologyEx(
        gray,
        cv2.MORPH_TOPHAT,
        kernel
    )

    # --------------------------------------------------------
    # C. Black-hat
    #
    # Tim cac vung toi hon background.
    # Huu ich cho vien chu / chu toi.
    # --------------------------------------------------------

    black_hat = cv2.morphologyEx(
        gray,
        cv2.MORPH_BLACKHAT,
        kernel
    )

    # --------------------------------------------------------
    # D. Adaptive threshold
    # --------------------------------------------------------

    bright_mask = cv2.adaptiveThreshold(
        top_hat,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        3
    )

    dark_mask = cv2.adaptiveThreshold(
        black_hat,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        3
    )

    # --------------------------------------------------------
    # E. Gop hai loai
    # --------------------------------------------------------

    mask = cv2.bitwise_or(
        bright_mask,
        dark_mask
    )

    # --------------------------------------------------------
    # F. Morphology
    # --------------------------------------------------------

    small_kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (3, 3)
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        small_kernel
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        small_kernel
    )

    # --------------------------------------------------------
    # G. Lo cac blob qua nho
    # --------------------------------------------------------

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        mask,
        connectivity=8
    )

    cleaned = np.zeros_like(mask)

    min_area = max(
        10,
        int(mask.shape[0] * mask.shape[1] * 0.0001)
    )

    for label in range(1, num_labels):

        area = stats[label, cv2.CC_STAT_AREA]

        if area >= min_area:
            cleaned[labels == label] = 255

    return cleaned


# ============================================================
# 4. Process OCR boxes
# ============================================================

for result in results:

    data = result.json["res"]

    texts = data["rec_texts"]
    scores = data["rec_scores"]
    boxes = data["rec_boxes"]

    for index, (text, score, box) in enumerate(
        zip(texts, scores, boxes)
    ):

        if score < 0.8:
            continue

        x1, y1, x2, y2 = map(
            int,
            box
        )

        # ----------------------------------------------------
        # Padding nhe
        # ----------------------------------------------------

        padding = 10

        x1_crop = max(
            0,
            x1 - padding
        )

        y1_crop = max(
            0,
            y1 - padding
        )

        x2_crop = min(
            image.shape[1],
            x2 + padding
        )

        y2_crop = min(
            image.shape[0],
            y2 + padding
        )

        crop = image[
            y1_crop:y2_crop,
            x1_crop:x2_crop
        ]

        if crop.size == 0:
            continue

        print()
        print("=" * 60)
        print(f"Text : {text}")
        print(f"Score: {score:.4f}")
        print(
            f"Box  : "
            f"{x1}, {y1}, {x2}, {y2}"
        )

        # ----------------------------------------------------
        # Segment
        # ----------------------------------------------------

        mask = segment_text(crop)

        # ----------------------------------------------------
        # Save mask
        # ----------------------------------------------------

        safe_name = (
            f"{index:02d}_"
            + "".join(
                c if c.isalnum() else "_"
                for c in text
            )
        )

        mask_path = os.path.join(
            OUTPUT_DIR,
            f"{safe_name}_mask.png"
        )

        cv2.imwrite(
            mask_path,
            mask
        )

        # ----------------------------------------------------
        # Save crop
        # ----------------------------------------------------

        crop_path = os.path.join(
            OUTPUT_DIR,
            f"{safe_name}_crop.png"
        )

        cv2.imwrite(
            crop_path,
            crop
        )

        # ----------------------------------------------------
        # Create overlay
        # ----------------------------------------------------

        overlay = crop.copy()

        red_layer = np.zeros_like(crop)
        red_layer[:, :, 2] = 255

        mask_bool = mask > 0

        overlay[mask_bool] = cv2.addWeighted(
            crop[mask_bool],
            0.35,
            red_layer[mask_bool],
            0.65,
            0
        )

        overlay_path = os.path.join(
            OUTPUT_DIR,
            f"{safe_name}_overlay.png"
        )

        cv2.imwrite(
            overlay_path,
            overlay
        )

        print(f"Mask   : {mask_path}")
        print(f"Crop   : {crop_path}")
        print(f"Overlay: {overlay_path}")


print()
print("=" * 60)
print("DONE")
print("=" * 60)
print(
    f"Output: {OUTPUT_DIR}"
)