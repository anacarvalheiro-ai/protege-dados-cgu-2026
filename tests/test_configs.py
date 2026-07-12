import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_json_configs():
    for p in (ROOT/"web/config").glob("*.json"): json.loads(p.read_text(encoding="utf-8"))
def test_menu_targets_exist():
    menu=json.loads((ROOT/"web/config/menu.json").read_text(encoding="utf-8"))
    for item in menu:
        assert (ROOT/"web"/item["url"]).exists(), item["url"]
