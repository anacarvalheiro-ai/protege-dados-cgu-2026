$ErrorActionPreference = "Stop"
Write-Host "=== Protege.Dados 2.0 — Atualização segura ===" -ForegroundColor Cyan
$repo = Join-Path $HOME "protege-dados-cgu-2026"
$downloads = Join-Path $HOME "Downloads"
$package = Get-ChildItem $downloads -File | Where-Object { $_.Name -like "Protege_Dados_2_0_Fundacao*.zip" } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $package) { throw "Pacote Protege_Dados_2_0_Fundacao não encontrado em Downloads." }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "Git não está disponível." }
if (-not (Test-Path (Join-Path $repo ".git"))) { git clone "https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026.git" $repo }
Set-Location $repo
git pull origin main
$temp = Join-Path $env:TEMP "Protege_Dados_2_0_Fundacao"
if (Test-Path $temp) { Remove-Item $temp -Recurse -Force }
Expand-Archive $package.FullName $temp -Force
$dataFile = Join-Path $repo "web\data\ivpd_uf_v1.json"
if (-not (Test-Path $dataFile)) { throw "A base web\data\ivpd_uf_v1.json não foi encontrada. Nada foi publicado." }
$backup = Join-Path $HOME ("Protege_Dados_Backup_" + (Get-Date -Format "yyyyMMdd_HHmmss"))
New-Item -ItemType Directory -Path $backup -Force | Out-Null
Copy-Item (Join-Path $repo "web") (Join-Path $backup "web") -Recurse -Force
Copy-Item (Join-Path $temp "web\index.html") (Join-Path $repo "web\index.html") -Force
Copy-Item (Join-Path $temp "web\404.html") (Join-Path $repo "web\404.html") -Force
foreach ($folder in @("assets\css","assets\js","assets\icons","config","pages")) { $dest=Join-Path $repo ("web\"+$folder); New-Item -ItemType Directory -Path $dest -Force | Out-Null; Copy-Item (Join-Path $temp ("web\"+$folder+"\*")) $dest -Recurse -Force }
Copy-Item (Join-Path $temp ".github\workflows\main.yml") (Join-Path $repo ".github\workflows\main.yml") -Force
python -m json.tool ".\web\config\portal.json" | Out-Null
python -m json.tool ".\web\data\ivpd_uf_v1.json" | Out-Null
Write-Host "Backup criado em: $backup" -ForegroundColor Green
git status --short
$answer = Read-Host "Digite PUBLICAR para enviar ao GitHub"
if ($answer -cne "PUBLICAR") { Write-Host "Publicação cancelada." -ForegroundColor Yellow; exit 0 }
git add web .github/workflows/main.yml
git commit -m "Implantar Fundação Protege.Dados 2.0"
if ($LASTEXITCODE -eq 1) { Write-Host "Não há alterações novas."; exit 0 }
git push origin main
Write-Host "FUNDAÇÃO 2.0 ENVIADA COM SUCESSO." -ForegroundColor Green
