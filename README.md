# Protege.Dados 5.1 — Ecossistema público de inteligência territorial

[![Portal](https://img.shields.io/badge/portal-GitHub%20Pages-0b73b9)](https://anacarvalheiro-ai.github.io/protege-dados-cgu-2026/)
[![Deploy](https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026/actions/workflows/deploy.yml/badge.svg)](https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026/actions/workflows/deploy.yml)
[![Release](https://img.shields.io/badge/release-5.1-56c7ff)](CHANGELOG.md)
[![Licença](https://img.shields.io/badge/c%C3%B3digo-MIT-06365f)](LICENSE)
[![Dados](https://img.shields.io/badge/dados-CSV%20%7C%20JSON-0873ba)](data/processed/ivpd_uf_v1.csv)

## Candidatura ao 2º Concurso de Reúso de Dados Abertos da CGU

O **Protege.Dados 5.1** integra dados oficiais de população, educação e denúncias administrativas e publica resultados agregados para as 27 unidades federativas. O portal foi redesenhado com base nos templates institucionais aprovados, preservando as funcionalidades de consulta, comparação, filtros, downloads, API e acessibilidade.

> **Leitura responsável:** a IVPD é experimental. Não constitui ranking, não mede prevalência real, não identifica pessoas e não realiza decisões automatizadas.

## Entregas da versão 5.1

- página inicial com painel nacional e métricas verificáveis;
- consulta por UF com indicadores e componentes normalizados;
- cartograma interativo e acessível das 27 UFs;
- comparador de até três UFs;
- exportação de recortes e comparações em CSV;
- seção de dados abertos com pesquisa e filtros;
- CSV compatível com Excel brasileiro e CSV internacional;
- JSON e API estática com cinco endpoints;
- metodologia do IVPD documentada;
- governança, salvaguardas, limitações e dicionário de dados;
- controles persistentes de alto contraste, ampliação, sublinhado de links e redução de movimento;
- layout responsivo para desktop, tablet e celular;
- testes Python, validação estática e auditoria funcional por navegador;
- publicação automatizada pelo GitHub Actions.

## Acessos

- Portal: https://anacarvalheiro-ai.github.io/protege-dados-cgu-2026/
- Repositório: https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026
- API: https://anacarvalheiro-ai.github.io/protege-dados-cgu-2026/api/v1/index.json
- Documentação: [docs/](docs/)

## Resultados atuais

| Evidência | Resultado |
|---|---:|
| Unidades federativas | 27 |
| Grupos de fontes oficiais | 3 |
| Escolas analisadas | 181.065 |
| Matrículas consideradas | 47.088.922 |
| Escolas com internet | 166.771 |
| Escolas com banda larga | 145.195 |
| Denúncias no recorte de 2025 | 294.592 |

## Estrutura principal

```text
web/                     Portal publicado no GitHub Pages
web/data/                JSON territorial
web/downloads/           CSVs para reúso
web/api/v1/              Endpoints estáticos
web/assets/              CSS, JavaScript e identidade técnica
scripts/                 Validadores e auditoria funcional
tests/                   Testes unitários Python
evidence/                Relatórios, hashes e capturas de tela
```

## Validação local

```bash
python -m pip install -e .
python scripts/validate_release.py
python scripts/validate_portal.py
python -m pytest -q
node --check web/assets/site.js
node --check web/assets/app.js
```

Para a auditoria funcional com navegador Chromium:

```bash
python scripts/browser_audit.py
```

## Atualização assistida no Windows

Após extrair o pacote, execute:

```text
ATUALIZAR_PROTEGE_DADOS_5_1.bat
```

O atualizador cria backup, copia os arquivos, executa as validações e oferece a opção de preparar o commit no Git. Consulte `INSTRUCOES_ATUALIZACAO_5_1.txt`.

## Publicação

1. mantenha o projeto na raiz do repositório `protege-dados-cgu-2026`;
2. confirme que **Settings → Pages → Source** está em **GitHub Actions**;
3. envie o commit para a branch `main`;
4. acompanhe o workflow **Publicar Protege.Dados 5.1**;
5. somente conclua a submissão após os jobs de validação e deploy ficarem verdes.

## Autoria

**Ana Maria Carvalheiro**  
Pretos Na Era Digital Ltda.  
Brasília/DF — 2026
