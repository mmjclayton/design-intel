from pathlib import Path

from src.input.models import DesignInput, InputType
from src.input.screenshot import capture_url


def process_image(image_path: str) -> DesignInput:
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    return DesignInput(type=InputType.SCREENSHOT, image_path=str(path.resolve()))


def process_url(url: str) -> DesignInput:
    screenshot_path, page_text = capture_url(url)
    return DesignInput(
        type=InputType.URL,
        image_path=screenshot_path,
        page_text=page_text,
        url=url,
    )


def process_text(description: str) -> DesignInput:
    return DesignInput(type=InputType.TEXT, page_text=description)


def process_input(
    image: str | None = None,
    url: str | None = None,
    describe: str | None = None,
) -> DesignInput:
    if image:
        return process_image(image)
    if url:
        return process_url(url)
    if describe:
        return process_text(describe)
    raise ValueError("Provide one of: --image, --url, or --describe")
