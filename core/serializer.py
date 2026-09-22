import json
from dataclasses import asdict


def save_regions(regions, output_path):
    data = [
        asdict(region)
        for region in regions
    ]

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )