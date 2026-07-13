(() => {
  "use strict";
  const DATA_URL = "data/ivpd_uf_v1.json?v=5.2.0";
  const $ = (id) => document.getElementById(id);
  const expected = new Set(["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]);
  let rows = [], selected = null, comparisonRows = [];

  function numberValue(value) {
    if (typeof value === "number") return Number.isFinite(value) ? value : NaN;
    if (value === null || value === undefined || value === "") return NaN;
    const text = String(value).trim();
    const result = Number(text.includes(",") ? text.replace(/\./g,"").replace(",",".") : text);
    return Number.isFinite(result) ? result : NaN;
  }
  function formatNumber(value, digits=1) {
    const valueNumber = numberValue(value);
    return Number.isFinite(valueNumber)
      ? new Intl.NumberFormat("pt-BR",{minimumFractionDigits:digits,maximumFractionDigits:digits}).format(valueNumber)
      : "—";
  }
  const formatPercent = (value) => Number.isFinite(numberValue(value)) ? `${formatNumber(value,1)}%` : "—";
  function setNotice(text, error=false) {
    const notice = $("portal-status");
    if (!notice) return;
    notice.textContent = text;
    notice.className = error ? "notice error" : "notice";
  }
  function setMessage(text, error=false) {
    const message = $("download-message");
    if (!message) return;
    message.textContent = text;
    message.style.color = error ? "#a22929" : "#117443";
  }
  async function loadRows() {
    const response = await fetch(DATA_URL,{cache:"no-store",headers:{Accept:"application/json"}});
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    const list = Array.isArray(payload) ? payload : payload.territories;
    if (!Array.isArray(list)) throw new Error("Formato de dados inválido");
    const map = new Map();
    for (const item of list) {
      const uf = String(item.uf || "").trim().toUpperCase();
      if (expected.has(uf)) map.set(uf,{...item,uf});
    }
    const normalized = [...map.values()].sort((a,b)=>a.uf.localeCompare(b.uf,"pt-BR"));
    if (normalized.length !== 27) throw new Error(`A base contém ${normalized.length} UFs; eram esperadas 27`);
    return normalized;
  }
  function fillSelect(select, allowEmpty=false) {
    if (!select) return;
    select.replaceChildren();
    if (allowEmpty) select.add(new Option("Nenhuma",""));
    for (const row of rows) select.add(new Option(row.uf,row.uf));
  }
  function makeBar(label, value) {
    const raw = numberValue(value);
    const width = Number.isFinite(raw) ? Math.max(0,Math.min(100,raw)) : 0;
    const el = document.createElement("div");
    el.innerHTML = `<div class="bar-title"><strong>${label}</strong><span>${formatNumber(width)}</span></div><div class="bar"><i style="width:${width}%"></i></div>`;
    return el;
  }
  function renderUf(row) {
    if (!row) return;
    selected = row;
    $("vuln").textContent = formatNumber(row.eixo_vulnerabilidade);
    $("taxa").textContent = formatNumber(row.taxa_denuncias_100mil);
    $("internet").textContent = formatPercent(row.perc_escolas_internet);
    $("banda").textContent = formatPercent(row.perc_escolas_banda_larga);
    $("bars").replaceChildren(
      makeBar("Denúncias notificadas",row.n_taxa_denuncias),
      makeBar("Déficit de internet escolar",row.n_deficit_internet),
      makeBar("Déficit de banda larga escolar",row.n_deficit_banda_larga)
    );
  }
  function comparisonCard(row) {
    const card = document.createElement("article");
    card.className = "compare-card";
    card.innerHTML = `<h3>${row.uf}</h3>
      <div class="compare-row"><span>IVPD</span><b>${formatNumber(row.eixo_vulnerabilidade)}</b></div>
      <div class="compare-row"><span>Taxa de denúncias</span><b>${formatNumber(row.taxa_denuncias_100mil)}</b></div>
      <div class="compare-row"><span>Internet escolar</span><b>${formatPercent(row.perc_escolas_internet)}</b></div>
      <div class="compare-row"><span>Banda larga escolar</span><b>${formatPercent(row.perc_escolas_banda_larga)}</b></div>
      <div class="compare-row"><span>Escolas</span><b>${formatNumber(row.escolas,0)}</b></div>
      <div class="compare-row"><span>Matrículas</span><b>${formatNumber(row.matriculas,0)}</b></div>`;
    return card;
  }
  function renderComparison() {
    const container = $("comparison");
    if (!container) return;
    const ids = [$("compare-1")?.value,$("compare-2")?.value,$("compare-3")?.value].filter(Boolean);
    comparisonRows = [...new Set(ids)].map(uf=>rows.find(row=>row.uf===uf)).filter(Boolean);
    container.replaceChildren();
    if (!comparisonRows.length) {
      container.textContent = "Selecione pelo menos uma UF para comparar.";
      return;
    }
    comparisonRows.forEach(row=>container.appendChild(comparisonCard(row)));
  }
  function csvCell(value, separator) {
    const text = value == null ? "" : String(value);
    return text.includes('"') || text.includes("\r") || text.includes("\n") || text.includes(separator)
      ? `"${text.replace(/"/g,'""')}"` : text;
  }
  function createCsv(data, separator=";", decimalComma=true) {
    if (!data.length) return "";
    const keys = Object.keys(data[0]);
    const lines = [keys.map(key=>csvCell(key,separator)).join(separator)];
    for (const row of data) {
      lines.push(keys.map(key=>{
        let value = row[key];
        if (typeof value === "number" && decimalComma) value = String(value).replace(".",",");
        return csvCell(value,separator);
      }).join(separator));
    }
    return "\uFEFF"+lines.join("\r\n")+"\r\n";
  }
  function download(content, filename) {
    const blob = new Blob([content],{type:"text/csv;charset=utf-8"});
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href=url; anchor.download=filename; anchor.hidden=true;
    document.body.appendChild(anchor); anchor.click(); anchor.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  function bindControls() {
    const uf = $("uf");
    if (uf) uf.addEventListener("change",()=>renderUf(rows.find(row=>row.uf===uf.value)));
    $("compare-button")?.addEventListener("click",(event)=>{event.preventDefault();renderComparison();});
    $("download")?.addEventListener("click",()=>{
      if (!selected) return setMessage("Selecione uma UF.",true);
      download(createCsv([selected],";",true),`protege-dados-${selected.uf}-excel.csv`);
      setMessage("Arquivo compatível com Excel gerado com sucesso.");
    });
    $("download-standard")?.addEventListener("click",()=>{
      if (!selected) return setMessage("Selecione uma UF.",true);
      download(createCsv([selected],",",false),`protege-dados-${selected.uf}.csv`);
      setMessage("CSV padrão gerado com sucesso.");
    });
    $("download-comparison")?.addEventListener("click",()=>{
      if (!comparisonRows.length) return setMessage("Atualize a comparação antes de exportar.",true);
      download(createCsv(comparisonRows,";",true),"protege-dados-comparacao.csv");
      setMessage("Comparação exportada com sucesso.");
    });
  }
  function renderTable() {
    const body = $("uf-table-body");
    if (!body) return;
    body.replaceChildren();
    for (const row of rows) {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td><strong>${row.uf}</strong></td><td>${formatNumber(row.eixo_vulnerabilidade)}</td><td>${formatNumber(row.taxa_denuncias_100mil)}</td><td>${formatPercent(row.perc_escolas_internet)}</td><td>${formatPercent(row.perc_escolas_banda_larga)}</td>`;
      body.appendChild(tr);
    }
  }
  async function init() {
    try {
      rows = await loadRows();
      fillSelect($("uf"));
      fillSelect($("compare-1"));
      fillSelect($("compare-2"));
      fillSelect($("compare-3"),true);
      if ($("uf")) {
        $("uf").value="DF";
        renderUf(rows.find(row=>row.uf==="DF")||rows[0]);
      }
      if ($("compare-1")) $("compare-1").value="DF";
      if ($("compare-2")) $("compare-2").value="SP";
      if ($("compare-3")) $("compare-3").value="BA";
      renderComparison();
      renderTable();
      bindControls();
      setNotice("Portal carregado com sucesso: 27 UFs disponíveis.");
    } catch (error) {
      console.error(error);
      setNotice(`Não foi possível carregar os dados: ${error.message}`,true);
      for (const id of ["uf","compare-1","compare-2","compare-3"]) {
        const select=$(id);
        if (select) select.replaceChildren(new Option("Dados indisponíveis",""));
      }
    }
  }
  if (document.readyState==="loading") document.addEventListener("DOMContentLoaded",init,{once:true});
  else init();
})();

;(()=>{try{const r=document.documentElement,b=document.body;b.classList.toggle("high-contrast",localStorage.getItem("pd-contrast")==="1");b.classList.toggle("links-underlined",localStorage.getItem("pd-links")==="1");r.classList.toggle("font-large",localStorage.getItem("pd-font")==="1");}catch(_){}})();
