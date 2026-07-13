# Relatório de correção integral — Protege.Dados 5.0

## Problemas eliminados
- JSON incompatível com navegadores por uso de `NaN`.
- Textos com caracteres corrompidos.
- JavaScript interrompido por versões antigas e inconsistentes.
- Seletores de UF vazios.
- Botões de comparação e exportação sem resposta.
- Endpoints e downloads ausentes.
- Workflows duplicados para GitHub Pages.
- Página única excessivamente longa e difícil de manter.

## Nova estrutura
- `index.html`: apresentação e resultados nacionais.
- `painel.html`: seleção das 27 UFs, indicadores, comparador e exportações.
- `dados.html`: JSON, CSV e endpoints da API.
- `metodologia.html`: composição, fontes e limitações.
- `governanca.html`: privacidade, transparência e integridade.
- `acessibilidade.html`: recursos de acesso inclusivo.

## Validações executadas
- JSON estrito, sem `NaN`.
- Exatamente 27 UFs, sem duplicidades.
- Links e recursos locais verificados.
- Codificação UTF-8 em todas as páginas.
- Sintaxe JavaScript validada pelo Node.js.
- Testes Python aprovados.
