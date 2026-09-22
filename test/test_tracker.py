from core.models import TextObservation
from ocr.tracker import TextTracker


tracker = TextTracker(
    max_gap=1.5,
    max_distance=100,
    min_text_similarity=0.8
)

# Cùng một câu nhưng OCR hơi khác nhau
tracker.add(
    TextObservation(
        text="姥姥",
        x=300,
        y=500,
        width=200,
        height=80,
        score=0.99,
        time=1.0
    )
)

tracker.add(
    TextObservation(
        text="姥姥!",
        x=305,
        y=503,
        width=200,
        height=80,
        score=0.99,
        time=2.0
    )
)

tracker.add(
    TextObservation(
        text="姥姥",
        x=302,
        y=501,
        width=200,
        height=80,
        score=0.99,
        time=3.0
    )
)


regions = tracker.get_regions()

print("=" * 50)
print(f"So region: {len(regions)}")

for region in regions:
    print("=" * 50)
    print(f"Text : {region.text}")
    print(f"Start: {region.start_time}s")
    print(f"End  : {region.end_time}s")