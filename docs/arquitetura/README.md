# Arquitetura

## Componentes

- src/protege_dados/readers.py: leitura de fontes;
- src/protege_dados/processors.py: limpeza e transformação;
- src/protege_dados/indicators.py: indicadores e IVPD;
- src/protege_dados/pipeline.py: orquestração;
- src/protege_dados/quality.py: verificações de qualidade;
- web/: portal público e API estática;
- .github/workflows/: integração e publicação contínuas.

## Princípios

- reprodutibilidade;
- separação entre dados, processamento e apresentação;
- formatos abertos;
- validação automática;
- privacidade por desenho.