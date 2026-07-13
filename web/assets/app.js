(() => {
  "use strict";

  const DATA_URL = "data/ivpd_uf_v1.json";
  const EXPECTED = new Set(["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"]);
  const UF_NAMES = {
    AC:"Acre", AL:"Alagoas", AP:"Amapá", AM:"Amazonas", BA:"Bahia", CE:"Ceará", DF:"Distrito Federal",
    ES:"Espírito Santo", GO:"Goiás", MA:"Maranhão", MT:"Mato Grosso", MS:"Mato Grosso do Sul", MG:"Minas Gerais",
    PA:"Pará", PB:"Paraíba", PR:"Paraná", PE:"Pernambuco", PI:"Piauí", RJ:"Rio de Janeiro", RN:"Rio Grande do Norte",
    RS:"Rio Grande do Sul", RO:"Rondônia", RR:"Roraima", SC:"Santa Catarina", SP:"São Paulo", SE:"Sergipe", TO:"Tocantins"
  };
  const MAP_POSITIONS = {
    RR:[12,4], AP:[62,5], AM:[15,18], PA:[48,19], MA:[68,23], CE:[82,28], RN:[91,32],
    AC:[2,31], RO:[20,35], MT:[35,42], TO:[56,40], PI:[72,36], PB:[91,40], PE:[86,46],
    AL:[88,52], SE:[82,55], BA:[69,52], GO:[52,52], DF:[59,56], MS:[35,57], MG:[62,61],
    ES:[74,65], SP:[52,68], RJ:[66,71], PR:[46,74], SC:[48,80], RS:[38,85]
  };

  const $ = (id) => document.getElementById(id);
  let rows = [];
  let selected = null;
  let comparisonRows = [];

  function numberValue(value) {
    if (typeof value === "number") return value;
    if (value === null || value === undefined || value === "") return NaN;
    return Number(String(value).replace(/\s/g, "").replace(",", "."));
  }

  function formatNumber(value, digits = 1) {
    const numeric = numberValue(value);
    return Number.isFinite(numeric)
      ? new Intl.NumberFormat("pt-BR", { minimumFractionDigits: digits, maximumFractionDigits: digits }).format(numeric)
      : "—";
  }

  function formatInteger(value) {
    const numeric = numberValue(value);
    return Number.isFinite(numeric) ? new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 0 }).format(numeric) : "—";
  }

  function formatPercent(value) { return Number.isFinite(numberValue(value)) ? `${formatNumber(value, 1)}%` : "—"; }

  function setText(id, value) { const element = $(id); if (element) element.textContent = value; }

  function setNotice(text, error = false) {
    const notice = $("portal-status");
    if (!notice) return;
    notice.textContent = text;
    notice.className = error ? "notice error" : "notice";
  }

  function setMessage(text, error = false) {
    const message = $("download-message");
    if (!message) return;
    message.textContent = text;
    message.style.color = error ? "#a22929" : "#117443";
  }

  async function loadRows() {
    const response = await fetch(DATA_URL, { cache: "no-store", headers: { Accept: "application/json" } });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload = await response.json();
    const list = Array.isArray(payload) ? payload : payload.territories;
    if (!Array.isArray(list)) throw new Error("Formato de dados inválido");

    const map = new Map();
    for (const item of list) {
      const uf = String(item.uf || "").trim().toUpperCase();
      if (EXPECTED.has(uf)) map.set(uf, { ...item, uf });
    }
    const normalized = [...map.values()].sort((a, b) => a.uf.localeCompare(b.uf, "pt-BR"));
    if (normalized.length !== 27) throw new Error(`A base contém ${normalized.length} UFs; eram esperadas 27`);
    return normalized;
  }

  function fillSelect(select, allowEmpty = false) {
    if (!select) return;
    select.replaceChildren();
    if (allowEmpty) select.add(new Option("Nenhuma", ""));
    for (const row of rows) select.add(new Option(`${UF_NAMES[row.uf]} (${row.uf})`, row.uf));
  }

  function levelFor(value) {
    const v = numberValue(value);
    if (!Number.isFinite(v)) return 1;
    if (v < 20) return 1;
    if (v < 35) return 2;
    if (v < 50) return 3;
    if (v < 65) return 4;
    return 5;
  }

  function makeBar(label, value) {
    const raw = numberValue(value);
    const width = Number.isFinite(raw) ? Math.max(0, Math.min(100, raw)) : 0;
    const element = document.createElement("div");
    element.innerHTML = `<div class="bar-title"><strong>${label}</strong><span>${formatNumber(width)}</span></div><div class="bar" aria-label="${label}: ${formatNumber(width)} de 100"><i style="width:${width}%"></i></div>`;
    return element;
  }

  function renderMap() {
    const container = $("uf-map");
    if (!container) return;
    container.replaceChildren();

    for (const row of rows) {
      const button = document.createElement("button");
      const [left, top] = MAP_POSITIONS[row.uf] || [50, 50];
      button.type = "button";
      button.className = "map-tile";
      button.dataset.level = String(levelFor(row.eixo_vulnerabilidade));
      button.style.left = `${left}%`;
      button.style.top = `${top}%`;
      button.style.transformOrigin = "center";
      button.textContent = row.uf;
      button.title = `${UF_NAMES[row.uf]} — IVPD ${formatNumber(row.eixo_vulnerabilidade)}`;
      button.setAttribute("aria-label", `${UF_NAMES[row.uf]}, IVPD ${formatNumber(row.eixo_vulnerabilidade)}`);
      button.setAttribute("aria-pressed", String(selected?.uf === row.uf));
      button.addEventListener("click", () => {
        const select = $("uf");
        if (select) select.value = row.uf;
        renderUf(row);
      });
      container.appendChild(button);
    }
  }

  function renderUf(row) {
    if (!row) return;
    selected = row;
    setText("selected-name", `${UF_NAMES[row.uf]} (${row.uf})`);
    setText("selected-period", `Denúncias ${row.periodo_denuncias} · população ${row.ano_populacao} · Censo Escolar ${row.ano_censo_escolar}`);
    setText("vuln", formatNumber(row.eixo_vulnerabilidade));
    setText("taxa", formatNumber(row.taxa_denuncias_100mil));
    setText("internet", formatPercent(row.perc_escolas_internet));
    setText("banda", formatPercent(row.perc_escolas_banda_larga));
    setText("selected-denuncias", formatInteger(row.denuncias));
    setText("selected-escolas", formatInteger(row.escolas));
    setText("selected-matriculas", formatInteger(row.matriculas));
    setText("selected-populacao", formatInteger(row.populacao));
    setText("selected-note", row.nota_metodologica || "Índice experimental e agregado por UF.");

    const bars = $("bars");
    if (bars) {
      bars.replaceChildren(
        makeBar("Denúncias notificadas", row.n_taxa_denuncias),
        makeBar("Déficit de internet escolar", row.n_deficit_internet),
        makeBar("Déficit de banda larga escolar", row.n_deficit_banda_larga)
      );
    }
    renderMap();
  }

  function comparisonCard(row) {
    const card = document.createElement("article");
    card.className = "compare-card";
    card.innerHTML = `<h3>${UF_NAMES[row.uf]} <small>(${row.uf})</small></h3>
      <div class="compare-row"><span>IVPD experimental</span><b>${formatNumber(row.eixo_vulnerabilidade)}</b></div>
      <div class="compare-row"><span>Taxa de denúncias</span><b>${formatNumber(row.taxa_denuncias_100mil)}</b></div>
      <div class="compare-row"><span>Internet escolar</span><b>${formatPercent(row.perc_escolas_internet)}</b></div>
      <div class="compare-row"><span>Banda larga escolar</span><b>${formatPercent(row.perc_escolas_banda_larga)}</b></div>
      <div class="compare-row"><span>Escolas</span><b>${formatInteger(row.escolas)}</b></div>
      <div class="compare-row"><span>Matrículas</span><b>${formatInteger(row.matriculas)}</b></div>`;
    return card;
  }

  function renderComparison() {
    const container = $("comparison");
    if (!container) return;
    const ids = [$("compare-1")?.value, $("compare-2")?.value, $("compare-3")?.value].filter(Boolean);
    comparisonRows = [...new Set(ids)].map((uf) => rows.find((row) => row.uf === uf)).filter(Boolean);
    container.replaceChildren();
    if (!comparisonRows.length) {
      container.textContent = "Selecione pelo menos uma UF para comparar.";
      return;
    }
    comparisonRows.forEach((row) => container.appendChild(comparisonCard(row)));

    const body = $("comparison-table-body");
    if (body) {
      body.replaceChildren();
      for (const row of comparisonRows) {
        const tr = document.createElement("tr");
        tr.innerHTML = `<td><strong>${UF_NAMES[row.uf]} (${row.uf})</strong></td><td>${formatNumber(row.eixo_vulnerabilidade)}</td><td>${formatNumber(row.taxa_denuncias_100mil)}</td><td>${formatPercent(row.perc_escolas_internet)}</td><td>${formatPercent(row.perc_escolas_banda_larga)}</td>`;
        body.appendChild(tr);
      }
    }
  }

  function csvCell(value, separator) {
    const text = value == null ? "" : String(value);
    return text.includes('"') || text.includes("\r") || text.includes("\n") || text.includes(separator)
      ? `"${text.replace(/"/g, '""')}"` : text;
  }

  function createCsv(data, separator = ";", decimalComma = true) {
    if (!data.length) return "";
    const keys = Object.keys(data[0]);
    const lines = [keys.map((key) => csvCell(key, separator)).join(separator)];
    for (const row of data) {
      lines.push(keys.map((key) => {
        let value = row[key];
        if (typeof value === "number" && decimalComma) value = String(value).replace(".", ",");
        return csvCell(value, separator);
      }).join(separator));
    }
    return `\uFEFF${lines.join("\r\n")}\r\n`;
  }

  function download(content, filename) {
    const blob = new Blob([content], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = filename;
    anchor.hidden = true;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function bindControls() {
    const uf = $("uf");
    uf?.addEventListener("change", () => renderUf(rows.find((row) => row.uf === uf.value)));
    $("compare-button")?.addEventListener("click", () => renderComparison());
    $("download")?.addEventListener("click", () => {
      if (!selected) return setMessage("Selecione uma UF.", true);
      download(createCsv([selected], ";", true), `protege-dados-${selected.uf}-excel.csv`);
      setMessage("Arquivo compatível com Excel gerado com sucesso.");
    });
    $("download-standard")?.addEventListener("click", () => {
      if (!selected) return setMessage("Selecione uma UF.", true);
      download(createCsv([selected], ",", false), `protege-dados-${selected.uf}.csv`);
      setMessage("CSV padrão gerado com sucesso.");
    });
    $("download-comparison")?.addEventListener("click", () => {
      if (!comparisonRows.length) return setMessage("Atualize a comparação antes de exportar.", true);
      download(createCsv(comparisonRows, ";", true), "protege-dados-comparacao.csv");
      setMessage("Comparação exportada com sucesso.");
    });
  }

  function renderTable() {
    const body = $("uf-table-body");
    if (!body) return;
    body.replaceChildren();
    for (const row of rows) {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td><strong>${UF_NAMES[row.uf]} (${row.uf})</strong></td><td>${formatNumber(row.eixo_vulnerabilidade)}</td><td>${formatNumber(row.taxa_denuncias_100mil)}</td><td>${formatPercent(row.perc_escolas_internet)}</td><td>${formatPercent(row.perc_escolas_banda_larga)}</td><td>${formatInteger(row.escolas)}</td><td>${formatInteger(row.matriculas)}</td>`;
      body.appendChild(tr);
    }
  }

  function updateHomeTotals() {
    if (!$("home-total-ufs")) return;
    const sum = (key) => rows.reduce((total, row) => total + (numberValue(row[key]) || 0), 0);
    setText("home-total-ufs", formatInteger(rows.length));
    setText("home-total-escolas", formatInteger(sum("escolas")));
    setText("home-total-matriculas", formatInteger(sum("matriculas")));
    setText("home-total-denuncias", formatInteger(sum("denuncias")));
  }

  async function init() {
    try {
      rows = await loadRows();
      updateHomeTotals();
      fillSelect($("uf"));
      fillSelect($("compare-1"));
      fillSelect($("compare-2"));
      fillSelect($("compare-3"), true);

      if ($("uf")) {
        $("uf").value = "DF";
        renderUf(rows.find((row) => row.uf === "DF") || rows[0]);
      }
      if ($("compare-1")) $("compare-1").value = "DF";
      if ($("compare-2")) $("compare-2").value = "SP";
      if ($("compare-3")) $("compare-3").value = "BA";

      renderComparison();
      renderTable();
      bindControls();
      setNotice("Portal carregado com sucesso: 27 UFs disponíveis.");
    } catch (error) {
      console.error(error);
      setNotice(`Não foi possível carregar os dados: ${error.message}`, true);
      for (const id of ["uf", "compare-1", "compare-2", "compare-3"]) {
        const select = $(id);
        if (select) select.replaceChildren(new Option("Dados indisponíveis", ""));
      }
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init, { once: true });
  else init();
})();
