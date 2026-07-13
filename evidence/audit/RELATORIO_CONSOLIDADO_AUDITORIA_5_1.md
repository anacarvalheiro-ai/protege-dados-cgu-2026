# Relatório consolidado de auditoria — Protege.Dados 5.1

Execução UTC: 2026-07-13T18:44:01.724309+00:00
Etapas aprovadas: 6
Etapas reprovadas: 0

## APROVADO — Validação dos dados e da release

```text
VALIDAÇÃO APROVADA — PROTEGE.DADOS 5.1 | 162 verificações
```

## APROVADO — Validação estrutural do portal

```text
VALIDAÇÃO DO PORTAL APROVADA — 7 páginas | 173 verificações
```

## APROVADO — Testes unitários Python

```text
...                                                                      [100%]
3 passed in 0.11s
```

## APROVADO — Sintaxe JavaScript do site

```text

```

## APROVADO — Sintaxe JavaScript do painel

```text

```

## APROVADO — Teste do atualizador executável

```text
==============================================================
ATUALIZADOR PROFISSIONAL — PROTEGE.DADOS 5.1
Origem: /mnt/data/Protege_Dados_5_1_MASTER_ATUALIZACAO
Destino: /tmp/protege-updater-test-xqkjw27s/protege-dados-cgu-2026
==============================================================
Backup criado: /tmp/protege-updater-test-xqkjw27s/Backups_Protege_Dados/Protege_Dados_antes_5_1_20260713-184354.zip
Pasta atualizada: .github
Pasta atualizada: config
Pasta atualizada: data
Pasta atualizada: docs
Pasta atualizada: evidence
Pasta atualizada: scripts
Pasta atualizada: src
Pasta atualizada: tests
Pasta atualizada: web
Arquivo atualizado: pyproject.toml
Arquivo atualizado: LICENSE
Arquivo atualizado: DATA_LICENSE.md
Arquivo atualizado: SECURITY.md
Arquivo atualizado: CONTRIBUTING.md
Arquivo atualizado: CODE_OF_CONDUCT.md
Arquivo atualizado: CHANGELOG.md
Arquivo atualizado: CITATION.cff
Arquivo atualizado: .gitignore
Arquivo atualizado: README.md
Arquivo atualizado: INSTRUCOES_ATUALIZACAO_5_1.txt
Arquivo atualizado: ATUALIZAR_PROTEGE_DADOS_5_1.bat
Arquivo atualizado: Atualizar_Protege_Dados_5_1.ps1
Arquivo atualizado: atualizar_protege_dados_5_1.py
Arquivo atualizado: ABRIR_PREVIA_LOCAL.bat
Arquivo atualizado: PUBLICAR_NO_GITHUB_5_1.bat
Arquivo atualizado: Publicar_No_GitHub_5_1.ps1
Arquivo atualizado: PUBLICAR_NO_GITHUB.md
Arquivo atualizado: LEIA_PRIMEIRO.txt
$ /opt/pyvenv/bin/python scripts/validate_release.py
VALIDAÇÃO APROVADA — PROTEGE.DADOS 5.1 | 162 verificações
$ /opt/pyvenv/bin/python scripts/validate_portal.py
VALIDAÇÃO DO PORTAL APROVADA — 7 páginas | 173 verificações
$ /opt/pyvenv/bin/python -m pytest -q
...                                                                      [100%]
3 passed in 0.11s
$ /opt/nvm/versions/node/v22.16.0/bin/node --check web/assets/site.js
$ /opt/nvm/versions/node/v22.16.0/bin/node --check web/assets/app.js
Git não disponível ou pasta não é um repositório; commit não executado.
PROTEGE.DADOS 5.1 ATUALIZADO E VALIDADO COM SUCESSO.
Log: /tmp/protege-updater-test-xqkjw27s/protege-dados-cgu-2026/logs/atualizacao-5-1-20260713-184354.log

OK — versao_5_1
OK — site_js
OK — arquivo_obsoleto_removido
OK — log_criado
OK — backup_criado
TESTE DO ATUALIZADOR APROVADO — 5/5 verificações
```
