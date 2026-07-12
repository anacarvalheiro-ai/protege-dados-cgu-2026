from __future__ import annotations
from pathlib import Path
import pandas as pd
from .utils import normalize_ibge_code, normalize_uf, safe_numeric
from .schema import resolve_semantic_map
from .quality import quality_report

def _require(mapping: dict, fields: list[str], source: str):
    missing = [f for f in fields if not mapping.get(f)]
    if missing:
        raise ValueError(f"{source}: campos sem correspondência: {missing}")

def process_ibge(df: pd.DataFrame, cfg: dict):
    m = resolve_semantic_map(df.columns, cfg["required_semantic_fields"])
    _require(m, ["municipality_code", "uf", "population"], "IBGE")
    out = pd.DataFrame({
        "codigo_municipio_ibge_7": normalize_ibge_code(df[m["municipality_code"]]),
        "uf": normalize_uf(df[m["uf"]]),
        "population": safe_numeric(df[m["population"]]),
    })
    out = out.dropna(subset=["codigo_municipio_ibge_7", "uf", "population"])
    out = out[out["population"] > 0]
    return out, quality_report(out, ["codigo_municipio_ibge_7"])

def process_inep(df: pd.DataFrame, cfg: dict):
    m = resolve_semantic_map(df.columns, cfg["required_semantic_fields"])
    _require(m, ["municipality_code", "uf", "internet", "broadband"], "INEP")
    out = pd.DataFrame({
        "codigo_municipio_ibge_7": normalize_ibge_code(df[m["municipality_code"]]),
        "uf": normalize_uf(df[m["uf"]]),
        "internet": safe_numeric(df[m["internet"]]),
        "broadband": safe_numeric(df[m["broadband"]]),
    })
    if m.get("active_school"):
        active = safe_numeric(df[m["active_school"]])
        out = out[active == 1]
    out["internet"] = out["internet"].fillna(0).clip(0, 1)
    out["broadband"] = out["broadband"].fillna(0).clip(0, 1)
    return out, quality_report(out)

def process_anatel(df: pd.DataFrame, cfg: dict, reference_year: int):
    m = resolve_semantic_map(df.columns, cfg["required_semantic_fields"])
    _require(m, ["municipality_code", "uf", "accesses"], "ANATEL")
    out = pd.DataFrame({
        "codigo_municipio_ibge_7": normalize_ibge_code(df[m["municipality_code"]]),
        "uf": normalize_uf(df[m["uf"]]),
        "accesses": safe_numeric(df[m["accesses"]]),
    })
    if m.get("year"):
        out["year"] = safe_numeric(df[m["year"]])
        out = out[out["year"] == reference_year]
    if m.get("month"):
        out["month"] = safe_numeric(df[m["month"]])
        out = out[out["month"] == 12]
    out["accesses"] = out["accesses"].fillna(0)
    return out, quality_report(out)

def process_ondh(df: pd.DataFrame, cfg: dict, reference_year: int):
    m = resolve_semantic_map(df.columns, cfg["required_semantic_fields"])
    _require(m, ["uf"], "ONDH")
    out = pd.DataFrame({"uf": normalize_uf(df[m["uf"]])})
    if m.get("count"):
        out["violations"] = safe_numeric(df[m["count"]]).fillna(0)
    else:
        out["violations"] = 1
    if m.get("year"):
        y = safe_numeric(df[m["year"]])
        out = out[y == reference_year]
    return out, quality_report(out)
