# Protege.Dados 4.0 — Ecossistema Nacional

## Entrega

Esta versão transforma a Fundação 2.0 em um ecossistema com:

- Painel Nacional;
- comparador de até três UFs;
- relatório territorial imprimível em PDF;
- API pública estática;
- catálogo de fontes;
- painel de qualidade e transparência;
- arquitetura de conectores;
- pipeline reproduzível;
- manifesto SHA-256;
- testes automatizados;
- atualização mensal programada;
- módulos de educação, rede de proteção, pesquisa e governança;
- diferenciação explícita entre dados publicados, planejados e em desenvolvimento.

## Limite de honestidade

A versão 4.0 não cria números para capacidade de proteção nem afirma integrações que ainda dependem de fonte oficial validada. Ela entrega a arquitetura, o catálogo e os conectores-base para incorporar novas bases com segurança.

## Instalação

1. Baixe o ZIP para `Downloads`.
2. Abra o PowerShell.
3. Execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

4. Execute o script extraído:

```powershell
& "$HOME\Downloads\Protege_Dados_4_0_Ecossistema_Nacional\scripts\Atualizar_Protege_Dados_4_0.ps1"
```

5. Quando solicitado, digite apenas `PUBLICAR`.

## Atualização rotineira

- conteúdo institucional: `web/config/portal.json`;
- menu: `web/config/menu.json`;
- fontes: `web/config/fontes.json`;
- indicadores: `web/config/indicadores.json`;
- qualidade: `web/config/qualidade.json`;
- dados territoriais: `web/data/ivpd_uf_v1.json`.

## Próximas integrações condicionadas à validação

- capacidade da assistência social;
- cobertura de Conselhos Tutelares;
- séries históricas;
- granularidade municipal;
- indicadores amostrais de acesso e práticas digitais.
