from core.models import TextRegion
from ocr.filter import TextFilter


regions = [
    TextRegion(
        text="你好",
        x=200,
        y=100,
        width=300,
        height=100,
        start_time=1.0,
        end_time=2.0,
    ),

    TextRegion(
        text="我",
        x=300,
        y=500,
        width=80,
        height=80,
        start_time=2.0,
        end_time=3.0,
    ),

    TextRegion(
        text="7",
        x=600,
        y=500,
        width=30,
        height=25,
        start_time=3.0,
        end_time=3.0,
    ),
]


text_filter = TextFilter()

filtered = text_filter.filter(regions)

print("=" * 50)
print(f"Before: {len(regions)}")
print(f"After : {len(filtered)}")
print("=" * 50)

for region in filtered:
    print(
        f"{region.text} | "
        f"{region.width}x{region.height}"
    )