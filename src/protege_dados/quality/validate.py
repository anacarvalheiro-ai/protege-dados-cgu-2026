from __future__ import annotations
import json
from pathlib import Path

REQUIRED=["web/config/portal.json","web/config/menu.json","web/config/indicadores.json","web/config/fontes.json","web/data/ivpd_uf_v1.json"]

def main() -> None:
    root=Path(__file__).resolve().parents[3]
    for rel in REQUIRED:
        p=root/rel
        if not p.exists(): raise FileNotFoundError(rel)
        if p.suffix==".json": json.loads(p.read_text(encoding="utf-8"))
    rows=json.loads((root/"web/data/ivpd_uf_v1.json").read_text(encoding="utf-8"))
    ufs={str(r.get("uf","")).upper() for r in rows}
    if len(ufs)!=27: raise ValueError(f"Cobertura territorial inesperada: {len(ufs)} UFs")
    print("Validação 4.0 concluída.")
if __name__=="__main__": main()
