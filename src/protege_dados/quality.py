from __future__ import annotations
import pandas as pd

def quality_report(df: pd.DataFrame, key_columns: list[str] | None = None) -> dict:
    report = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_by_column": {c: int(df[c].isna().sum()) for c in df.columns},
    }
    if key_columns:
        valid = [c for c in key_columns if c in df.columns]
        if valid:
            report["duplicate_keys"] = int(df.duplicated(valid).sum())
    return report

def coverage_by_uf(df: pd.DataFrame, uf_col: str) -> pd.DataFrame:
    out = df.groupby(uf_col, dropna=False).size().rename("rows").reset_index()
    return out.sort_values(uf_col)
