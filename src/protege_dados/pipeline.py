from __future__ import annotations
from pathlib import Path
import json, yaml, pandas as pd
from .readers import read_tabular, read_zip_first_csv
from .processors import process_ibge, process_inep, process_anatel, process_ondh
from .indicators import build_uf_indicators
from .utils import sha256_file, ensure_dirs, write_json

def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def first_file(folder: Path, allowed):
    files = [p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in allowed]
    if not files:
        raise FileNotFoundError(f"Nenhum arquivo encontrado em {folder}")
    return sorted(files)[0]

def read_source(path: Path):
    return read_zip_first_csv(path) if path.suffix.lower()==".zip" else read_tabular(path)

def run(root: Path) -> dict:
    cfg = load_yaml(root/"config/sources.yml")
    ivpd = load_yaml(root/"config/ivpd.yml")
    ensure_dirs(root/"logs", root/"data/interim", root/"data/processed", root/"data/published")

    manifest=[]
    frames={}
    quality={}
    for key, scfg in cfg["sources"].items():
        path = first_file(root/scfg["raw_dir"], set(scfg["accepted_extensions"]))
        manifest.append({"source":key,"file":str(path.relative_to(root)),"bytes":path.stat().st_size,"sha256":sha256_file(path)})
        df=read_source(path)
        if key=="ibge": frames[key], quality[key]=process_ibge(df, scfg)
        elif key=="inep": frames[key], quality[key]=process_inep(df, scfg)
        elif key=="anatel": frames[key], quality[key]=process_anatel(df, scfg, cfg["reference_year"])
        elif key=="ondh": frames[key], quality[key]=process_ondh(df, scfg, cfg["reference_year"])
        frames[key].to_parquet(root/f"data/interim/{key}.parquet", index=False)

    write_json(manifest, root/"logs/raw_manifest.json")
    write_json(quality, root/"logs/quality_report.json")

    result=build_uf_indicators(frames["ibge"],frames["inep"],frames["anatel"],frames["ondh"],ivpd["weights"])
    result.to_csv(root/"data/processed/ivpd_uf_2024.csv", index=False)
    result.to_json(root/"data/published/ivpd_uf_2024.json", orient="records", force_ascii=False, indent=2)

    summary={
        "reference_year":cfg["reference_year"],
        "sources":len(manifest),
        "ufs":int(result["uf"].nunique()),
        "rows":int(len(result)),
        "protection_axis_published":False
    }
    write_json(summary, root/"reports/execution_summary.json")
    return summary
