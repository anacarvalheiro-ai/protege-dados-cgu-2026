from __future__ import annotations
import csv, hashlib, json, re, sys
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
WEB=ROOT/'web'
EXPECTED={'AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO'}
checks=[]
issues=[]

def check(name, condition, detail=''):
    checks.append({'name':name,'ok':bool(condition),'detail':detail})
    if not condition: issues.append(f'{name}: {detail}')

# HTML structure, accessibility and local assets
pages=sorted(WEB.glob('*.html'))
check('Quantidade de páginas HTML', len(pages)>=7, f'{len(pages)} páginas')
for page in pages:
    text=page.read_text(encoding='utf-8')
    soup=BeautifulSoup(text,'html.parser')
    check(f'{page.name}: idioma', soup.html and soup.html.get('lang')=='pt-BR','lang=pt-BR')
    check(f'{page.name}: título', bool(soup.title and soup.title.string and soup.title.string.strip()), str(soup.title))
    check(f'{page.name}: viewport', bool(soup.find('meta',attrs={'name':'viewport'})),'meta viewport')
    check(f'{page.name}: descrição', bool(soup.find('meta',attrs={'name':'description'})),'meta description')
    check(f'{page.name}: conteúdo principal', len(soup.select('main#conteudo'))==1,'main#conteudo único')
    check(f'{page.name}: pular conteúdo', bool(soup.select_one('a.skip[href="#conteudo"]')),'skip link')
    ids=[tag.get('id') for tag in soup.find_all(attrs={'id':True})]
    check(f'{page.name}: IDs únicos', len(ids)==len(set(ids)),f'{len(ids)} IDs')
    nav=soup.find('nav')
    if nav:
        check(f'{page.name}: rótulo da navegação', bool(nav.get('aria-label')),'aria-label')
    for tag in soup.find_all(['a','link','script','img']):
        attr='href' if tag.name in {'a','link'} else 'src'
        target=tag.get(attr)
        if not target or target.startswith(('#','http://','https://','mailto:','javascript:','data:')): continue
        clean=target.split('?',1)[0].split('#',1)[0]
        dest=(page.parent/clean).resolve()
        check(f'{page.name}: recurso {target}', dest.exists(), str(dest.relative_to(ROOT)) if dest.exists() else 'ausente')

# JSON and API consistency
main=json.loads((WEB/'data/ivpd_uf_v1.json').read_text(encoding='utf-8'))
check('JSON principal: lista', isinstance(main,list),'lista JSON')
check('JSON principal: 27 registros', len(main)==27,str(len(main)))
ufs=[str(x.get('uf','')).upper() for x in main]
check('JSON principal: UFs exatas', set(ufs)==EXPECTED and len(ufs)==len(set(ufs)),','.join(sorted(set(ufs))))
for row in main:
    uf=row.get('uf','?')
    for key in ('populacao','escolas','matriculas','denuncias','eixo_vulnerabilidade'):
        value=row.get(key)
        check(f'{uf}: campo {key}', isinstance(value,(int,float)) and value>=0,str(value))
    iv=row.get('eixo_vulnerabilidade')
    check(f'{uf}: IVPD 0-100', isinstance(iv,(int,float)) and 0<=iv<=100,str(iv))

territ=json.loads((WEB/'api/v1/territories.json').read_text(encoding='utf-8'))
terr_list=territ.get('territories') if isinstance(territ,dict) else territor
check('API territórios: 27 registros', isinstance(terr_list,list) and len(terr_list)==27,str(len(terr_list) if isinstance(terr_list,list) else type(terr_list)))
check('API territórios igual ao JSON principal', terr_list==main,'conteúdo idêntico')
for endpoint in sorted((WEB/'api/v1').glob('*.json')):
    try:
        data=json.loads(endpoint.read_text(encoding='utf-8'))
        check(f'API {endpoint.name}: JSON válido',True,'válido')
        if isinstance(data,dict) and 'version' in data:
            check(f'API {endpoint.name}: versão 5.1.0',data['version']=='5.1.0',str(data['version']))
    except Exception as exc:
        check(f'API {endpoint.name}: JSON válido',False,str(exc))

# CSV downloadable consistency
for csvfile in [WEB/'downloads/ivpd_uf_v1.csv',WEB/'downloads/ivpd_uf_v1_excel.csv',ROOT/'data/processed/ivpd_uf_v1.csv']:
    delimiter=';' if 'excel' in csvfile.name else ','
    with csvfile.open(encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f,delimiter=delimiter))
    check(f'{csvfile.name}: 27 linhas',len(rows)==27,str(len(rows)))
    check(f'{csvfile.name}: UFs exatas',{r.get('uf','').upper() for r in rows}==EXPECTED,'27 UFs')

# JavaScript and interactive contract
js=(WEB/'assets/app.js').read_text(encoding='utf-8')
for token in ['loadRows','renderUf','renderComparison','createCsv','download','renderTable']:
    check(f'JavaScript: função {token}',f'function {token}' in js,token)
check('JavaScript: versão de cache 5.1.0','v=5.1.0' in js,'5.1.0')
panel=(WEB/'painel.html').read_text(encoding='utf-8')
for control in ['uf','compare-1','compare-2','compare-3','compare-button','download','download-standard','download-comparison','uf-table-body']:
    check(f'Painel: controle {control}',f'id="{control}"' in panel,control)

# Version consistency
stale=[]
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in {'.html','.md','.txt','.py','.json','.cff','.yml','.yaml'} and '.pytest_cache' not in p.parts and p.name != 'audit_complete.py' and p.name != 'auditoria_completa_5_1.json':
        try: s=p.read_text(encoding='utf-8')
        except Exception: continue
        for pattern in ['Protege.Dados 5.0','PROTEGE.DADOS 5.0','<small>5.0</small>','"version": "5.0.0"']:
            if pattern in s: stale.append(f'{p.relative_to(ROOT)}: {pattern}')
check('Consistência da versão 5.1',not stale,'; '.join(stale) if stale else 'sem rótulos 5.0 ativos')

# Deployment essentials
for rel in ['web/.nojekyll','web/404.html','web/robots.txt','web/site.webmanifest','LICENSE','README.md','CHANGELOG.md','SECURITY.md']:
    check(f'Arquivo de implantação {rel}',(ROOT/rel).exists(),rel)

# hashes
hashes={}
for p in sorted(WEB.rglob('*')):
    if p.is_file(): hashes[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
(ROOT/'evidence/audit_web_sha256.json').write_text(json.dumps({'version':'5.1.0','files':hashes},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

report={'version':'5.1.0','total_checks':len(checks),'passed':sum(c['ok'] for c in checks),'failed':len(issues),'issues':issues,'checks':checks}
(ROOT/'evidence/auditoria_completa_5_1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ('version','total_checks','passed','failed','issues')},ensure_ascii=False,indent=2))
sys.exit(1 if issues else 0)
