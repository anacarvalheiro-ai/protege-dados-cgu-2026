from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def ignore(path: str, names: list[str]) -> set[str]:
    return {name for name in names if name in {".git", ".pytest_cache", "__pycache__", "logs"} or name.endswith((".pyc", ".pyo"))}


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="protege-updater-test-") as temporary:
        temp = Path(temporary)
        target = temp / "protege-dados-cgu-2026"
        shutil.copytree(ROOT, target, ignore=ignore)

        # Simula uma instalação anterior para confirmar a substituição.
        index = target / "web" / "index.html"
        index.write_text(index.read_text(encoding="utf-8").replace("<small>5.1</small>", "<small>5.0</small>"), encoding="utf-8")
        stale = target / "web" / "arquivo_obsoleto.tmp"
        stale.write_text("remover", encoding="utf-8")

        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "atualizar_protege_dados_5_1.py"),
                "--target", str(target),
                "--non-interactive",
                "--skip-install",
                "--skip-browser",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print(completed.stdout)
        if completed.returncode != 0:
            return completed.returncode

        checks = {
            "versao_5_1": "<small>5.1</small>" in index.read_text(encoding="utf-8"),
            "site_js": (target / "web" / "assets" / "site.js").exists(),
            "arquivo_obsoleto_removido": not stale.exists(),
            "log_criado": bool(list((target / "logs").glob("atualizacao-5-1-*.log"))),
            "backup_criado": bool(list((temp / "Backups_Protege_Dados").glob("*.zip"))),
        }
        for name, passed in checks.items():
            print(f"{'OK' if passed else 'FALHA'} — {name}")
        if not all(checks.values()):
            return 1
        print(f"TESTE DO ATUALIZADOR APROVADO — {sum(checks.values())}/{len(checks)} verificações")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
