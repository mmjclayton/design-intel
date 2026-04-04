import base64
from pathlib import Path

import litellm

from src.config import settings


# Map shorthand provider names to LiteLLM model prefixes
PROVIDER_PREFIX = {
    "claude": "anthropic/",
    "openai": "",
    "ollama": "ollama/",
    "google": "gemini/",
    "mistral": "mistral/",
    "groq": "groq/",
    "deepseek": "deepseek/",
    "together": "together_ai/",
    "openrouter": "openrouter/",
}


def _resolve_model(model_override: str | None = None) -> str:
    if model_override:
        # If it already has a prefix (contains /), use as-is
        if "/" in model_override:
            return model_override
        # Otherwise apply the default provider prefix
        prefix = PROVIDER_PREFIX.get(settings.llm_provider, "")
        return f"{prefix}{model_override}"

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
    image_paths: list[str] | None = None,
    max_tokens: int | None = None,
    temperature: float | None = None,
    model: str | None = None,
) -> str:
    """Call an LLM. Optional model override for ensemble mode."""
    resolved_model = _resolve_model(model)
    messages = [{"role": "system", "content": system_prompt}]

    # Collect all images
    all_images = []
    if image_path:
        all_images.append(image_path)
    if image_paths:
        all_images.extend(image_paths)

    # Check if model supports vision (some don't)
    model_lower = resolved_model.lower()
    supports_vision = not any(
        nv in model_lower for nv in [
            "llama-3.3", "mistral-small", "mistral-large",
            "deepseek-chat", "llama-3.1",
        ]
    )

    user_content: list[dict] | str
    if all_images and supports_vision:
        user_content = [{"type": "text", "text": user_prompt}]
        for img in all_images:
            if Path(img).exists():
                user_content.append(_encode_image(img))
    else:
        user_content = user_prompt

    messages.append({"role": "user", "content": user_content})

    response = litellm.completion(
        model=resolved_model,
        messages=messages,
        max_tokens=max_tokens or settings.llm_max_tokens,
        temperature=temperature if temperature is not None else settings.llm_temperature,
    )

    return response.choices[0].message.content


def get_model_display_name(model: str) -> str:
    """Get a short display name for a model."""
    # Strip provider prefix for display
    parts = model.split("/")
    if len(parts) >= 2:
        provider = parts[0]
        name = "/".join(parts[1:])
        return f"{name} ({provider})"
    return model
