(() => {
  "use strict";

  const DATA_URL = "data/ivpd_uf_v1.json";

  function byId(id) {
    return document.getElementById(id);
  }

  function toNumber(value) {
    if (typeof value === "number") return value;
    if (value === null || value === undefined || value === "") return NaN;

    const text = String(value).trim();
    return Number(
      text.includes(",")
        ? text.replace(/\./g, "").replace(",", ".")
        : text
    );
  }

  function formatNumber(value, decimals = 1) {
    const number = toNumber(value);

    if (!Number.isFinite(number)) return "—";

    return new Intl.NumberFormat("pt-BR", {
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    }).format(number);
  }

  function formatPercent(value) {
    const number = toNumber(value);
    return Number.isFinite(number) ? `${formatNumber(number, 1)}%` : "—";
  }

  function escapeCsv(value, separator) {
    const text = value === null || value === undefined ? "" : String(value);

    if (
      text.includes('"') ||
      text.includes("\n") ||
      text.includes("\r") ||
      text.includes(separator)
    ) {
      return `"${text.replace(/"/g, '""')}"`;
    }

    return text;
  }

  function createCsv(rows, separator = ";", decimalComma = true) {
    if (!Array.isArray(rows) || rows.length === 0) return "";

    const keys = Object.keys(rows[0]);
    const output = [keys.map(key => escapeCsv(key, separator)).join(separator)];

    for (const row of rows) {
      output.push(
        keys.map(key => {
          let value = row[key];

          if (typeof value === "number" && decimalComma) {
            value = String(value).replace(".", ",");
          }

          return escapeCsv(value, separator);
        }).join(separator)
      );
    }

    return "\uFEFF" + output.join("\r\n") + "\r\n";
  }

  function saveFile(content, filename) {
    const blob = new Blob([content], {
      type: "text/csv;charset=utf-8;"
    });

    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");

    anchor.href = url;
    anchor.download = filename;
    anchor.style.display = "none";

    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();

    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function createBar(label, value) {
    const number = toNumber(value);
    const safeValue = Number.isFinite(number)
      ? Math.max(0, Math.min(100, number))
      : 0;

    const element = document.createElement("div");
    element.className = "indicator-bar";
    element.innerHTML = `
      <div style="display:flex;justify-content:space-between;gap:12px;margin:10px 0 5px">
        <strong>${label}</strong>
        <span>${formatNumber(safeValue, 1)}</span>
      </div>
      <div class="mini-bar">
        <i style="width:${safeValue}%"></i>
      </div>
    `;

    return element;
  }

  function startApplication() {
    const ui = {
      uf: byId("uf"),
      vulnerability: byId("vuln"),
      complaintRate: byId("taxa"),
      internet: byId("internet"),
      broadband: byId("banda"),
      bars: byId("bars"),
      download: byId("download"),
      downloadStandard: byId("download-standard"),
      message: byId("download-message"),
      compare1: byId("compare-1"),
      compare2: byId("compare-2"),
      compare3: byId("compare-3"),
      compareButton: byId("compare-button"),
      comparison: byId("comparison"),
      downloadComparison: byId("download-comparison")
    };

    const required = [
      "uf",
      "vulnerability",
      "complaintRate",
      "internet",
      "broadband",
      "bars"
    ];

    const missing = required.filter(key => !ui[key]);

    if (missing.length > 0) {
      console.error("Elementos obrigatórios ausentes:", missing);
      return;
    }

    let records = [];
    let selectedRecord = null;
    let comparisonRecords = [];

    function showMessage(text, isError = false) {
      if (!ui.message) return;

      ui.message.textContent = text;
      ui.message.style.color = isError ? "#9b1c1c" : "#126d3a";
    }

    function normalizeRecord(row) {
      return {
        ...row,
        uf: String(row.uf || "").trim().toUpperCase()
      };
    }

    function renderRecord(record) {
      if (!record) return;

      selectedRecord = record;

      ui.vulnerability.textContent = formatNumber(
        record.eixo_vulnerabilidade,
        1
      );

      ui.complaintRate.textContent = formatNumber(
        record.taxa_denuncias_100mil,
        1
      );

      ui.internet.textContent = formatPercent(
        record.perc_escolas_internet
      );

      ui.broadband.textContent = formatPercent(
        record.perc_escolas_banda_larga
      );

      ui.bars.innerHTML = "";
      ui.bars.append(
        createBar("Denúncias notificadas", record.n_taxa_denuncias),
        createBar(
          "Déficit de internet escolar",
          record.n_deficit_internet
        ),
        createBar(
          "Déficit de banda larga escolar",
          record.n_deficit_banda_larga
        )
      );
    }

    function createComparisonCard(record) {
      const card = document.createElement("article");
      card.className = "compare-card";
      card.innerHTML = `
        <h3>${record.uf}</h3>
        <div class="compare-row">
          <span>IVPD</span>
          <b>${formatNumber(record.eixo_vulnerabilidade, 1)}</b>
        </div>
        <div class="mini-bar">
          <i style="width:${Math.max(
            0,
            Math.min(100, toNumber(record.eixo_vulnerabilidade) || 0)
          )}%"></i>
        </div>
        <div class="compare-row">
          <span>Taxa de denúncias</span>
          <b>${formatNumber(record.taxa_denuncias_100mil, 1)}</b>
        </div>
        <div class="compare-row">
          <span>Internet escolar</span>
          <b>${formatPercent(record.perc_escolas_internet)}</b>
        </div>
        <div class="compare-row">
          <span>Banda larga escolar</span>
          <b>${formatPercent(record.perc_escolas_banda_larga)}</b>
        </div>
        <div class="compare-row">
          <span>Escolas</span>
          <b>${formatNumber(record.escolas, 0)}</b>
        </div>
        <div class="compare-row">
          <span>Matrículas</span>
          <b>${formatNumber(record.matriculas, 0)}</b>
        </div>
      `;

      return card;
    }

    function updateComparison() {
      if (
        !ui.compare1 ||
        !ui.compare2 ||
        !ui.compare3 ||
        !ui.comparison
      ) {
        return;
      }

      const selectedUfs = [
        ui.compare1.value,
        ui.compare2.value,
        ui.compare3.value
      ].filter(Boolean);

      const uniqueUfs = [...new Set(selectedUfs)];

      comparisonRecords = uniqueUfs
        .map(uf => records.find(record => record.uf === uf))
        .filter(Boolean);

      ui.comparison.innerHTML = "";

      for (const record of comparisonRecords) {
        ui.comparison.appendChild(createComparisonCard(record));
      }

      if (comparisonRecords.length === 0) {
        ui.comparison.textContent =
          "Selecione pelo menos uma UF para comparar.";
      }
    }

    function fillSelect(select, includeEmpty = false) {
      if (!select) return;

      const options = [];

      if (includeEmpty) {
        options.push('<option value="">Nenhuma</option>');
      }

      for (const record of records) {
        options.push(
          `<option value="${record.uf}">${record.uf}</option>`
        );
      }

      select.innerHTML = options.join("");
    }

    async function loadData() {
      const response = await fetch(DATA_URL, {
        cache: "no-store",
        headers: {
          Accept: "application/json"
        }
      });

      if (!response.ok) {
        throw new Error(`Falha ao carregar os dados: HTTP ${response.status}`);
      }

      const payload = await response.json();

      if (!Array.isArray(payload)) {
        throw new Error("O arquivo de dados não contém uma lista de UFs.");
      }

      records = payload
        .map(normalizeRecord)
        .filter(record => record.uf);

      records.sort((a, b) => a.uf.localeCompare(b.uf, "pt-BR"));

      if (records.length !== 27) {
        console.warn(
          `Foram carregadas ${records.length} UFs; eram esperadas 27.`
        );
      }
    }

    async function initialize() {
      try {
        loadButtonListeners();

        await loadData();

        fillSelect(ui.uf);
        fillSelect(ui.compare1);
        fillSelect(ui.compare2);
        fillSelect(ui.compare3, true);

        const initial = records.find(record => record.uf === "DF") || records[0];

        if (!initial) {
          throw new Error("Nenhuma UF foi encontrada no arquivo de dados.");
        }

        ui.uf.value = initial.uf;
        renderRecord(initial);

        if (ui.compare1) ui.compare1.value = "DF";
        if (ui.compare2) ui.compare2.value = "SP";
        if (ui.compare3) ui.compare3.value = "BA";

        updateComparison();
        showMessage("");
      } catch (error) {
        console.error(error);

        ui.uf.innerHTML =
          '<option value="">Erro ao carregar as UFs</option>';

        showMessage(
          "Não foi possível carregar os indicadores. Atualize a página com Ctrl+F5.",
          true
        );
      }
    }

    function loadButtonListeners() {
      ui.uf.addEventListener("change", () => {
        const record = records.find(item => item.uf === ui.uf.value);
        renderRecord(record);
      });

      if (ui.compareButton) {
        ui.compareButton.addEventListener("click", event => {
          event.preventDefault();
          updateComparison();
        });
      }

      if (ui.download) {
        ui.download.addEventListener("click", event => {
          event.preventDefault();

          if (!selectedRecord) {
            showMessage("Selecione uma UF.", true);
            return;
          }

          saveFile(
            createCsv([selectedRecord], ";", true),
            `protege-dados-4-1-${selectedRecord.uf}-excel.csv`
          );

          showMessage(
            "Arquivo compatível com Excel brasileiro gerado."
          );
        });
      }

      if (ui.downloadStandard) {
        ui.downloadStandard.addEventListener("click", event => {
          event.preventDefault();

          if (!selectedRecord) {
            showMessage("Selecione uma UF.", true);
            return;
          }

          saveFile(
            createCsv([selectedRecord], ",", false),
            `protege-dados-4-1-${selectedRecord.uf}.csv`
          );

          showMessage("CSV padrão internacional gerado.");
        });
      }

      if (ui.downloadComparison) {
        ui.downloadComparison.addEventListener("click", event => {
          event.preventDefault();

          if (comparisonRecords.length === 0) {
            showMessage(
              "Selecione UFs e atualize a comparação.",
              true
            );
            return;
          }

          saveFile(
            createCsv(comparisonRecords, ";", true),
            "protege-dados-4-1-comparacao-excel.csv"
          );

          showMessage("Comparação exportada com sucesso.");
        });
      }
    }

    initialize();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", startApplication);
  } else {
    startApplication();
  }
})();
