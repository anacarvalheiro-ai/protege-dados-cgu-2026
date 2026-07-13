param([string]$RepoPath = "")
$ErrorActionPreference = "Stop"
$Script = Join-Path $PSScriptRoot "atualizar_protege_dados_5_1.py"
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python não encontrado. Instale Python 3.11 ou superior."
}
$Arguments = @($Script)
if (-not [string]::IsNullOrWhiteSpace($RepoPath)) {
    $Arguments += @("--target", $RepoPath)
}
& python @Arguments
exit $LASTEXITCODE
