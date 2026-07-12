$ErrorActionPreference = "Stop"
Write-Host "=== Protege.Dados 4.0 FINAL — Submissão ===" -ForegroundColor Cyan
$repo=Join-Path $HOME "protege-dados-cgu-2026"
$downloads=Join-Path $HOME "Downloads"
$zip=Get-ChildItem $downloads -File | Where-Object {$_.Name -like "Protege_Dados_4_0_Final_Submissao*.zip"} | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if(-not $zip){throw "Pacote Protege_Dados_4_0_Final_Submissao.zip não encontrado em Downloads."}
if(-not (Get-Command git -ErrorAction SilentlyContinue)){throw "Git não está disponível."}
if(-not (Test-Path (Join-Path $repo ".git"))){git clone "https://github.com/anacarvalheiro-ai/protege-dados-cgu-2026.git" $repo}
Set-Location $repo
git pull origin main
if($LASTEXITCODE -ne 0){throw "Falha no git pull."}
$temp=Join-Path $env:TEMP "Protege_Dados_4_0_Final_Submissao"
if(Test-Path $temp){Remove-Item $temp -Recurse -Force}
Expand-Archive $zip.FullName $temp -Force
if(-not (Test-Path ".\web\data\ivpd_uf_v1.json")){throw "Base web\data\ivpd_uf_v1.json não encontrada. Interrompido para preservar os resultados atuais."}
$backup=Join-Path $HOME ("Protege_Dados_Backup_FINAL_"+(Get-Date -Format "yyyyMMdd_HHmmss"))
New-Item -ItemType Directory -Path $backup -Force | Out-Null
Copy-Item ".\web" (Join-Path $backup "web") -Recurse -Force
Write-Host "Backup criado: $backup" -ForegroundColor Green
Copy-Item (Join-Path $temp "*") $repo -Recurse -Force
Get-ChildItem ".\web\config\*.json" | ForEach-Object {Get-Content $_.FullName -Raw | ConvertFrom-Json | Out-Null}
Get-Content ".\web\data\ivpd_uf_v1.json" -Raw | ConvertFrom-Json | Out-Null
Write-Host "JSON validado com sucesso." -ForegroundColor Green
git status --short
$resposta=Read-Host "Digite apenas PUBLICAR para enviar a versão final"
if($resposta -cne "PUBLICAR"){Write-Host "Publicação cancelada." -ForegroundColor Yellow;exit 0}
git add web src tests docs/4.0 evidence/4.0 scripts .github/workflows requirements-dev.txt pyproject-4.0.toml LEIA-ME-4.0.md
git commit -m "Publicar release final Protege.Dados 4.0 para submissão"
if($LASTEXITCODE -eq 1){Write-Host "Nenhuma alteração nova para commit." -ForegroundColor Yellow;exit 0}
if($LASTEXITCODE -ne 0){throw "Falha no commit."}
git push origin main
if($LASTEXITCODE -ne 0){throw "Falha no push."}
Write-Host "VERSÃO FINAL ENVIADA. AGUARDE O GITHUB ACTIONS FICAR VERDE." -ForegroundColor Green
