from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = ROOT / "evidence" / "audit"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)

parser = argparse.ArgumentParser(description="Auditoria consolidada do Protege.Dados 5.1")
parser.add_argument("--skip-browser", action="store_true")
args = parser.parse_args()

commands = [
    ("Validação dos dados e da release", [sys.executable, "scripts/validate_release.py"]),
    ("Validação estrutural do portal", [sys.executable, "scripts/validate_portal.py"]),
    ("Testes unitários Python", [sys.executable, "-m", "pytest", "-q"]),
]
if shutil.which("node"):
    commands.extend([
        ("Sintaxe JavaScript do site", ["node", "--check", "web/assets/site.js"]),
        ("Sintaxe JavaScript do painel", ["node", "--check", "web/assets/app.js"]),
    ])
if not args.skip_browser:
    commands.append(("Auditoria funcional Chromium", [sys.executable, "scripts/browser_audit.py"]))
commands.append(("Teste do atualizador executável", [sys.executable, "scripts/test_updater.py"]))

results = []
for name, command in commands:
    print(f"\n=== {name} ===", flush=True)
    timeout = 300 if "Chromium" in name else 180
    try:
        completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=timeout)
        output = (completed.stdout + completed.stderr).strip()
        returncode = completed.returncode
    except subprocess.TimeoutExpired as exc:
        output = ((exc.stdout or "") + (exc.stderr or "")).strip() + f"\nTempo máximo excedido: {timeout}s"
        returncode = 124
    print(output, flush=True)
    results.append({"name": name, "command": command, "returncode": returncode, "output": output})

report = {
    "project": "Protege.Dados", "version": "5.1",
    "executed_at_utc": datetime.now(timezone.utc).isoformat(),
    "passed": sum(item["returncode"] == 0 for item in results),
    "failed": sum(item["returncode"] != 0 for item in results),
    "results": results,
}
(AUDIT_DIR / "full_audit_5_1.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
lines = ["# Relatório consolidado de auditoria — Protege.Dados 5.1", "", f"Execução UTC: {report['executed_at_utc']}", f"Etapas aprovadas: {report['passed']}", f"Etapas reprovadas: {report['failed']}", ""]
for item in results:
    lines.extend([f"## {'APROVADO' if item['returncode'] == 0 else 'REPROVADO'} — {item['name']}", "", "```text", item["output"], "```", ""])
(AUDIT_DIR / "RELATORIO_CONSOLIDADO_AUDITORIA_5_1.md").write_text("\n".join(lines), encoding="utf-8")
if report["failed"]:
    sys.exit(1)
print(f"\nAUDITORIA COMPLETA APROVADA — {report['passed']} etapas")
