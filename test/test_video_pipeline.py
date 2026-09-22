from ocr.timing import TimingRefiner
from ocr.video_ocr import VideoOCR
from ocr.filter import TextFilter
from ocr.normalizer import TextNormalizer
from ocr.merger import TextRegionMerger
from core.serializer import save_regions
from core.video import get_video_info


video_path = "input/video.mp4"
video_info = get_video_info(video_path)
video_duration = video_info["duration"]


# OCR + Tracking
processor = VideoOCR(
    interval=0.5,
    score_threshold=0.8
)

regions = processor.process(video_path)

timing_refiner = TimingRefiner(
    padding=0.25,
    video_duration=video_duration
)

regions = timing_refiner.refine(regions)

# Merge cac region cung text
merger = TextRegionMerger()

print()
print(
    f"Truoc merge: {len(regions)} regions"
)

regions = merger.merge(regions)

print(
    f"Sau merge: {len(regions)} regions"
)


# Filter
text_filter = TextFilter()
regions = text_filter.filter(regions)


# Normalize
normalizer = TextNormalizer()

for region in regions:
    region.text = normalizer.normalize(region.text)

# Save OCR result
save_regions(
    regions,
    "test/data/ocr_result_sample.json"
)


print()
print("=" * 60)
print("TEXT REGIONS")
print("=" * 60)

for region in regions:
    print()
    print(f"Text  : {region.text}")
    print(f"Start : {region.start_time:.1f}s")
    print(f"End   : {region.end_time:.1f}s")
    print(
        f"Box   : "
        f"({region.x}, {region.y}) "
        f"{region.width}x{region.height}"
    )