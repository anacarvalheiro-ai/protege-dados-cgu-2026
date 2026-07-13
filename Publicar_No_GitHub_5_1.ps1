$ErrorActionPreference = "Stop"
$Repo = (Resolve-Path $PSScriptRoot).Path
Set-Location $Repo

if (-not (Test-Path (Join-Path $Repo ".git"))) {
    throw "Esta pasta não é um repositório Git. Execute primeiro o atualizador apontando para o repositório correto."
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git não encontrado."
}

Write-Host "Validando o Protege.Dados 5.1 antes da publicação..." -ForegroundColor Cyan
python scripts\validate_release.py
if ($LASTEXITCODE -ne 0) { throw "Validação da release reprovada." }
python scripts\validate_portal.py
if ($LASTEXITCODE -ne 0) { throw "Validação do portal reprovada." }
python -m pytest -q
if ($LASTEXITCODE -ne 0) { throw "Testes Python reprovados." }
if (Get-Command node -ErrorAction SilentlyContinue) {
    node --check web\assets\site.js
    if ($LASTEXITCODE -ne 0) { throw "site.js inválido." }
    node --check web\assets\app.js
    if ($LASTEXITCODE -ne 0) { throw "app.js inválido." }
}

Write-Host ""
Write-Host "Alterações pendentes:" -ForegroundColor Cyan
git status --short
$Confirm = Read-Host "Digite PUBLICAR para criar o commit e enviar para origin/main"
if ($Confirm -cne "PUBLICAR") {
    Write-Host "Publicação cancelada sem alterar o GitHub." -ForegroundColor Yellow
    exit 0
}

git add --all
$Changes = git status --porcelain
if ($Changes) {
    git commit -m "Publica Protege.Dados 5.1 — interface, acessibilidade e auditoria"
    if ($LASTEXITCODE -ne 0) { throw "Falha ao criar commit." }
} else {
    Write-Host "Nenhuma alteração pendente para commit." -ForegroundColor Yellow
}
git push origin main
if ($LASTEXITCODE -ne 0) { throw "Falha ao enviar para o GitHub." }
Write-Host "Publicação enviada. Aguarde os jobs validate e deploy ficarem verdes." -ForegroundColor Green
Read-Host "Pressione ENTER para fechar"
