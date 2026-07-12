# Publicação no GitHub

## Método recomendado: GitHub Desktop

1. Crie no GitHub um repositório público vazio chamado `protege-dados`.
2. Não marque README, licença ou `.gitignore`, pois já estão no pacote.
3. Abra o GitHub Desktop e clone o repositório vazio.
4. Copie **o conteúdo** desta pasta para a pasta clonada.
5. No GitHub Desktop, escreva `Publicação inicial do Protege.Dados`.
6. Clique em **Commit to main** e depois em **Push origin**.
7. No repositório, abra **Settings → Pages**.
8. Em **Build and deployment**, selecione **GitHub Actions**.
9. Abra **Actions** e acompanhe `Publicar portal no GitHub Pages`.
10. A URL aparecerá no workflow e em Settings → Pages.

Formato esperado:
`https://SEU-USUARIO.github.io/protege-dados/`

## Método alternativo: terminal

```bash
git init
git branch -M main
git add .
git commit -m "Publicação inicial do Protege.Dados"
git remote add origin https://github.com/SEU-USUARIO/protege-dados.git
git push -u origin main
```
