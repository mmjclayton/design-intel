from pathlib import Path

import yaml


KNOWLEDGE_DIR = Path(__file__).parent.parent.parent / "knowledge"


def load_entry(file_path: Path) -> dict:
    """Load a knowledge entry, parsing YAML frontmatter and markdown body."""
    text = file_path.read_text()
    if not text.startswith("---"):
        return {"body": text, "meta": {}}

    _, frontmatter, body = text.split("---", 2)
    meta = yaml.safe_load(frontmatter)
    return {"meta": meta or {}, "body": body.strip()}


def list_entries(category: str | None = None) -> list[Path]:
    """List all knowledge entries, optionally filtered by category."""
    if category:
        category_dir = KNOWLEDGE_DIR / category
        if not category_dir.exists():
            return []
        return sorted(category_dir.glob("*.md"))

    entries = []
    for child in sorted(KNOWLEDGE_DIR.iterdir()):
        if child.is_dir() and child.name not in ("pending",):
            entries.extend(sorted(child.glob("*.md")))
    return entries


def get_categories() -> list[str]:
    """List available knowledge categories."""
    return [
        d.name
        for d in sorted(KNOWLEDGE_DIR.iterdir())
        if d.is_dir() and d.name not in ("pending",)
    ]
