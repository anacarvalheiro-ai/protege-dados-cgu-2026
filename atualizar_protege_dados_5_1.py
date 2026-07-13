from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

VERSION = "5.1"
SOURCE = Path(__file__).resolve().parent
DIRECTORIES = [".github", "config", "data", "docs", "evidence", "scripts", "src", "tests", "web"]
ROOT_FILES = [
    "pyproject.toml", "LICENSE", "DATA_LICENSE.md", "SECURITY.md", "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md", "CHANGELOG.md", "CITATION.cff", ".gitignore", "README.md",
    "INSTRUCOES_ATUALIZACAO_5_1.txt", "ATUALIZAR_PROTEGE_DADOS_5_1.bat",
    "Atualizar_Protege_Dados_5_1.ps1", "atualizar_protege_dados_5_1.py",
    "ABRIR_PREVIA_LOCAL.bat", "PUBLICAR_NO_GITHUB_5_1.bat", "Publicar_No_GitHub_5_1.ps1",
    "PUBLICAR_NO_GITHUB.md", "LEIA_PRIMEIRO.txt",
]
EXCLUDED_NAMES = {".git", "__pycache__", ".pytest_cache", "logs"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Atualizador profissional do Protege.Dados 5.1")
    parser.add_argument("--target", help="Caminho do repositório a atualizar")
    parser.add_argument("--non-interactive", action="store_true", help="Não solicitar confirmação")
    parser.add_argument("--skip-install", action="store_true", help="Não executar pip install -e .")
    parser.add_argument("--skip-browser", action="store_true", help="Não executar auditoria Playwright")
    parser.add_argument("--no-backup", action="store_true", help="Não criar backup ZIP")
    parser.add_argument("--commit", action="store_true", help="Criar commit local após validação")
    parser.add_argument("--push", action="store_true", help="Enviar para origin/main; exige --commit")
    return parser.parse_args()


def ask(prompt: str, default: bool = False) -> bool:
    suffix = " [S/n] " if default else " [s/N] "
    value = input(prompt + suffix).strip().lower()
    if not value:
        return default
    return value in {"s", "sim", "y", "yes"}


def find_target() -> Path | None:
    home = Path.home()
    candidates = [
        home / "Documents" / "ProtegeDadosAtualizacao" / "protege-dados-cgu-2026",
        home / "Documents" / "protege-dados-cgu-2026",
        home / "Downloads" / "protege-dados-cgu-2026",
    ]
    return next((path for path in candidates if path.exists()), None)


def ignore_copy(path: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        if name in EXCLUDED_NAMES or Path(name).suffix in EXCLUDED_SUFFIXES:
            ignored.add(name)
    return ignored


def run_command(command: list[str], cwd: Path, logger, required: bool = True) -> bool:
    logger(f"$ {' '.join(command)}")
    completed = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if completed.stdout:
        logger(completed.stdout.rstrip())
    if completed.returncode != 0:
        message = f"Comando falhou com código {completed.returncode}: {' '.join(command)}"
        if required:
            raise RuntimeError(message)
        logger("AVISO: " + message)
        return False
    return True


def create_backup(target: Path, logger) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_parent = target.parent / "Backups_Protege_Dados"
    backup_parent.mkdir(parents=True, exist_ok=True)
    temp = backup_parent / f".temp_backup_{stamp}"
    archive_base = backup_parent / f"Protege_Dados_antes_5_1_{stamp}"
    if temp.exists():
        shutil.rmtree(temp)
    shutil.copytree(target, temp, ignore=ignore_copy)
    archive = Path(shutil.make_archive(str(archive_base), "zip", root_dir=temp))
    shutil.rmtree(temp)
    logger(f"Backup criado: {archive}")
    return archive


def copy_project(target: Path, logger) -> None:
    for directory in DIRECTORIES:
        source_dir = SOURCE / directory
        if not source_dir.exists():
            continue
        target_dir = target / directory
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(source_dir, target_dir, ignore=ignore_copy)
        logger(f"Pasta atualizada: {directory}")
    for name in ROOT_FILES:
        source_file = SOURCE / name
        if source_file.exists():
            shutil.copy2(source_file, target / name)
            logger(f"Arquivo atualizado: {name}")


def validate(target: Path, args: argparse.Namespace, logger) -> None:
    if not args.skip_install:
        run_command([sys.executable, "-m", "pip", "install", "-e", "."], target, logger)
    run_command([sys.executable, "scripts/validate_release.py"], target, logger)
    run_command([sys.executable, "scripts/validate_portal.py"], target, logger)
    run_command([sys.executable, "-m", "pytest", "-q"], target, logger)
    node = shutil.which("node")
    if node:
        run_command([node, "--check", "web/assets/site.js"], target, logger)
        run_command([node, "--check", "web/assets/app.js"], target, logger)
    else:
        logger("AVISO: Node.js não encontrado; o GitHub Actions fará a verificação JavaScript.")

    if not args.skip_browser and importlib.util.find_spec("playwright"):
        run_command([sys.executable, "scripts/browser_audit.py"], target, logger, required=False)
    elif not args.skip_browser:
        logger("AVISO: Playwright não instalado. O pacote contém auditoria funcional previamente aprovada.")


def git_actions(target: Path, args: argparse.Namespace, logger) -> None:
    git = shutil.which("git")
    if not git or not (target / ".git").exists():
        logger("Git não disponível ou pasta não é um repositório; commit não executado.")
        return
    commit = args.commit
    push = args.push
    if not args.non_interactive and not commit:
        commit = ask("Deseja criar um commit local da versão 5.1?")
    if not commit:
        return
    run_command([git, "add", "--all"], target, logger)
    status = subprocess.run([git, "status", "--porcelain"], cwd=target, text=True, capture_output=True, check=True).stdout
    if status.strip():
        run_command([git, "commit", "-m", "Atualiza interface e funcionalidades do Protege.Dados 5.1"], target, logger)
    else:
        logger("Nenhuma alteração pendente para commit.")
    if not args.non_interactive and not push:
        push = ask("Deseja enviar o commit para origin/main?")
    if push:
        run_command([git, "push", "origin", "main"], target, logger)


def main() -> int:
    args = parse_args()
    if args.push and not args.commit:
        print("ERRO: --push exige --commit", file=sys.stderr)
        return 2
    if not (SOURCE / "web" / "index.html").exists():
        print("ERRO: pacote incompleto; extraia todo o ZIP.", file=sys.stderr)
        return 2

    target = Path(args.target).expanduser().resolve() if args.target else find_target()
    if target is None and not args.non_interactive:
        target = Path(input("Caminho completo do repositório protege-dados-cgu-2026: ").strip()).expanduser().resolve()
    if target is None or not target.exists() or not target.is_dir():
        print(f"ERRO: repositório não encontrado: {target}", file=sys.stderr)
        return 2

    log_dir = target / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"atualizacao-5-1-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"

    def logger(message: str) -> None:
        text = str(message)
        print(text, flush=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(text + "\n")

    logger("=" * 62)
    logger("ATUALIZADOR PROFISSIONAL — PROTEGE.DADOS 5.1")
    logger(f"Origem: {SOURCE}")
    logger(f"Destino: {target}")
    logger("=" * 62)

    try:
        same_folder = SOURCE.resolve() == target.resolve()
        if not same_folder:
            if not args.no_backup:
                create_backup(target, logger)
            copy_project(target, logger)
        else:
            logger("Execução dentro do próprio repositório; cópia dispensada.")
        validate(target, args, logger)
        git_actions(target, args, logger)
        logger("PROTEGE.DADOS 5.1 ATUALIZADO E VALIDADO COM SUCESSO.")
        logger(f"Log: {log_path}")
        return 0
    except Exception as exc:
        logger(f"ERRO: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
