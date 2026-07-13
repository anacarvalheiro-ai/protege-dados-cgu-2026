from pathlib import Path
import csv, json, sys

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"}
errors=[]

def check(condition, message):
    if not condition:
        errors.append(message)

csv_path = ROOT/"data/processed/ivpd_uf_v1.csv"
json_path = ROOT/"web/data/ivpd_uf_v1.json"
panel_path = ROOT/"web/painel.html"
js_path = ROOT/"web/assets/app.js"
css_path = ROOT/"web/assets/style.css"

for path, label in [(csv_path,"CSV derivado"),(json_path,"JSON do portal"),(panel_path,"painel.html"),(js_path,"app.js"),(css_path,"style.css")]:
    check(path.exists(), f"{label} ausente")

rows=[]
if csv_path.exists():
    with csv_path.open(encoding="utf-8-sig",newline="") as handle:
        rows=list(csv.DictReader(handle))
    ufs={row.get("uf","").strip().upper() for row in rows}
    check(ufs==EXPECTED, f"Conjunto de UFs inválido: faltantes={sorted(EXPECTED-ufs)} extras={sorted(ufs-EXPECTED)}")
    check(len(rows)==27, "CSV deve ter exatamente 27 linhas territoriais")
    check(len(ufs)==len(rows), "Há duplicidade de UF")
    for row in rows:
        try:
            check(float(row["populacao"])>0, f"População inválida em {row['uf']}")
            check(float(row["denuncias"])>=0, f"Denúncias inválidas em {row['uf']}")
            iv=float(row["eixo_vulnerabilidade"])
            check(0<=iv<=100, f"IVPD fora do intervalo em {row['uf']}")
        except Exception as exc:
            errors.append(f"Erro numérico em {row.get('uf')}: {exc}")

if json_path.exists():
    try:
        payload=json.loads(json_path.read_text(encoding="utf-8"))
        check(isinstance(payload,list) and len(payload)==27, "JSON deve conter lista com 27 UFs")
        check({str(row.get("uf","")).upper() for row in payload}==EXPECTED, "JSON não contém as 27 UFs esperadas")
    except Exception as exc:
        errors.append(f"JSON principal inválido: {exc}")

for endpoint in ["index.json","territories.json","indicators.json","sources.json","quality.json"]:
    path=ROOT/"web/api/v1"/endpoint
    check(path.exists(), f"Endpoint ausente: {endpoint}")
    if path.exists():
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"JSON inválido em {endpoint}: {exc}")

if panel_path.exists():
    html=panel_path.read_text(encoding="utf-8")
    for token in ['id="uf"','id="vuln"','id="taxa"','id="internet"','id="banda"','id="bars"','id="compare-1"','id="compare-2"','id="compare-3"','id="comparison"','id="download"','id="download-standard"','id="download-comparison"']:
        check(token in html, f"Elemento obrigatório ausente no painel: {token}")

for page in ["index.html","painel.html","dados.html","metodologia.html","governanca.html","acessibilidade.html"]:
    path=ROOT/"web"/page
    check(path.exists(), f"Página ausente: {page}")
    if path.exists():
        text=path.read_text(encoding="utf-8")
        check('charset="utf-8"' in text.lower(), f"UTF-8 não declarado em {page}")
        check(not any(marker in text for marker in ("Ã","Â","â€")), f"Texto corrompido em {page}")

if errors:
    print("VALIDAÇÃO REPROVADA")
    for error in errors:
        print("-",error)
    sys.exit(1)

print("VALIDAÇÃO APROVADA — PROTEGE.DADOS 5.0")
