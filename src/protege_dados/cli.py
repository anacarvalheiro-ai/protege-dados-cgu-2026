from __future__ import annotations
from pathlib import Path
import argparse, json
from .pipeline import run

def main():
    parser=argparse.ArgumentParser(prog="protege-dados")
    parser.add_argument("command", choices=["run"])
    parser.add_argument("--root", default=".")
    args=parser.parse_args()
    if args.command=="run":
        summary=run(Path(args.root).resolve())
        print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
