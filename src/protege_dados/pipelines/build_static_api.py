from __future__ import annotations
import json, hashlib
from pathlib import Path

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def main() -> None:
    root=Path(__file__).resolve().parents[3]
    source=root/"web/data/ivpd_uf_v1.json"
    api=root/"web/api/v1"
    api.mkdir(parents=True,exist_ok=True)
    rows=json.loads(source.read_text(encoding="utf-8"))
    (api/"territories.json").write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding="utf-8")
    manifest={"version":"4.0.0","artifacts":{"territories.json":sha256(api/"territories.json")}}
    (api/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
if __name__=="__main__": main()
