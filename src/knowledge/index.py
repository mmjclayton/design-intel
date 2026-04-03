from pathlib import Path

import yaml

from src.knowledge.store import KNOWLEDGE_DIR, load_entry, list_entries


INDEX_PATH = KNOWLEDGE_DIR / "INDEX.yaml"


def build_index() -> dict:
    """Build the tag-based index from all knowledge entries."""
    index = {"categories": {}, "tags": {}}

    for entry_path in list_entries():
        entry = load_entry(entry_path)
        meta = entry["meta"]
        rel_path = str(entry_path.relative_to(KNOWLEDGE_DIR))

        category = meta.get("category", "uncategorized")
        index["categories"].setdefault(category, []).append(rel_path)

        for tag in meta.get("tags", []):
            index["tags"].setdefault(tag, []).append(rel_path)

    INDEX_PATH.write_text(yaml.dump(index, default_flow_style=False, sort_keys=False))
    return index


def load_index() -> dict:
    """Load the tag-based index."""
    if not INDEX_PATH.exists():
        return build_index()
    return yaml.safe_load(INDEX_PATH.read_text()) or {}


def query_by_tags(tags: list[str]) -> list[Path]:
    """Find knowledge entries matching any of the given tags."""
    index = load_index()
    tag_index = index.get("tags", {})
    paths = set()
    for tag in tags:
        for rel_path in tag_index.get(tag, []):
            paths.add(KNOWLEDGE_DIR / rel_path)
    return sorted(paths)


def query_by_category(category: str) -> list[Path]:
    """Find knowledge entries in a given category."""
    index = load_index()
    cat_index = index.get("categories", {})
    return [KNOWLEDGE_DIR / p for p in cat_index.get(category, [])]
