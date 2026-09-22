from dataclasses import dataclass


@dataclass
class TextObservation:
    text: str
    x: int
    y: int
    width: int
    height: int
    score: float
    time: float


@dataclass
class TextRegion:
    text: str
    x: int
    y: int
    width: int
    height: int
    start_time: float
    end_time: float