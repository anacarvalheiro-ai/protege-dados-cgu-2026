# COMEÇAR AQUI — Novo Projeto Protege.Dados

## Nome recomendado do repositório

`protege-dados-cgu-2026`

## Passo a passo mais simples

1. No GitHub, clique em **New repository**.
2. Use o nome `protege-dados-cgu-2026`.
3. Marque **Public**.
4. Não adicione README, licença ou `.gitignore`, pois eles já estão no pacote.
5. Crie o repositório.
6. Clique em **Add file → Upload files**.
7. Extraia este ZIP no computador.
8. Selecione todos os arquivos e pastas de dentro da pasta extraída.
9. Arraste para a área de upload.
10. Use a mensagem de commit:
   `publicacao-inicial-protege-dados-cgu-2026`
11. Confirme o commit.
12. Vá para **Settings → Pages**.
13. Em **Source**, selecione **GitHub Actions**.
14. Vá para **Actions** e aguarde os workflows ficarem verdes.
15. Abra o portal:
    https://anacarvalheiro-ai.github.io/protege-dados-cgu-2026/

## QR Code

O pacote já contém QR Codes para o endereço acima:

- `web/assets/qr_portal.png`
- `web/assets/qr_repositorio.png`

Se você escolher outro nome de repositório, será necessário gerar novos QR Codes e atualizar os links no README e no `web/index.html`.

## Estrutura correta da web

```text
web/
├── index.html
├── assets/
│   ├── app.js
│   ├── style.css
│   ├── qr_portal.png
│   └── qr_repositorio.png
└── data/
    └── ivpd_uf_v1.json
```

Não crie `web/app.js` nem `web/style.css` fora da pasta `assets`.
