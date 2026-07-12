(() => {
  "use strict";

  const DATA_URL = "data/ivpd_uf_v1.json";

  const UF_NAMES = {
    AC: "Acre", AL: "Alagoas", AP: "Amapá", AM: "Amazonas", BA: "Bahia",
    CE: "Ceará", DF: "Distrito Federal", ES: "Espírito Santo", GO: "Goiás",
    MA: "Maranhão", MT: "Mato Grosso", MS: "Mato Grosso do Sul",
    MG: "Minas Gerais", PA: "Pará", PB: "Paraíba", PR: "Paraná",
    PE: "Pernambuco", PI: "Piauí", RJ: "Rio de Janeiro",
    RN: "Rio Grande do Norte", RS: "Rio Grande do Sul", RO: "Rondônia",
    RR: "Roraima", SC: "Santa Catarina", SP: "São Paulo", SE: "Sergipe",
    TO: "Tocantins"
  };

  const byId = (id) => document.getElementById(id);

  const ui = {
    panel: byId("painel"),
    uf: byId("uf"),
    vuln: byId("vuln"),
    taxa: byId("taxa"),
    internet: byId("internet"),
    bars: byId("bars"),
    downloadExcel: byId("download"),
    downloadStandard: byId("download-standard"),
    message: byId("download-message"),
    loading: byId("loading-status"),
    menuButton: document.querySelector(".menu-toggle"),
    menu: byId("menu-principal")
  };

  let records = [];
  let selected = null;

  function number(value) {
    if (typeof value === "number") return value;
    if (value === null || value === undefined || value === "") return NaN;

    const text = String(value).trim();
    if (text.includes(",")) {
      return Number(text.replace(/\./g, "").replace(",", "."));
    }

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
    const safe = Number.isFinite(value)
      ? Math.min(100, Math.max(0, value))
      : 0;

    const wrapper = document.createElement("div");
    wrapper.className = "bar-item";

    const header = document.createElement("div");
    header.className = "bar-header";

    const labelElement = document.createElement("span");
    labelElement.textContent = label;

    const valueElement = document.createElement("strong");
    valueElement.textContent = format(safe);

    const track = document.createElement("div");
    track.className = "bar-track";
    track.setAttribute("role", "progressbar");
    track.setAttribute("aria-label", label);
    track.setAttribute("aria-valuemin", "0");
    track.setAttribute("aria-valuemax", "100");
    track.setAttribute("aria-valuenow", String(Math.round(safe)));

    const fill = document.createElement("div");
    fill.className = "bar-fill";
    fill.style.width = `${safe}%`;

    header.append(labelElement, valueElement);
    track.append(fill);
    wrapper.append(header, track);

    return wrapper;
  }

  function render(row) {
    selected = derive(row);

    ui.vuln.textContent = format(selected.vulnerabilidade);
    ui.taxa.textContent = format(selected.taxa);
    ui.internet.textContent = Number.isFinite(selected.internetPct)
      ? `${format(selected.internetPct)}%`
      : "—";

    ui.bars.replaceChildren(
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
    const header = keys.map((key) => escapeCsv(key, separator)).join(separator);

    const values = keys
      .map((key) => {
        let value = row[key];

        if (typeof value === "number" && decimalComma) {
          value = String(value).replace(".", ",");
        }

        return escapeCsv(value, separator);
      })
      .join(separator);

    return "\uFEFF" + header + "\r\n" + values + "\r\n";
  }

  function save(content, filename) {
    const blob = new Blob([content], {
      type: "text/csv;charset=utf-8;"
    });

    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");

    anchor.href = url;
    anchor.download = filename;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();

    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function message(text, error = false) {
    ui.message.textContent = text;
    ui.message.classList.toggle("error", error);
    ui.message.classList.toggle("success", !error);
  }

  function setLoading(isLoading, text = "") {
    ui.panel.setAttribute("aria-busy", String(isLoading));
    ui.uf.disabled = isLoading;
    ui.downloadExcel.disabled = isLoading;
    ui.downloadStandard.disabled = isLoading;
    ui.loading.hidden = !text;
    ui.loading.textContent = text;
  }

  function configureMenu() {
    if (!ui.menuButton || !ui.menu) return;

    ui.menuButton.addEventListener("click", () => {
      const expanded = ui.menuButton.getAttribute("aria-expanded") === "true";
      ui.menuButton.setAttribute("aria-expanded", String(!expanded));
      ui.menu.classList.toggle("is-open", !expanded);
    });

    ui.menu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        ui.menuButton.setAttribute("aria-expanded", "false");
        ui.menu.classList.remove("is-open");
      });
    });
  }

  async function init() {
    configureMenu();
    setLoading(true, "Carregando indicadores...");

    try {
      const response = await fetch(DATA_URL, { cache: "no-store" });

      if (!response.ok) {
        throw new Error(`Falha HTTP ${response.status}`);
      }

      const payload = await response.json();

      if (!Array.isArray(payload) || payload.length === 0) {
        throw new Error("A base de indicadores está vazia ou em formato inválido.");
      }

      records = payload
        .map(derive)
        .filter((item) => item.uf && UF_NAMES[item.uf]);

      records.sort((a, b) =>
        UF_NAMES[a.uf].localeCompare(UF_NAMES[b.uf], "pt-BR")
      );

      ui.uf.innerHTML = records
        .map(
          (item) =>
            `<option value="${item.uf}">${UF_NAMES[item.uf]} — ${item.uf}</option>`
        )
        .join("");

      const initial = records.find((item) => item.uf === "DF") || records[0];

      ui.uf.value = initial.uf;
      render(initial);

      ui.uf.addEventListener("change", () => {
        const row = records.find((item) => item.uf === ui.uf.value);
        if (row) render(row);
      });

      ui.downloadExcel.addEventListener("click", () => {
        if (!selected) {
          return message("Selecione uma unidade federativa.", true);
        }

        save(
          makeCsv(selected, ";", true),
          `protege-dados-${selected.uf}-excel.csv`
        );

        message("CSV compatível com Excel brasileiro gerado.");
      });

      ui.downloadStandard.addEventListener("click", () => {
        if (!selected) {
          return message("Selecione uma unidade federativa.", true);
        }

        save(
          makeCsv(selected, ",", false),
          `protege-dados-${selected.uf}.csv`
        );

        message("CSV padrão internacional gerado.");
      });

      setLoading(false, "");
    } catch (error) {
      console.error(error);
      selected = null;
      ui.uf.innerHTML = "<option>Dados indisponíveis</option>";
      setLoading(true, "Não foi possível carregar os indicadores. Atualize a página ou consulte a base no repositório.");
      message("Falha no carregamento da base de indicadores.", true);
    }
  }

  init();
})();
