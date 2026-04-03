from dataclasses import dataclass, field
from enum import Enum


class InputType(Enum):
    SCREENSHOT = "screenshot"
    URL = "url"
    TEXT = "text"
    FIGMA = "figma"


@dataclass
class DesignInput:
    type: InputType
    image_path: str | None = None
    page_text: str | None = None
    url: str | None = None
    metadata: dict = field(default_factory=dict)
