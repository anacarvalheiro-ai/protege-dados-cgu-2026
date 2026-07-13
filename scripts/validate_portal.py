from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
PAGES = sorted(WEB.glob("*.html"))
EXPECTED_UFS = {"AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"}

errors: list[str] = []
checks = 0

class PortalParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.refs: list[tuple[str, str]] = []
        self.has_main = False
        self.has_title = False
        self.has_skip = False
        self.has_nav_label = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.append(str(data["id"]))
        for attr in ("href", "src"):
            if data.get(attr):
                self.refs.append((attr, str(data[attr])))
        if tag == "main" and data.get("id") == "conteudo":
            self.has_main = True
        if tag == "title":
            self.has_title = True
        if tag == "a" and data.get("class") == "skip" and data.get("href") == "#conteudo":
            self.has_skip = True
        if tag == "nav" and data.get("aria-label"):
            self.has_nav_label = True

def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        errors.append(message)

try:
    data = json.loads((WEB / "data/ivpd_uf_v1.json").read_text(encoding="utf-8"))
except Exception as exc:
    data = []
    errors.append(f"JSON principal inválido: {exc}")
check(len(data) == 27, f"Total de UFs diferente de 27: {len(data)}")
check({str(row.get('uf','')).upper() for row in data if isinstance(row, dict)} == EXPECTED_UFS, "Conjunto de UFs incorreto")

required_nav = {"index.html", "painel.html", "dados.html", "metodologia.html", "governanca.html", "acessibilidade.html"}
for page in PAGES:
    text = page.read_text(encoding="utf-8")
    parser = PortalParser()
    try:
        parser.feed(text)
    except Exception as exc:
        errors.append(f"HTML não pôde ser analisado em {page.name}: {exc}")
        continue

    check(parser.has_title, f"Título ausente: {page.name}")
    check(parser.has_main, f"Elemento main#conteudo ausente: {page.name}")
    check(parser.has_skip, f"Link para pular ao conteúdo ausente: {page.name}")
    check(parser.has_nav_label, f"Rótulo da navegação principal ausente: {page.name}")
    duplicates = sorted({id_ for id_ in parser.ids if parser.ids.count(id_) > 1})
    check(not duplicates, f"IDs duplicados em {page.name}: {duplicates}")

    local_nav = {ref.split("?", 1)[0].split("#", 1)[0] for attr, ref in parser.refs if attr == "href" and ref.endswith(".html")}
    if page.name != "404.html":
        check(required_nav.issubset(local_nav), f"Navegação incompleta em {page.name}: faltam {sorted(required_nav-local_nav)}")

    for attr, target in parser.refs:
        if target.startswith(("http://", "https://", "mailto:", "tel:", "#", "javascript:")):
            continue
        clean = target.split("?", 1)[0].split("#", 1)[0]
        if not clean:
            continue
        path = (page.parent / clean).resolve()
        try:
            path.relative_to(WEB.resolve())
        except ValueError:
            errors.append(f"Referência sai da pasta web em {page.name}: {target}")
            continue
        check(path.exists(), f"Referência ausente em {page.name}: {target}")

for path in (WEB / "api/v1").glob("*.json"):
    try:
        json.loads(path.read_text(encoding="utf-8"))
        checks += 1
    except Exception as exc:
        errors.append(f"API inválida {path.name}: {exc}")

css = (WEB / "assets/style.css").read_text(encoding="utf-8")
check("@media (max-width: 620px)" in css, "Breakpoint móvel principal ausente no CSS")
check(":focus-visible" in css, "Estado de foco visível ausente no CSS")
check("prefers-reduced-motion" in css, "Preferência de movimento reduzido ausente no CSS")

for script in [WEB / "assets/site.js", WEB / "assets/app.js"]:
    text = script.read_text(encoding="utf-8")
    check('"use strict"' in text, f"Modo estrito ausente em {script.name}")

stale = []
for path in list(WEB.glob("*.html")) + [WEB / "assets/site.js", WEB / "assets/app.js"]:
    content = path.read_text(encoding="utf-8")
    if re.search(r"Protege\.Dados\s+5\.2|<small>5\.2</small>|v=5\.2", content):
        stale.append(path.name)
check(not stale, f"Referências antigas à versão 5.2: {stale}")

if errors:
    print("VALIDAÇÃO DO PORTAL REPROVADA")
    for error in errors:
        print("-", error)
    sys.exit(1)

print(f"VALIDAÇÃO DO PORTAL APROVADA — {len(PAGES)} páginas | {checks} verificações")
