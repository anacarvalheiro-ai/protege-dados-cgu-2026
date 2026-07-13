# Protege.Dados 5.1 — Ecossistema Nacional de Proteção Digital Infantojuvenil

[![Portal](https://img.shields.io/badge/portal-GitHub%20Pages-0b73b9)](https://anacarvalheiro-ai.github.io/protege-dados-cgu-2026/)
[![Deploy](https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026/actions/workflows/deploy.yml/badge.svg)](https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026/actions/workflows/deploy.yml)
[![Release](https://img.shields.io/badge/release-5.1-d4a72c)](CHANGELOG.md)
[![Licença](https://img.shields.io/badge/c%C3%B3digo-MIT-06365f)](LICENSE)
[![Dados](https://img.shields.io/badge/dados-CSV%20%7C%20JSON-0873ba)](data/processed/ivpd_uf_v1.csv)

## Release candidata ao 2º Concurso de Reúso de Dados Abertos da CGU

O **Protege.Dados 5.1** integra dados oficiais de população, educação, conectividade e denúncias administrativas e disponibiliza resultados agregados para as 27 unidades federativas.

A release inclui:

- painel nacional;
- consulta por UF;
- comparador de até três UFs;
- CSV completo e recortes por UF;
- CSV compatível com Excel brasileiro;
- JSON;
- API estática;
- catálogo de indicadores;
- catálogo de fontes;
- endpoint de qualidade;
- metodologia, governança, limitações e dicionário;
- código aberto;
- testes de aceite;
- publicação automatizada;
- QR Codes do portal e do repositório.

> **Leitura responsável:** a IVPD é experimental. Não constitui ranking, não mede prevalência real, não identifica pessoas e não realiza decisões automatizadas.

## Acessos

- Portal: https://anacarvalheiro-ai.github.io/protege-dados-cgu-2026/
- Repositório: https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026
- API: https://anacarvalheiro-ai.github.io/protege-dados-cgu-2026/api/v1/index.json
- Documentação: [docs/](docs/)
- Dossiê e anexos: [docs/submissao-cgu-2026/](docs/submissao-cgu-2026/)

## Resultados atuais

| Evidência | Resultado |
|---|---:|
| UFs | 27 |
| Grupos de fontes oficiais | 3 |
| Escolas analisadas | 181.065 |
| Matrículas consideradas | 47.088.922 |
| Escolas com internet | 166.771 |
| Escolas com banda larga | 145.195 |
| Denúncias no recorte de 2025 | 294.592 |

## API estática

- `web/api/v1/index.json`
- `web/api/v1/territories.json`
- `web/api/v1/indicators.json`
- `web/api/v1/sources.json`
- `web/api/v1/quality.json`

## Publicação

Este pacote foi preparado para upload integral na raiz do repositório `protege-dados-cgu-2026`.

Após o upload:

1. abra **Settings → Pages**;
2. em **Source**, selecione **GitHub Actions**;
3. abra **Actions**;
4. execute ou reexecute `Publicar Protege.Dados 5.1`;
5. aguarde os jobs `validate` e `deploy` ficarem verdes.

O workflow também tenta habilitar o Pages automaticamente com `enablement: true`.

## Validação local

```bash
python scripts/validate_release.py
```

Resultado esperado:

```text
VALIDAÇÃO APROVADA — PROTEGE.DADOS 5.1
```

## QR Codes

- `web/assets/qr_portal.png`
- `web/assets/qr_repositorio.png`
- versões SVG equivalentes.

Os QR Codes usam correção de erros alta e apontam para os acessos oficiais.

## Autoria

**Ana Maria Carvalheiro**  
Pretos Na Era Digital Ltda.  
Brasília/DF — 2026
