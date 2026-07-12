# Arquitetura 4.0

## Camadas

1. **Fontes** — catálogos oficiais e licenças.
2. **Conectores** — aquisição controlada, sem credenciais no front-end.
3. **Processamento** — harmonização territorial, qualidade e derivação.
4. **Produtos** — CSV, JSON, API estática, dashboards e relatórios.
5. **Governança** — limitações, privacidade, versões, manifestos e supervisão humana.

## Critérios para nova fonte

- legitimidade e origem oficial;
- licença compatível;
- nível territorial adequado;
- periodicidade e estabilidade;
- ausência de dados pessoais no produto público;
- compatibilidade temporal e conceitual;
- avaliação de risco de estigmatização;
- documentação e revisão humana.

## Automação

O workflow mensal não baixa fontes ainda não implementadas. Ele valida o catálogo, reconstrói a API e registra mudanças dos artefatos. Cada conector futuro deve passar por revisão e testes antes de ser habilitado.
