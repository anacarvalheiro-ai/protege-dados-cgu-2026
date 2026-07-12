from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import json, sys
ROOT=Path(__file__).resolve().parents[1]
WEB=ROOT/'web'
class Parser(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]
    def handle_starttag(self,tag,attrs):
        values=dict(attrs)
        for key in ('href','src'):
            if key in values: self.links.append(values[key])
def check_html(path:Path):
    p=Parser(); p.feed(path.read_text(encoding='utf-8'))
    errors=[]
    for link in p.links:
        if not link or link.startswith(('#','mailto:','tel:','data:','javascript:')): continue
        if urlparse(link).scheme in ('http','https'): continue
        clean=unquote(link.split('#')[0].split('?')[0])
        if not clean: continue
        target=(path.parent/clean).resolve()
        if not target.exists(): errors.append(f'{path.relative_to(ROOT)} -> {link}')
    return errors
def main():
    errors=[]
    for p in WEB.rglob('*.html'): errors.extend(check_html(p))
    for p in WEB.rglob('*.json'):
        try: json.loads(p.read_text(encoding='utf-8'))
        except Exception as e: errors.append(f'{p.relative_to(ROOT)} JSON inválido: {e}')
    if errors:
        print('\n'.join(errors)); sys.exit(1)
    print('Links locais e JSON validados.')
if __name__=='__main__': main()
