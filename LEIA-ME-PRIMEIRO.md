# Protege.Dados 2.0 — Fundação

Pacote de atualização modular e segura.

## Como publicar
1. Salve o ZIP em Downloads.
2. Extraia o ZIP.
3. Abra o PowerShell.
4. Execute `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.
5. Execute o script `scripts/Atualizar_Protege_Dados_2_0.ps1`.
6. Revise a lista de arquivos e digite `PUBLICAR`.

O script cria backup, preserva `web/data/ivpd_uf_v1.json`, valida JSON e só então publica.

## Atualizações futuras
- identidade: `web/config/portal.json`;
- menu: `web/config/menu.json`;
- indicadores: `web/config/indicadores.json`;
- fontes: `web/config/fontes.json`;
- públicos: `web/config/publicos.json`;
- histórico: `web/config/atualizacoes.json`.
