# Instalação local

Requisitos:

- Python 3.12;
- Git;
- PowerShell ou terminal compatível.

Procedimento:

`powershell
git clone https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026.git
cd protege-dados-cgu-2026
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pytest -q
`
"@

  "docs\release\RELEASE-5.1.0.md" = @"
# Protege.Dados 5.1.0 LTS

## Escopo

Versão estável consolidada para apresentação institucional, reúso de dados, demonstrações e submissões.

## Destaques

- README institucional;
- documentação organizada;
- metodologia e governança consolidadas;
- feedback multicanal;
- API estática;
- portal responsivo;
- testes automatizados;
- preparação para release oficial.

## Verificação antes da publicação

- [ ] GitHub Actions concluído;
- [ ] portal testado no computador e celular;
- [ ] downloads testados;
- [ ] seletor de UF validado;
- [ ] comparador validado;
- [ ] feedback testado;
- [ ] documentos abertos;
- [ ] changelog revisado.