from __future__ import annotations
import json, re, sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
PAGES = sorted(WEB.glob("*.html"))
EXPECTED_UFS = {"AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"}

errors=[]

def fail(msg): errors.append(msg)

# Strict JSON
try:
    data=json.loads((WEB/"data/ivpd_uf_v1.json").read_text(encoding="utf-8"))
except Exception as exc:
    data=[]
    fail(f"JSON principal inválido: {exc}")

if len(data)!=27: fail(f"Total de UFs diferente de 27: {len(data)}")
ufs={str(row.get("uf","")).upper() for row in data if isinstance(row,dict)}
if ufs!=EXPECTED_UFS: fail(f"Conjunto de UFs incorreto. Ausentes={sorted(EXPECTED_UFS-ufs)} extras={sorted(ufs-EXPECTED_UFS)}")

# Text and links
bad_markers=("Ã","Â","â€","ï»¿")
for page in PAGES:
    text=page.read_text(encoding="utf-8")
    for marker in bad_markers:
        if marker in text: fail(f"Texto corrompido em {page.name}: {marker}")
    if '<meta charset="utf-8">' not in text.lower(): fail(f"Meta charset ausente: {page.name}")
    if 'lang="pt-BR"' not in text: fail(f"Idioma ausente: {page.name}")
    for target in re.findall(r'(?:href|src)="([^"]+)"', text):
        if target.startswith(("http://","https://","mailto:","#","javascript:")): continue
        clean=target.split("?",1)[0].split("#",1)[0]
        if not clean: continue
        path=(page.parent/clean).resolve()
        try:
            path.relative_to(WEB.resolve())
        except ValueError:
            fail(f"Link sai da pasta web em {page.name}: {target}")
            continue
        if not path.exists(): fail(f"Link/recurso ausente em {page.name}: {target}")

# Required controls
panel=(WEB/"painel.html").read_text(encoding="utf-8")
for id_ in ["uf","vuln","taxa","internet","banda","bars","download","download-standard","compare-1","compare-2","compare-3","compare-button","comparison","download-comparison","uf-table-body"]:
    if f'id="{id_}"' not in panel: fail(f"Controle ausente no painel: {id_}")

# API strict JSON
for path in (WEB/"api/v1").glob("*.json"):
    try: json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc: fail(f"API inválida {path.name}: {exc}")

if errors:
    print("VALIDAÇÃO REPROVADA")
    for err in errors: print("-",err)
    sys.exit(1)
print(f"VALIDAÇÃO APROVADA: {len(PAGES)} páginas, 27 UFs e links locais íntegros.")
