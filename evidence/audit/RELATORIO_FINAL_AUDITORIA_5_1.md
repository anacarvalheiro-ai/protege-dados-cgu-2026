# Relatório final de auditoria — Protege.Dados 5.1

**Data:** 13 de julho de 2026  
**Escopo:** interface, dados, funcionalidades, acessibilidade, responsividade, atualização e publicação no GitHub Pages.

## Resultado executivo

A versão **Protege.Dados 5.1** foi aprovada nas verificações executadas neste pacote.

| Área | Resultado |
|---|---:|
| Validação de dados e release | 162/162 |
| Validação estrutural do portal | 173/173 |
| Testes unitários Python | 3/3 |
| Teste do atualizador executável | 5/5 |
| Sintaxe JavaScript | 2/2 |
| Auditoria funcional Chromium | 67/67 |
| **Total consolidado** | **412/412** |

## Funcionalidades verificadas

- carregamento das 27 unidades federativas;
- totais nacionais de escolas, matrículas e denúncias;
- mudança de UF e atualização dos indicadores;
- cartograma com 27 controles territoriais;
- comparação de três UFs;
- exportação da comparação em CSV;
- exportação de recorte por UF em formato compatível com Excel;
- tabela completa com 27 UFs;
- pesquisa e filtros da seção de dados abertos;
- acesso aos cinco endpoints da API;
- metodologia e fórmula publicadas;
- acordeões de governança;
- alto contraste, ampliação de texto, sublinhado de links e redução de movimento;
- persistência das preferências de acessibilidade;
- menu móvel;
- ausência de overflow horizontal nas seis telas principais;
- ausência de erros de console e de requisições locais com falha;
- atualização controlada em pasta de teste, com backup, remoção de arquivo obsoleto e revalidação.

## Design e experiência

- cabeçalho e rodapé em azul institucional;
- ausência de imagens decorativas no cabeçalho e no rodapé;
- identidade consistente nas sete páginas;
- cartões, filtros, tabelas e hierarquia tipográfica harmonizados;
- layout responsivo para desktop, tablet e celular;
- foco de teclado visível e HTML semântico;
- recursos locais, sem bibliotecas externas no portal publicado.

## Evidências

- `browser_audit_5_1.json`;
- `RELATORIO_AUDITORIA_NAVEGADOR_5_1.md`;
- `full_audit_5_1.json`;
- capturas em `evidence/screenshots/`;
- logs gerados pelo atualizador em cada execução.

## Conclusão

O pacote está tecnicamente preparado para atualização do repositório e submissão ao GitHub Pages. A publicação efetiva depende apenas das credenciais Git da responsável e da conclusão bem-sucedida dos workflows no repositório remoto.
