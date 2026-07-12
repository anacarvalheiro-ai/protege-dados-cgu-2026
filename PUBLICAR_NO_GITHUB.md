# Publicar o Protege.Dados 4.1 no GitHub

Repositório de destino:
`https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026`

## Método recomendado — GitHub Desktop

1. Instale e abra o GitHub Desktop.
2. Entre na conta `anacarvalheiro-ai`.
3. Use **File > Clone repository** e escolha `protege-dados-cgu-2026`.
4. Abra a pasta clonada no computador.
5. Copie para essa pasta todo o conteúdo deste pacote, incluindo a pasta oculta `.github`.
6. Confirme a substituição dos arquivos antigos.
7. No GitHub Desktop, escreva o resumo: `Publica release 4.1 do Protege.Dados`.
8. Clique em **Commit to main** e depois em **Push origin**.
9. No GitHub, abra **Settings > Pages** e escolha **GitHub Actions** como fonte.
10. Abra **Actions** e acompanhe o workflow **Publicar Protege.Dados 4.1**.

Portal esperado:
`https://anacarvalheiro-ai.github.io/protege-dados-cgu-2026/`

## Verificação após o deploy

- O workflow deve mostrar os jobs `validate` e `deploy` em verde.
- O portal deve abrir sem erro.
- O seletor de UF deve carregar 27 UFs.
- Os botões de download CSV devem funcionar.
- O comparador deve exibir até três UFs.
- Os endpoints em `/api/v1/` devem abrir como JSON.

## Comandos alternativos com Git

```bash
git clone https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026.git
cd protege-dados-cgu-2026
# copie o conteúdo deste pacote para esta pasta
git add -A
git commit -m "Publica release 4.1 do Protege.Dados"
git push origin main
```
