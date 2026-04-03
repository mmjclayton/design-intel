import base64
from pathlib import Path

import litellm

from src.config import settings


# Map shorthand provider names to LiteLLM model prefixes
PROVIDER_PREFIX = {
    "claude": "anthropic/",
    "openai": "",
    "ollama": "ollama/",
}


def _resolve_model() -> str:
    prefix = PROVIDER_PREFIX.get(settings.llm_provider, "")
    model = settings.llm_model
    if model.startswith(prefix):
        return model
    return f"{prefix}{model}"


def _encode_image(image_path: str) -> dict:
    path = Path(image_path)
    suffix = path.suffix.lower().lstrip(".")
    media_type = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(
        suffix, "image/png"
    )
    data = base64.b64encode(path.read_bytes()).decode("utf-8")
    return {
        "type": "image_url",
        "image_url": {"url": f"data:{media_type};base64,{data}"},
    }


def call_llm(
    system_prompt: str,
    user_prompt: str,
    image_path: str | None = None,
    max_tokens: int | None = None,
    temperature: float | None = None,
) -> str:
    model = _resolve_model()
    messages = [{"role": "system", "content": system_prompt}]

    user_content: list[dict] | str
    if image_path:
        user_content = [
            {"type": "text", "text": user_prompt},
            _encode_image(image_path),
        ]
    else:
        user_content = user_prompt

    messages.append({"role": "user", "content": user_content})

    response = litellm.completion(
        model=model,
        messages=messages,
        max_tokens=max_tokens or settings.llm_max_tokens,
        temperature=temperature if temperature is not None else settings.llm_temperature,
    )

    return response.choices[0].message.content
