from __future__ import annotations
from typing import Iterable

def resolve_column(columns: Iterable[str], aliases: list[str]) -> str | None:
    lookup = {str(c).strip().lower(): c for c in columns}
    for alias in aliases:
        if alias.lower() in lookup:
            return lookup[alias.lower()]
    return None

def resolve_semantic_map(columns, required_semantic_fields: dict[str, list[str]]) -> dict[str, str | None]:
    return {
        semantic: resolve_column(columns, aliases)
        for semantic, aliases in required_semantic_fields.items()
    }
