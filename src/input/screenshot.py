import asyncio
from pathlib import Path

from playwright.async_api import async_playwright


async def _capture(url: str, output_path: str, viewport_width: int = 1440) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": viewport_width, "height": 900})
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await page.screenshot(path=output_path, full_page=True)
        text = await page.inner_text("body")
        await browser.close()
    return text


def capture_url(url: str, output_path: str = "output/screenshot.png") -> tuple[str, str]:
    """Capture a screenshot of a URL. Returns (screenshot_path, extracted_text)."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    text = asyncio.run(_capture(url, output_path))
    return output_path, text
