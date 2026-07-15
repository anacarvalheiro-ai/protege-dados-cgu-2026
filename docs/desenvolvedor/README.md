# Guia do desenvolvedor

## Preparação

`powershell
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
`

## Testes

`powershell
python -m pytest -q
`

## Publicação

A publicação é realizada por GitHub Actions. Não publique artefatos manualmente sem validar o pipeline.