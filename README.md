# Protege.Dados — Observatório de Proteção Digital Infantojuvenil

[![Portal público](https://img.shields.io/badge/portal-online-brightgreen)](https://anacarvalheiro-ai.github.io/protege-dados-cgu-2026/)
[![GitHub Pages](https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026/actions/workflows/pages.yml/badge.svg)](https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026/actions/workflows/pages.yml)
[![Testes](https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026/actions/workflows/tests.yml/badge.svg)](https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026/actions/workflows/tests.yml)
[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-blue)](LICENSE)
[![IVPD](https://img.shields.io/badge/IVPD-v1.1-C79A28)](docs/METODOLOGIA.md)

## Candidatura ao 2º Concurso de Reúso de Dados Abertos da CGU

O **Protege.Dados** é uma iniciativa de reúso responsável de dados abertos voltada à produção de indicadores territoriais relacionados à proteção digital de crianças e adolescentes.

O projeto integra dados oficiais do IBGE, do Censo Escolar/Inep e do Disque 100/Observatório Nacional dos Direitos Humanos, harmoniza códigos territoriais e disponibiliza resultados agregados para as 27 unidades federativas.

> **Leitura responsável:** a IVPD é experimental. Não constitui ranking, não mede prevalência, não identifica pessoas e não realiza previsão individual.

## Acesso

- **Portal:** https://anacarvalheiro-ai.github.io/protege-dados-cgu-2026/
- **Repositório:** https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026
- **Documentação:** [docs/](docs/)
- **Documentos da candidatura:** [docs/submissao-cgu-2026/](docs/submissao-cgu-2026/)
- **Evidências:** [evidence/](evidence/)

## Resultados do MVP

| Evidência | Resultado |
|---|---:|
| Unidades federativas | 27 |
| Grupos de fontes oficiais | 3 |
| Escolas analisadas | 181.065 |
| Matrículas consideradas | 47.088.922 |
| Escolas com internet | 166.771 |
| Escolas com banda larga | 145.195 |
| Denúncias no recorte de 2025 | 294.592 |
| Verificações técnicas | 7 de 7 |

## Recursos

- portal público funcional;
- seletor por UF;
- indicadores territoriais;
- download Excel brasileiro;
- download CSV internacional;
- base completa em CSV e JSON;
- metodologia aberta;
- dicionário de dados;
- evidências técnicas;
- QR Code para o portal e para o repositório;
- GitHub Pages;
- GitHub Actions;
- testes automatizados;
- versionamento Git.

## QR Codes

- `web/assets/qr_portal.png`
- `web/assets/qr_repositorio.png`
- versões SVG correspondentes.

Os QR Codes foram gerados para:

- Portal: https://anacarvalheiro-ai.github.io/protege-dados-cgu-2026/
- Repositório: https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026

## Fontes oficiais

1. IBGE — estimativas municipais de população.
2. Inep — Microdados do Censo Escolar 2024.
3. MDHC/ONDH — dados públicos do Disque 100.

## IVPD experimental

| Componente | Peso |
|---|---:|
| Taxa de denúncias por 100 mil habitantes | 50% |
| Déficit de internet escolar | 25% |
| Déficit de banda larga escolar | 25% |

## Estrutura

```text
protege-dados-cgu-2026/
├── .github/
├── config/
├── data/processed/
├── docs/
├── evidence/
├── src/
├── tests/
├── web/
│   ├── assets/
│   │   ├── app.js
│   │   ├── style.css
│   │   ├── qr_portal.png
│   │   └── qr_repositorio.png
│   ├── data/
│   └── index.html
├── README.md
├── LICENSE
└── pyproject.toml
```

## Publicação

1. Crie um repositório público chamado `protege-dados-cgu-2026`.
2. Envie todo o conteúdo deste pacote para a raiz do repositório.
3. Abra **Settings → Pages**.
4. Em **Source**, selecione **GitHub Actions**.
5. Abra a aba **Actions** e aguarde os workflows ficarem verdes.
6. Acesse: https://anacarvalheiro-ai.github.io/protege-dados-cgu-2026/

## Testes

```bash
python -m venv .venv
pip install -e .
pytest -q
```

## Licenças

- Código: [MIT](LICENSE)
- Dados derivados: [DATA_LICENSE.md](DATA_LICENSE.md)

## Autoria

**Ana Maria Carvalheiro**  
Pretos Na Era Digital Ltda.  
Brasília — DF  
E-mail: anacarvalheiro@gmail.com
