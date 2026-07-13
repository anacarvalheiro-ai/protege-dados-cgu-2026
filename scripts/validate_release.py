from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
EXPECTED_UFS = {"AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"}
EXPECTED_TOTALS = {
    "escolas": 181_065,
    "matriculas": 47_088_922,
    "denuncias": 294_592,
    "escolas_internet": 166_771,
    "escolas_banda_larga": 145_195,
}

errors: list[str] = []
checks = 0

def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        errors.append(message)

required_files = [
    ROOT / "data/processed/ivpd_uf_v1.csv",
    WEB / "data/ivpd_uf_v1.json",
    WEB / "downloads/ivpd_uf_v1.csv",
    WEB / "downloads/ivpd_uf_v1_excel.csv",
    WEB / "assets/style.css",
    WEB / "assets/site.js",
    WEB / "assets/app.js",
    WEB / "site.webmanifest",
    WEB / "robots.txt",
    WEB / "sitemap.xml",
]
for path in required_files:
    check(path.exists(), f"Arquivo obrigatório ausente: {path.relative_to(ROOT)}")

rows: list[dict] = []
csv_path = ROOT / "data/processed/ivpd_uf_v1.csv"
if csv_path.exists():
    with csv_path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    ufs = {row.get("uf", "").strip().upper() for row in rows}
    check(len(rows) == 27, "CSV derivado deve conter exatamente 27 linhas territoriais")
    check(ufs == EXPECTED_UFS, f"Conjunto de UFs inválido: faltantes={sorted(EXPECTED_UFS-ufs)} extras={sorted(ufs-EXPECTED_UFS)}")
    check(len(ufs) == len(rows), "Há duplicidade de UF no CSV derivado")
    for row in rows:
        uf = row.get("uf", "?")
        try:
            check(float(row["populacao"]) > 0, f"População inválida em {uf}")
            check(float(row["denuncias"]) >= 0, f"Denúncias inválidas em {uf}")
            ivpd = float(row["eixo_vulnerabilidade"])
            check(0 <= ivpd <= 100, f"IVPD fora do intervalo 0–100 em {uf}")
        except Exception as exc:
            errors.append(f"Erro numérico em {uf}: {exc}")

payload: list[dict] = []
json_path = WEB / "data/ivpd_uf_v1.json"
if json_path.exists():
    try:
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        check(isinstance(payload, list), "JSON principal deve ser uma lista")
        check(len(payload) == 27, "JSON principal deve conter 27 UFs")
        check({str(row.get("uf", "")).upper() for row in payload} == EXPECTED_UFS, "JSON principal não contém as 27 UFs esperadas")
        for key, expected in EXPECTED_TOTALS.items():
            actual = round(sum(float(row.get(key, 0) or 0) for row in payload))
            check(actual == expected, f"Total de {key} divergente: esperado={expected} obtido={actual}")
    except Exception as exc:
        errors.append(f"JSON principal inválido: {exc}")

for endpoint in ["index.json", "territories.json", "indicators.json", "sources.json", "quality.json"]:
    path = WEB / "api/v1" / endpoint
    check(path.exists(), f"Endpoint ausente: {endpoint}")
    if path.exists():
        try:
            json.loads(path.read_text(encoding="utf-8"))
            checks += 1
        except Exception as exc:
            errors.append(f"JSON inválido em {endpoint}: {exc}")

pages = ["index.html", "painel.html", "dados.html", "metodologia.html", "governanca.html", "acessibilidade.html", "404.html"]
for page in pages:
    path = WEB / page
    check(path.exists(), f"Página ausente: {page}")
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    check('charset="utf-8"' in text.lower(), f"UTF-8 não declarado em {page}")
    check('lang="pt-BR"' in text, f"Idioma pt-BR ausente em {page}")
    check("Protege.Dados 5.1" in text or "<small>5.1</small>" in text, f"Versão 5.1 não identificada em {page}")
    check(not any(marker in text for marker in ("Ã", "Â", "â€", "ï»¿")), f"Texto possivelmente corrompido em {page}")

panel = (WEB / "painel.html").read_text(encoding="utf-8") if (WEB / "painel.html").exists() else ""
for token in [
    'id="uf"','id="vuln"','id="taxa"','id="internet"','id="banda"','id="bars"',
    'id="compare-1"','id="compare-2"','id="compare-3"','id="comparison"','id="uf-map"',
    'id="download"','id="download-standard"','id="download-comparison"','id="uf-table-body"'
]:
    check(token in panel, f"Elemento obrigatório ausente no painel: {token}")

if errors:
    print("VALIDAÇÃO REPROVADA")
    for error in errors:
        print("-", error)
    sys.exit(1)

print(f"VALIDAÇÃO APROVADA — PROTEGE.DADOS 5.1 | {checks} verificações")
