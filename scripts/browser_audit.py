from __future__ import annotations

import contextlib
import csv
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
EVIDENCE = ROOT / "evidence"
SCREENSHOTS = EVIDENCE / "screenshots"
AUDIT = EVIDENCE / "audit"
PAGES = ["index.html", "painel.html", "dados.html", "metodologia.html", "governanca.html", "acessibilidade.html", "404.html"]

try:
    from playwright.sync_api import sync_playwright, expect
except ImportError:
    print("Playwright não está instalado. Execute: python -m pip install playwright")
    sys.exit(2)


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_server(url: str, timeout: float = 15.0) -> None:
    deadline = time.time() + timeout
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status < 500:
                    return
        except Exception as exc:
            last_error = exc
            time.sleep(0.2)
    raise RuntimeError(f"Servidor local não respondeu: {last_error}")


def run() -> dict:
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    AUDIT.mkdir(parents=True, exist_ok=True)
    for old in SCREENSHOTS.glob("*.png"):
        old.unlink()

    port = free_port()
    base_url = f"http://127.0.0.1:{port}"
    server_log = AUDIT / "http_server.log"
    with server_log.open("w", encoding="utf-8") as log:
        server = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", str(WEB)],
            stdout=log,
            stderr=subprocess.STDOUT,
        )

    results: list[dict] = []
    failures: list[str] = []
    console_errors: list[str] = []
    failed_requests: list[str] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        results.append({"name": name, "passed": bool(condition), "detail": detail})
        if not condition:
            failures.append(f"{name}: {detail}")

    try:
        wait_server(f"{base_url}/index.html")
        with sync_playwright() as playwright:
            executable = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
            launch_kwargs = {"headless": True, "args": ["--no-sandbox", "--disable-dev-shm-usage"]}
            if executable:
                launch_kwargs["executable_path"] = executable
            browser = playwright.chromium.launch(**launch_kwargs)
            context = browser.new_context(viewport={"width": 1440, "height": 1000}, accept_downloads=True, locale="pt-BR")
            page = context.new_page()
            page.on("console", lambda msg: console_errors.append(f"{page.url}: {msg.text}") if msg.type == "error" else None)
            page.on("requestfailed", lambda request: failed_requests.append(f"{request.url}: {request.failure}"))

            # Carregamento e evidências visuais de todas as páginas.
            for filename in PAGES:
                response = page.goto(f"{base_url}/{filename}", wait_until="networkidle")
                check(f"HTTP {filename}", response is not None and response.ok, f"status={response.status if response else 'sem resposta'}")
                check(f"Título {filename}", bool(page.title().strip()), page.title())
                check(f"Main {filename}", page.locator("main#conteudo").count() == 1, "main#conteudo")
                check(f"Sem overflow desktop {filename}", page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 2"), f"scroll={page.evaluate('document.documentElement.scrollWidth')} client={page.evaluate('document.documentElement.clientWidth')}")
                page.screenshot(path=str(SCREENSHOTS / filename.replace(".html", "_desktop.png")), full_page=True)

            # Início e dados nacionais.
            page.goto(f"{base_url}/index.html", wait_until="networkidle")
            expect(page.locator("#portal-status")).to_contain_text("27 UFs")
            check("Início carrega 27 UFs", "27 UFs" in page.locator("#portal-status").inner_text())
            check("Total nacional de escolas", page.locator("#home-total-escolas").inner_text() == "181.065", page.locator("#home-total-escolas").inner_text())
            check("Total nacional de matrículas", page.locator("#home-total-matriculas").inner_text() == "47.088.922", page.locator("#home-total-matriculas").inner_text())
            check("Total nacional de denúncias", page.locator("#home-total-denuncias").inner_text() == "294.592", page.locator("#home-total-denuncias").inner_text())

            # Painel e comparação.
            page.goto(f"{base_url}/painel.html", wait_until="networkidle")
            expect(page.locator("#portal-status")).to_contain_text("27 UFs")
            check("Seletor contém 27 UFs", page.locator("#uf option").count() == 27, str(page.locator("#uf option").count()))
            page.select_option("#uf", "SP")
            expect(page.locator("#selected-name")).to_contain_text("São Paulo")
            check("Troca de UF atualiza painel", "São Paulo" in page.locator("#selected-name").inner_text())
            check("IVPD selecionado é numérico", page.locator("#vuln").inner_text() not in {"—", ""}, page.locator("#vuln").inner_text())

            page.locator('[data-panel-tab="mapa"]').click()
            check("Cartograma possui 27 UFs", page.locator("#uf-map .map-tile").count() == 27, str(page.locator("#uf-map .map-tile").count()))
            page.locator('#uf-map .map-tile', has_text="DF").click()
            check("Cartograma atualiza UF", "Distrito Federal" in page.locator("#selected-name").inner_text(), page.locator("#selected-name").inner_text())
            page.screenshot(path=str(SCREENSHOTS / "painel_mapa_desktop.png"), full_page=True)

            page.locator('[data-panel-tab="comparacao"]').click()
            page.select_option("#compare-1", "DF")
            page.select_option("#compare-2", "SP")
            page.select_option("#compare-3", "BA")
            page.locator("#compare-button").click()
            check("Comparação gera três cartões", page.locator("#comparison .compare-card").count() == 3, str(page.locator("#comparison .compare-card").count()))
            check("Comparação gera três linhas", page.locator("#comparison-table-body tr").count() == 3, str(page.locator("#comparison-table-body tr").count()))
            page.screenshot(path=str(SCREENSHOTS / "painel_comparacao_desktop.png"), full_page=True)

            with page.expect_download() as download_info:
                page.locator("#download-comparison").click()
            download_path = Path(download_info.value.path())
            check("Download da comparação", download_path.exists() and download_path.stat().st_size > 100, f"bytes={download_path.stat().st_size if download_path.exists() else 0}")

            page.locator('[data-panel-tab="visao"]').click()
            with page.expect_download() as download_info:
                page.locator("#download").click()
            uf_download = Path(download_info.value.path())
            check("Download Excel por UF", uf_download.exists() and uf_download.stat().st_size > 100, f"bytes={uf_download.stat().st_size if uf_download.exists() else 0}")

            page.locator('[data-panel-tab="tabela"]').click()
            check("Tabela contém 27 UFs", page.locator("#uf-table-body tr").count() == 27, str(page.locator("#uf-table-body tr").count()))

            # Dados abertos e filtros.
            page.goto(f"{base_url}/dados.html", wait_until="networkidle")
            check("Dados apresenta nove recursos", page.locator("#resource-list .resource-card").count() == 9, str(page.locator("#resource-list .resource-card").count()))
            page.select_option("#resource-category", "API")
            visible_api = page.locator("#resource-list .resource-card:visible").count()
            check("Filtro por API", visible_api == 5, str(visible_api))
            page.locator("#resource-clear").click()
            page.select_option("#resource-format", "CSV")
            visible_csv = page.locator("#resource-list .resource-card:visible").count()
            check("Filtro por CSV", visible_csv == 2, str(visible_csv))
            page.locator("#resource-clear").click()
            page.fill("#resource-search", "dicionário")
            check("Busca textual", page.locator("#resource-list .resource-card:visible").count() == 1, str(page.locator("#resource-list .resource-card:visible").count()))
            page.locator("#resource-clear").click()
            check("Limpar filtros restaura recursos", page.locator("#resource-list .resource-card:visible").count() == 9, str(page.locator("#resource-list .resource-card:visible").count()))

            # Metodologia e governança.
            page.goto(f"{base_url}/metodologia.html", wait_until="networkidle")
            check("Fórmula metodológica publicada", "IVPD =" in page.locator(".formula").inner_text())
            check("Sumário metodológico possui seis links", page.locator(".toc a").count() == 6, str(page.locator(".toc a").count()))

            page.goto(f"{base_url}/governanca.html", wait_until="networkidle")
            check("Governança possui cinco salvaguardas", page.locator(".accordion details").count() == 5, str(page.locator(".accordion details").count()))
            second = page.locator(".accordion details").nth(1)
            second.locator("summary").click()
            check("Accordion de governança abre", second.get_attribute("open") is not None)

            # Acessibilidade e persistência.
            page.goto(f"{base_url}/acessibilidade.html", wait_until="networkidle")
            page.locator("#contrast-toggle").click()
            page.locator("#font-toggle").click()
            page.locator("#links-toggle").click()
            page.locator("#motion-toggle").click()
            check("Alto contraste aplicado", page.locator("body").evaluate("el => el.classList.contains('high-contrast')"))
            check("Fonte ampliada aplicada", page.locator("html").evaluate("el => el.classList.contains('font-large')"))
            check("Links sublinhados aplicados", page.locator("body").evaluate("el => el.classList.contains('links-underlined')"))
            check("Movimento reduzido aplicado", page.locator("body").evaluate("el => el.classList.contains('reduce-motion')"))
            page.reload(wait_until="networkidle")
            check("Preferências persistem após reload", page.locator("body").evaluate("el => el.classList.contains('high-contrast') && el.classList.contains('links-underlined') && el.classList.contains('reduce-motion')") and page.locator("html").evaluate("el => el.classList.contains('font-large')"))
            # Restaura preferências para capturas futuras.
            for selector in ["#contrast-toggle", "#font-toggle", "#links-toggle", "#motion-toggle"]:
                if page.locator(selector).get_attribute("aria-pressed") == "true":
                    page.locator(selector).click()

            # Responsividade e menu móvel.
            mobile = browser.new_context(viewport={"width": 390, "height": 844}, locale="pt-BR")
            mobile_page = mobile.new_page()
            mobile_errors: list[str] = []
            mobile_page.on("console", lambda msg: mobile_errors.append(msg.text) if msg.type == "error" else None)
            for filename in PAGES[:-1]:
                mobile_page.goto(f"{base_url}/{filename}", wait_until="networkidle")
                overflow = mobile_page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 2")
                check(f"Sem overflow móvel {filename}", overflow, f"scroll={mobile_page.evaluate('document.documentElement.scrollWidth')} client={mobile_page.evaluate('document.documentElement.clientWidth')}")
            mobile_page.goto(f"{base_url}/index.html", wait_until="networkidle")
            mobile_page.locator("#menu-toggle").click()
            check("Menu móvel abre", mobile_page.locator("#nav-links").evaluate("el => el.classList.contains('open')"))
            check("Menu móvel expõe seis links", mobile_page.locator("#nav-links a").count() == 6, str(mobile_page.locator("#nav-links a").count()))
            mobile_page.screenshot(path=str(SCREENSHOTS / "index_mobile.png"), full_page=True)
            check("Console móvel sem erros", not mobile_errors, "; ".join(mobile_errors))
            mobile.close()

            check("Console desktop sem erros", not console_errors, "; ".join(console_errors))
            check("Sem requisições falhas", not failed_requests, "; ".join(failed_requests))
            context.close()
            browser.close()
    finally:
        server.terminate()
        with contextlib.suppress(Exception):
            server.wait(timeout=5)
        if server.poll() is None:
            server.kill()

    report = {
        "project": "Protege.Dados",
        "version": "5.1",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "checks": len(results),
        "passed": sum(1 for item in results if item["passed"]),
        "failed": len(failures),
        "failures": failures,
        "console_errors": console_errors,
        "failed_requests": failed_requests,
        "results": results,
    }
    (AUDIT / "browser_audit_5_1.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [
        "# Auditoria funcional por navegador — Protege.Dados 5.1",
        "",
        f"- Execução UTC: {report['executed_at_utc']}",
        f"- Verificações: {report['checks']}",
        f"- Aprovadas: {report['passed']}",
        f"- Falhas: {report['failed']}",
        "",
        "## Resultado detalhado",
        "",
    ]
    for item in results:
        mark = "✅" if item["passed"] else "❌"
        detail = f" — {item['detail']}" if item["detail"] else ""
        md.append(f"- {mark} {item['name']}{detail}")
    if failures:
        md.extend(["", "## Falhas", ""] + [f"- {failure}" for failure in failures])
    (AUDIT / "RELATORIO_AUDITORIA_NAVEGADOR_5_1.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    report = run()
    if report["failed"]:
        print(f"AUDITORIA FUNCIONAL REPROVADA — {report['failed']} falha(s)")
        for failure in report["failures"]:
            print("-", failure)
        sys.exit(1)
    print(f"AUDITORIA FUNCIONAL APROVADA — {report['passed']}/{report['checks']} verificações")
