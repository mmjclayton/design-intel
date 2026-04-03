from src.knowledge.index import query_by_tags, query_by_category
from src.knowledge.store import load_entry
from src.config import settings


def retrieve(
    tags: list[str] | None = None,
    category: str | None = None,
    max_tokens: int | None = None,
) -> str:
    """Retrieve knowledge entries by tags and/or category, up to the token budget.

    Returns concatenated summaries of matching entries.
    """
    limit = max_tokens or settings.knowledge_retrieval_limit
    paths = set()

    if category:
        paths.update(query_by_category(category))
    if tags:
        paths.update(query_by_tags(tags))

    if not paths:
        return ""

    chunks = []
    total_chars = 0
    char_limit = limit * 4  # rough token-to-char estimate

    for path in sorted(paths):
        if not path.exists():
            continue
        entry = load_entry(path)
        title = entry["meta"].get("title", path.stem)
        body = entry["body"]

        chunk = f"### {title}\n{body}\n"
        if total_chars + len(chunk) > char_limit:
            break
        chunks.append(chunk)
        total_chars += len(chunk)

    return "\n".join(chunks)
