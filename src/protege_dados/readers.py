from __future__ import annotations
from pathlib import Path
import pandas as pd
import zipfile
import tempfile

def read_tabular(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        for enc in ("utf-8", "latin-1"):
            try:
                return pd.read_csv(path, sep=None, engine="python", encoding=enc, low_memory=False)
            except Exception:
                continue
        raise ValueError(f"Não foi possível ler CSV: {path}")
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    raise ValueError(f"Formato não suportado: {path.suffix}")

def read_zip_first_csv(path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as zf:
        members = [m for m in zf.namelist() if m.lower().endswith(".csv")]
        if not members:
            raise ValueError("ZIP sem CSV.")
        with zf.open(members[0]) as f:
            return pd.read_csv(f, sep=None, engine="python", encoding="latin-1", low_memory=False)
