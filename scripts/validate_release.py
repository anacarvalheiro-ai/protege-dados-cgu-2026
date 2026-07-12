from pathlib import Path
import csv, json, sys

ROOT=Path(__file__).resolve().parents[1]
EXPECTED={"AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"}
errors=[]
def check(condition,message):
    if not condition: errors.append(message)

csv_path=ROOT/"data/processed/ivpd_uf_v1.csv"
json_path=ROOT/"web/data/ivpd_uf_v1.json"
html_path=ROOT/"web/index.html"
js_path=ROOT/"web/assets/app.js"
css_path=ROOT/"web/assets/style.css"
check(csv_path.exists(),"CSV derivado ausente")
check(json_path.exists(),"JSON do portal ausente")
check(html_path.exists(),"index.html ausente")
check(js_path.exists(),"app.js ausente")
check(css_path.exists(),"style.css ausente")

rows=[]
if csv_path.exists():
    with csv_path.open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
    ufs={r.get("uf","").strip().upper() for r in rows}
    check(ufs==EXPECTED,f"Conjunto de UFs inválido: faltantes={sorted(EXPECTED-ufs)} extras={sorted(ufs-EXPECTED)}")
    check(len(rows)==27,"CSV deve ter exatamente 27 linhas territoriais")
    check(len(ufs)==len(rows),"Há duplicidade de UF")
    for r in rows:
        try:
            check(float(r["populacao"])>0,f"População inválida em {r['uf']}")
            check(float(r["denuncias"])>=0,f"Denúncias inválidas em {r['uf']}")
            iv=float(r["eixo_vulnerabilidade"])
            check(0<=iv<=100,f"IVPD fora do intervalo em {r['uf']}")
            check(r.get("eixo_protecao","").strip()=="" or r.get("eixo_protecao","").lower()=="nan",f"Eixo de proteção não deveria estar publicado em {r['uf']}")
        except Exception as e: errors.append(f"Erro numérico em {r.get('uf')}: {e}")

if json_path.exists():
    payload=json.loads(json_path.read_text(encoding="utf-8"))
    check(isinstance(payload,list) and len(payload)==27,"JSON deve conter lista com 27 UFs")

for endpoint in ["index.json","territories.json","indicators.json","sources.json","quality.json"]:
    p=ROOT/"web/api/v1"/endpoint
    check(p.exists(),f"Endpoint ausente: {endpoint}")
    if p.exists():
        try: json.loads(p.read_text(encoding="utf-8"))
        except Exception as e: errors.append(f"JSON inválido em {endpoint}: {e}")

if html_path.exists():
    html=html_path.read_text(encoding="utf-8")
    for token in ['id="uf"','id="vuln"','id="taxa"','id="internet"','id="banda"','id="bars"','id="compare-1"','id="compare-2"','id="compare-3"','id="comparison"']:
        check(token in html,f"Elemento obrigatório ausente no HTML: {token}")
    check("Protege.Dados 4.1" in html,"Versão 4.1 não identificada no portal")
    check("qr_portal.png" in html and "qr_repositorio.png" in html,"QR Codes não referenciados no portal")

for qr in ["qr_portal.png","qr_repositorio.png"]:
    check((ROOT/"web/assets"/qr).exists(),f"QR Code ausente: {qr}")

if errors:
    print("VALIDAÇÃO REPROVADA")
    for e in errors: print("-",e)
    sys.exit(1)
print("VALIDAÇÃO APROVADA — PROTEGE.DADOS 4.1")
