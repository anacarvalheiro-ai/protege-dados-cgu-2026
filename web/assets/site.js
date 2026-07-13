(() => {
  "use strict";

  const root = document.documentElement;
  const body = document.body;
  const $ = (id) => document.getElementById(id);
  const storage = {
    get(key) { try { return localStorage.getItem(key) === "1"; } catch (_) { return false; } },
    set(key, value) { try { localStorage.setItem(key, value ? "1" : "0"); } catch (_) {} }
  };

  const preferences = [
    ["contrast-toggle", "pd-contrast", "high-contrast"],
    ["font-toggle", "pd-font", "font-large", root],
    ["links-toggle", "pd-links", "links-underlined"],
    ["motion-toggle", "pd-motion", "reduce-motion"]
  ];

  function applyPreferences() {
    for (const [id, key, className, target = body] of preferences) {
      const active = storage.get(key);
      target.classList.toggle(className, active);
      const button = $(id);
      if (button) button.setAttribute("aria-pressed", String(active));
    }
  }

  for (const [id, key] of preferences) {
    $(id)?.addEventListener("click", () => {
      storage.set(key, !storage.get(key));
      applyPreferences();
    });
  }
  applyPreferences();

  const menuButton = $("menu-toggle");
  const navLinks = $("nav-links");
  function closeMenu() {
    if (!menuButton || !navLinks) return;
    navLinks.classList.remove("open");
    menuButton.setAttribute("aria-expanded", "false");
    body.classList.remove("no-scroll");
  }
  menuButton?.addEventListener("click", () => {
    const open = !navLinks.classList.contains("open");
    navLinks.classList.toggle("open", open);
    menuButton.setAttribute("aria-expanded", String(open));
    body.classList.toggle("no-scroll", open && matchMedia("(max-width: 840px)").matches);
  });
  navLinks?.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
  document.addEventListener("keydown", (event) => { if (event.key === "Escape") closeMenu(); });
  addEventListener("resize", () => { if (innerWidth > 840) closeMenu(); });

  // Filtros da página de dados abertos.
  const search = $("resource-search");
  const category = $("resource-category");
  const format = $("resource-format");
  const scope = $("resource-scope");
  const clear = $("resource-clear");
  const empty = $("resource-empty");
  const count = $("resource-count");

  function filterResources() {
    const query = (search?.value || "").trim().toLocaleLowerCase("pt-BR");
    const selectedCategory = category?.value || "";
    const selectedFormat = format?.value || "";
    const selectedScope = scope?.value || "";
    let shown = 0;

    document.querySelectorAll("#resource-list .resource-card").forEach((card) => {
      const ok = (!query || card.textContent.toLocaleLowerCase("pt-BR").includes(query))
        && (!selectedCategory || card.dataset.category === selectedCategory)
        && (!selectedFormat || (card.dataset.format || "").split(",").includes(selectedFormat))
        && (!selectedScope || card.dataset.scope === selectedScope);
      card.hidden = !ok;
      if (ok) shown += 1;
    });

    if (empty) empty.hidden = shown > 0;
    if (count) count.textContent = `${shown} recurso${shown === 1 ? "" : "s"} exibido${shown === 1 ? "" : "s"}`;
  }

  [search, category, format, scope].forEach((element) => {
    element?.addEventListener("input", filterResources);
    element?.addEventListener("change", filterResources);
  });
  clear?.addEventListener("click", () => {
    if (search) search.value = "";
    if (category) category.value = "";
    if (format) format.value = "";
    if (scope) scope.value = "";
    filterResources();
    search?.focus();
  });
  filterResources();

  // Abas genéricas do painel.
  const tabButtons = [...document.querySelectorAll("[data-panel-tab]")];
  const views = [...document.querySelectorAll("[data-panel-view]")];
  function activateTab(name, focus = false) {
    tabButtons.forEach((button) => {
      const active = button.dataset.panelTab === name;
      button.setAttribute("aria-selected", String(active));
      button.tabIndex = active ? 0 : -1;
      if (active && focus) button.focus();
    });
    views.forEach((view) => { view.hidden = view.dataset.panelView !== name; });
  }
  tabButtons.forEach((button, index) => {
    button.addEventListener("click", () => activateTab(button.dataset.panelTab));
    button.addEventListener("keydown", (event) => {
      if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
      event.preventDefault();
      let next = index;
      if (event.key === "ArrowLeft") next = (index - 1 + tabButtons.length) % tabButtons.length;
      if (event.key === "ArrowRight") next = (index + 1) % tabButtons.length;
      if (event.key === "Home") next = 0;
      if (event.key === "End") next = tabButtons.length - 1;
      activateTab(tabButtons[next].dataset.panelTab, true);
    });
  });
  if (tabButtons.length) activateTab(tabButtons.find((b) => b.getAttribute("aria-selected") === "true")?.dataset.panelTab || tabButtons[0].dataset.panelTab);
})();
