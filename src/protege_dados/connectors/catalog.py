from __future__ import annotations
import json
from pathlib import Path

def load_catalog(path: Path) -> dict:
    data=json.loads(path.read_text(encoding="utf-8"))
    if "sources" not in data: raise ValueError("Catálogo sem sources")
    return data

def enabled_sources(catalog: dict) -> list[dict]:
    return [s for s in catalog["sources"] if s.get("status") == "integrada"]
