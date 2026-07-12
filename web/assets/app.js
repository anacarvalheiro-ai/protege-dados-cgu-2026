(() => {
  "use strict";

  const DATA_URL = "data/ivpd_uf_v1.json";
  const byId = id => document.getElementById(id);
  const ui = {
    uf: byId("uf"),
    vuln: byId("vuln"),
    taxa: byId("taxa"),
    internet: byId("internet"),
    bars: byId("bars"),
    downloadExcel: byId("download"),
    downloadStandard: byId("download-standard"),
    message: byId("download-message")
  };

  let records = [];
  let selected = null;

  function number(value) {
    if (typeof value === "number") return value;
    if (value === null || value === undefined || value === "") return NaN;
    const text = String(value).trim();
    if (text.includes(",")) return Number(text.replace(/\./g, "").replace(",", "."));
    return Number(text);
  }

  function format(value, decimals = 1) {
    const n = number(value);
    return Number.isFinite(n)
      ? new Intl.NumberFormat("pt-BR", {
          minimumFractionDigits: decimals,
          maximumFractionDigits: decimals
        }).format(n)
      : "—";
  }

  function derive(row) {
    const populacao = number(row.populacao);
    const denuncias = number(row.denuncias);
    const escolas = number(row.escolas);
    const escolasInternet = number(row.escolas_internet);

    return {
      ...row,
      uf: String(row.uf || "").trim().toUpperCase(),
      taxa: Number.isFinite(number(row.taxa_denuncias_100mil))
        ? number(row.taxa_denuncias_100mil)
        : denuncias / populacao * 100000,
      internetPct: Number.isFinite(number(row.perc_escolas_internet))
        ? number(row.perc_escolas_internet)
        : escolasInternet / escolas * 100,
      vulnerabilidade: number(row.eixo_vulnerabilidade),
      denunciasNorm: number(row.n_taxa_denuncias),
      deficitInternetNorm: number(row.n_deficit_internet),
      deficitBandaNorm: number(row.n_deficit_banda_larga)
    };
  }

  function createBar(label, value) {
    const safe = Number.isFinite(value) ? Math.min(100, Math.max(0, value)) : 0;
    const box = document.createElement("div");
    box.innerHTML = `
      <div style="display:flex;justify-content:space-between;margin:.65rem 0 .3rem">
        <strong>${label}</strong><span>${format(safe)}</span>
      </div>
      <div style="height:.78rem;border-radius:999px;background:#dfe8f0;overflow:hidden">
        <div style="width:${safe}%;height:100%;background:#0b6db5"></div>
      </div>`;
    return box;
  }

  function render(row) {
    selected = derive(row);
    ui.vuln.textContent = format(selected.vulnerabilidade);
    ui.taxa.textContent = format(selected.taxa);
    ui.internet.textContent = Number.isFinite(selected.internetPct)
      ? `${format(selected.internetPct)}%`
      : "—";

    ui.bars.innerHTML = "";
    ui.bars.append(
      createBar("Denúncias notificadas", selected.denunciasNorm),
      createBar("Déficit de internet escolar", selected.deficitInternetNorm),
      createBar("Déficit de banda larga escolar", selected.deficitBandaNorm)
    );
  }

  function escapeCsv(value, separator) {
    const text = value === null || value === undefined ? "" : String(value);
    return text.includes('"') || text.includes("\n") || text.includes(separator)
      ? `"${text.replace(/"/g, '""')}"`
      : text;
  }

  function makeCsv(row, separator, decimalComma) {
    const keys = Object.keys(row);
    const header = keys.map(key => escapeCsv(key, separator)).join(separator);
    const values = keys.map(key => {
      let value = row[key];
      if (typeof value === "number" && decimalComma) {
        value = String(value).replace(".", ",");
      }
      return escapeCsv(value, separator);
    }).join(separator);
    return "\uFEFF" + header + "\r\n" + values + "\r\n";
  }

  function save(content, filename) {
    const blob = new Blob([content], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
  }

  function message(text, error = false) {
    ui.message.textContent = text;
    ui.message.style.color = error ? "#9b1c1c" : "#14733c";
  }

  async function init() {
    try {
      const response = await fetch(DATA_URL, { cache: "no-store" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const payload = await response.json();
      records = payload.map(derive).filter(item => item.uf);
      records.sort((a, b) => a.uf.localeCompare(b.uf, "pt-BR"));

      ui.uf.innerHTML = records
        .map(item => `<option value="${item.uf}">${item.uf}</option>`)
        .join("");

      const initial = records.find(item => item.uf === "DF") || records[0];
      ui.uf.value = initial.uf;
      render(initial);

      ui.uf.addEventListener("change", () => {
        const row = records.find(item => item.uf === ui.uf.value);
        if (row) render(row);
      });

      ui.downloadExcel.addEventListener("click", () => {
        if (!selected) return message("Selecione uma UF.", true);
        save(makeCsv(selected, ";", true), `protege-dados-${selected.uf}-excel.csv`);
        message("Arquivo compatível com Excel brasileiro gerado.");
      });

      ui.downloadStandard.addEventListener("click", () => {
        if (!selected) return message("Selecione uma UF.", true);
        save(makeCsv(selected, ",", false), `protege-dados-${selected.uf}.csv`);
        message("CSV padrão internacional gerado.");
      });
    } catch (error) {
      console.error(error);
      message("Não foi possível carregar os indicadores.", true);
    }
  }

  init();
})();