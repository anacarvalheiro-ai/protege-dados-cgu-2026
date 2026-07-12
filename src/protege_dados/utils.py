from __future__ import annotations
from pathlib import Path
import hashlib
import json
import pandas as pd

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def normalize_ibge_code(series: pd.Series) -> pd.Series:
    s = series.astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
    return s.str.zfill(7)

def normalize_uf(series: pd.Series) -> pd.Series:
    return series.astype("string").str.upper().str.strip()

def safe_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")

def ensure_dirs(*paths: Path) -> None:
    for p in paths:
        p.mkdir(parents=True, exist_ok=True)

def write_json(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
