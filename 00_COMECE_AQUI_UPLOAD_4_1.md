# COMEÇAR AQUI — Upload da Release 5.1

## Você já criou o repositório correto

`https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026`

## Substituição integral, sem editar arquivo por arquivo

1. Baixe e extraia o ZIP desta release.
2. No repositório, clique em **Add file → Upload files**.
3. Arraste **todos os arquivos e pastas de dentro da pasta extraída**.
4. O GitHub substituirá os arquivos com o mesmo caminho e adicionará os novos.
5. Use a mensagem:
   `publicar-release-candidata-protege-dados-4-1`
6. Confirme na branch `main`.
7. Abra **Settings → Pages**.
8. Em **Source**, selecione **GitHub Actions**.
9. Abra **Actions → Publicar Protege.Dados 5.1**.
10. Caso necessário, clique em **Run workflow** ou **Re-run all jobs**.
11. Aguarde `validate` e `deploy` ficarem verdes.
12. Abra o portal:
    `https://anacarvalheiro-ai.github.io/protege-dados-cgu-2026/`
13. Pressione `Ctrl + F5`.
14. Execute o checklist `docs/ACEITE_RELEASE_4_1.md`.

## Importante

Não envie o ZIP fechado ao GitHub. Extraia e envie o conteúdo.

Não crie arquivos duplicados fora de `web/assets`.

Estrutura correta:

```text
web/
├── index.html
├── assets/
├── data/
└── api/v1/
```
