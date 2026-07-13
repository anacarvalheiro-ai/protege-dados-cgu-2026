# Relatório de Auditoria Técnica — Protege.Dados 5.1

**Projeto:** Protege.Dados — Ecossistema Nacional de Proteção Digital Infantojuvenil  
**Versão preservada:** 5.1.0  
**Responsável:** Ana Maria Carvalheiro / Pretos Na Era Digital Ltda.  
**Data da auditoria:** 13 de julho de 2026

## Resultado executivo

A versão 5.1 foi revisada, corrigida e submetida a validações automatizadas de estrutura, dados, API, JavaScript, acessibilidade básica, arquivos para GitHub Pages e integridade do pacote.

- Auditoria ampliada: **337 verificações aprovadas e 0 falhas**.
- Validador de release: **aprovado**.
- Validador do portal: **7 páginas, 27 UFs e links locais íntegros**.
- Testes unitários: **3 aprovados**.
- Sintaxe JavaScript: **aprovada pelo Node.js**.
- JSON principal e endpoints: **válidos**.
- CSVs: **27 UFs, sem ausência territorial**.
- Versão visível e metadados: **padronizados como 5.1 / 5.1.0**.

## Correções realizadas

1. Padronização dos rótulos de versão, removendo referências ativas inconsistentes a 4.1 e 5.0.
2. Atualização dos endpoints `index.json` e `indicators.json` para a versão 5.1.0.
3. Correção do título visual do cabeçalho para Protege.Dados 5.1.
4. Inclusão de `aria-label` na navegação principal.
5. Inclusão de regiões `role="status"` e `aria-live="polite"` nas mensagens dinâmicas.
6. Inclusão explícita de `type="button"` nos controles do painel.
7. Inclusão de página `404.html` para GitHub Pages.
8. Inclusão de `robots.txt` e `site.webmanifest`.
9. Inclusão de metadado de cor do tema e manifesto em todas as páginas.
10. Inclusão de auditoria reproduzível em `scripts/audit_complete.py`.
11. Geração de manifesto SHA-256 dos arquivos da pasta web.

## Escopo validado

Foram auditadas as páginas:

- Início;
- Painel e comparador;
- Dados e API;
- Metodologia;
- Governança;
- Acessibilidade;
- Página de erro 404.

Também foram verificados:

- seleção de UF;
- contrato dos controles de comparação de até três UFs;
- funções de geração de CSV;
- tabela das 27 UFs;
- arquivos CSV para Excel e padrão internacional;
- API estática;
- consistência entre JSON principal e API de territórios;
- documentos essenciais de licença, segurança, contribuição e publicação;
- caminhos relativos adequados ao GitHub Pages.

## Comandos executados

```bash
python scripts/audit_complete.py
python scripts/validate_release.py
python scripts/validate_portal.py
pytest -q
node --check web/assets/app.js
```

## Evidências

- `evidence/auditoria_completa_5_1.json`
- `evidence/audit_web_sha256.json`
- `evidence/testes_tecnicos.json`
- `evidence/manifesto_derivados_sha256.json`

## Limitação registrada

O ambiente de auditoria bloqueou a abertura do navegador Chromium por política administrativa, tanto em endereço local quanto por arquivo. Por isso, não foi possível executar Lighthouse ou um ensaio visual automatizado real com navegador nesta sessão. A lógica, os dados, os controles, a estrutura DOM esperada, os recursos locais, a sintaxe JavaScript e os contratos funcionais foram validados por testes estáticos e automatizados. Após publicar no GitHub Pages, recomenda-se executar Lighthouse no endereço público como verificação final de ambiente.

## Conclusão

O pacote está tecnicamente preparado para publicação no GitHub Pages como **Protege.Dados 5.1**, com validações reproduzíveis e evidências incluídas. A publicação final ainda deve ser conferida no endereço público para confirmar comportamento específico da infraestrutura do GitHub Pages e resultados do Lighthouse.
