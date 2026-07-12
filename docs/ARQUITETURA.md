# Arquitetura

O Protege.Dados separa aquisição, tratamento, validação, cálculo, publicação e apresentação.

```text
Fontes oficiais
      ↓
arquivos preservados + hashes
      ↓
limpeza e harmonização territorial
      ↓
tabelas agregadas por UF
      ↓
indicadores e IVPD experimental
      ↓
CSV/JSON públicos
      ↓
portal estático acessível
```

O repositório público não contém os grandes arquivos brutos. Ele publica código, metodologia, agregados, manifestos, testes e documentos comprobatórios.
