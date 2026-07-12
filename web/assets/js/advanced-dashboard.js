(() => {
  "use strict";
  const $ = id => document.getElementById(id);
  const UF_NAMES = {AC:"Acre",AL:"Alagoas",AP:"Amapá",AM:"Amazonas",BA:"Bahia",CE:"Ceará",DF:"Distrito Federal",ES:"Espírito Santo",GO:"Goiás",MA:"Maranhão",MT:"Mato Grosso",MS:"Mato Grosso do Sul",MG:"Minas Gerais",PA:"Pará",PB:"Paraíba",PR:"Paraná",PE:"Pernambuco",PI:"Piauí",RJ:"Rio de Janeiro",RN:"Rio Grande do Norte",RS:"Rio Grande do Sul",RO:"Rondônia",RR:"Roraima",SC:"Santa Catarina",SP:"São Paulo",SE:"Sergipe",TO:"Tocantins"};
  let rows=[];
  const num=v=>{if(typeof v==='number')return v;if(v==null||v==='')return NaN;const s=String(v).trim();return Number(s.includes(',')?s.replace(/\./g,'').replace(',','.'):s)};
  const fmt=(v,d=1)=>Number.isFinite(num(v))?new Intl.NumberFormat('pt-BR',{minimumFractionDigits:d,maximumFractionDigits:d}).format(num(v)):'—';
  const val=(r,key)=>num(r[key]);
  function derive(r){const pop=val(r,'populacao'),den=val(r,'denuncias'),esc=val(r,'escolas'),net=val(r,'escolas_internet');return {...r,uf:String(r.uf||'').toUpperCase(),taxa:Number.isFinite(val(r,'taxa_denuncias_100mil'))?val(r,'taxa_denuncias_100mil'):den/pop*100000,internet:Number.isFinite(val(r,'perc_escolas_internet'))?val(r,'perc_escolas_internet'):net/esc*100,vuln:val(r,'eixo_vulnerabilidade')}}
  function card(label,value,sub){return `<article class="metric"><span>${label}</span><b>${value}</b><small>${sub}</small></article>`}
  function renderNational(){
    const n=rows.length, avg=k=>rows.reduce((a,r)=>a+(Number.isFinite(r[k])?r[k]:0),0)/n;
    $('national-metrics').innerHTML=card('Territórios cobertos',n,'Unidades federativas')+card('Vulnerabilidade média',fmt(avg('vuln')),'Leitura experimental')+card('Taxa média de denúncias',fmt(avg('taxa')),'Média simples entre UFs')+card('Escolas com internet',fmt(avg('internet'))+'%','Média simples entre UFs');
    const sorted=[...rows].filter(r=>Number.isFinite(r.taxa)).sort((a,b)=>b.taxa-a.taxa).slice(0,8);
    const max=Math.max(...sorted.map(r=>r.taxa));
    $('national-bars').innerHTML=sorted.map(r=>`<div class="bar-row"><div class="bar-head"><span>${UF_NAMES[r.uf]} — ${r.uf}</span><strong>${fmt(r.taxa)}</strong></div><div class="bar-track"><div class="bar-fill" style="width:${(r.taxa/max)*100}%"></div></div></div>`).join('');
  }
  function fillSelectors(){document.querySelectorAll('.compare-select').forEach((s,i)=>{s.innerHTML=rows.map(r=>`<option value="${r.uf}">${UF_NAMES[r.uf]} — ${r.uf}</option>`).join('');s.value=['DF','SP','BA'][i]||rows[i].uf});}
  function renderCompare(){const chosen=[...document.querySelectorAll('.compare-select')].map(s=>rows.find(r=>r.uf===s.value)).filter(Boolean);$('compare-grid').innerHTML=chosen.map(r=>`<article class="card"><p class="kicker">${r.uf}</p><h3>${UF_NAMES[r.uf]}</h3><dl class="data-list"><div><dt>Vulnerabilidade</dt><dd>${fmt(r.vuln)}</dd></div><div><dt>Taxa de denúncias</dt><dd>${fmt(r.taxa)}</dd></div><div><dt>Escolas com internet</dt><dd>${fmt(r.internet)}%</dd></div></dl></article>`).join('')}
  function printReport(){window.print()}
  async function init(){const status=$('advanced-status');try{const res=await fetch('../data/ivpd_uf_v1.json',{cache:'no-store'});if(!res.ok)throw new Error(`HTTP ${res.status}`);rows=(await res.json()).map(derive).filter(r=>UF_NAMES[r.uf]);renderNational();fillSelectors();renderCompare();document.querySelectorAll('.compare-select').forEach(s=>s.addEventListener('change',renderCompare));const p=$('print-report');if(p)p.addEventListener('click',printReport);status.textContent=`Base carregada: ${rows.length} UFs.`}catch(e){console.error(e);status.textContent='Não foi possível carregar a base territorial.';status.dataset.error='true'}}
  init();
})();