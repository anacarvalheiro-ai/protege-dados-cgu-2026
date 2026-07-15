# Protege.Dados

## Observatório de Proteção Digital Infantojuvenil

[![Versão](https://img.shields.io/badge/vers%C3%A3o-5.1.0-0E73B8)](#)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB)](#)
[![Dados abertos](https://img.shields.io/badge/dados-abertos-2E7D5A)](#)
[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-222222)](#)
[![Licença](https://img.shields.io/badge/licen%C3%A7a-consulte%20o%20reposit%C3%B3rio-D6A21E)](#)

O **Protege.Dados** é uma plataforma pública de inteligência territorial voltada à proteção digital de crianças e adolescentes. A iniciativa integra dados abertos oficiais, produz indicadores por Unidade da Federação e disponibiliza painel, comparador, arquivos abertos, API estática, metodologia e documentação de governança.

**Responsável técnica:** Ana Maria Carvalheiro  
**Organização:** Pretos Na Era Digital Ltda.  
**Versão estável:** 5.1.0 LTS

## Acesso rápido

- Portal público: https://anacarvalheiro-ai.github.io/protege-dados-cgu-2026/
- Dados e API: web/api/v1/
- Metodologia: docs/metodologia/
- Arquitetura: docs/arquitetura/
- Governança: docs/governanca/
- Guia do usuário: docs/usuario/
- Guia do desenvolvedor: docs/desenvolvedor/
- Registro de mudanças: CHANGELOG.md

## O que a plataforma oferece

- consulta territorial para as 27 Unidades da Federação;
- indicadores de denúncias e conectividade escolar;
- IVPD experimental em escala de 0 a 100;
- comparação contextual entre UFs;
- exportação em CSV e JSON;
- API estática pública;
- metodologia auditável e reproduzível;
- salvaguardas de privacidade e interpretação responsável;
- canal de feedback por GitHub Issue, e-mail e WhatsApp.

## Interpretação responsável do IVPD

O IVPD é um indicador sintético experimental de vulnerabilidade relativa. Ele:

- não representa percentual de crianças em risco;
- não mede pessoas individualmente;
- não estima prevalência real de violência;
- não constitui ranking absoluto;
- não realiza decisões automatizadas;
- não substitui análise qualitativa ou diagnóstico local.

## Fontes e processamento

A solução utiliza fontes públicas oficiais e processamento programado em Python. As etapas principais são:

1. ingestão e registro das bases;
2. padronização territorial;
3. limpeza e validação;
4. construção dos indicadores;
5. normalização;
6. cálculo do IVPD;
7. testes automáticos;
8. publicação em formatos abertos.

## Arquitetura

`	ext
fontes oficiais
      |
      v
leitura e validação
      |
      v
processamento em Python
      |
      v
indicadores por UF
      |
      +--> CSV
      +--> JSON
      +--> API estática
      +--> portal público
`

## Execução local

`powershell
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pytest -q
`

Consulte docs/desenvolvedor/instalacao.md antes de executar o pipeline completo.

## Documentação

| Documento | Finalidade |
|---|---|
| docs/metodologia/README.md | cálculo, pesos, normalização e limitações |
| docs/arquitetura/README.md | componentes e fluxo técnico |
| docs/governanca/README.md | versionamento, qualidade, privacidade e auditoria |
| docs/api/README.md | endpoints e formatos |
| docs/usuario/README.md | uso e interpretação do portal |
| docs/desenvolvedor/README.md | instalação, testes e manutenção |
| docs/release/RELEASE-5.1.0.md | notas da versão estável |

## Reúso e transparência

O projeto foi estruturado para facilitar auditoria, reprodução e reúso responsável. Antes de reutilizar os dados, consulte a metodologia, o dicionário de dados, as limitações e os termos de licenciamento presentes no repositório.

## Contato

Ana Maria Carvalheiro  
Pretos Na Era Digital Ltda.  
E-mail: anacarvalheiro@gmail.com