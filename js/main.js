/* All content is readable without JavaScript; this adds progressive enhancements. */
"use strict";
document.documentElement.classList.add("js");

const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector("#main-navigation");
function closeMenu(returnFocus = false) {
  if (!menuButton || !navigation) return;
  const wasOpen = menuButton.getAttribute("aria-expanded") === "true";
  menuButton.setAttribute("aria-expanded", "false");
  menuButton.textContent = "Menu";
  navigation.classList.remove("is-open");
  document.body.classList.remove("menu-open");
  if (returnFocus && wasOpen) menuButton.focus();
}
menuButton?.addEventListener("click", () => {
  const open = menuButton.getAttribute("aria-expanded") !== "true";
  menuButton.setAttribute("aria-expanded", String(open));
  menuButton.textContent = open ? "Close" : "Menu";
  navigation.classList.toggle("is-open", open);
  document.body.classList.toggle("menu-open", open);
});
document.addEventListener("keydown", event => { if (event.key === "Escape") closeMenu(true); });
navigation?.addEventListener("click", event => { if (event.target.closest("a")) closeMenu(); });
document.addEventListener("click", event => { if (!event.target.closest(".site-header")) closeMenu(); });
document.addEventListener("focusin", event => { if (!event.target.closest(".site-header")) closeMenu(); });
window.matchMedia("(min-width: 851px)").addEventListener("change", event => { if (event.matches) closeMenu(); });
document.querySelectorAll("[data-current-year]").forEach(el => { el.textContent = new Date().getFullYear(); });

const stages = {
  sense: {title: "01 / SENSING", text: "Embedded sensors capture the physical world: strain, temperature, geometry, and motion.", color: "#53e3d1"},
  model: {title: "02 / INTELLIGENCE", text: "Digital twins connect measurements to physics-based models for real-time structural validation.", color: "#8ca6ff"},
  adapt: {title: "03 / AUTONOMY", text: "Control and adaptive decision-making turn system knowledge into actions that improve production.", color: "#f7c556"}
};
document.querySelectorAll("[data-stage]").forEach(button => {
  button.addEventListener("click", () => {
    const stage = stages[button.dataset.stage];
    document.querySelectorAll("[data-stage]").forEach(el => el.setAttribute("aria-pressed", String(el === button)));
    document.querySelector("#workflow-description").textContent = stage.text;
    document.querySelector("#workflow-label").textContent = stage.title;
    document.querySelector(".workflow-explorer")?.style.setProperty("--stage-color", stage.color);
  });
});

const search = document.querySelector("#publication-search");
if (search) {
  const yearSelect = document.querySelector("#publication-year");
  const cards = [...document.querySelectorAll(".publication")];
  const filterButtons = [...document.querySelectorAll("[data-filter]")];
  const normalize = text => text.normalize("NFKD").replace(/[\u0300-\u036f]/g, "").toLocaleLowerCase();
  const searchable = cards.map(card => normalize(card.textContent));
  let activeType = "all";
  function filterPublications() {
    const terms = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    let count = 0;
    cards.forEach((card, index) => {
      const show = (activeType === "all" || card.dataset.type === activeType)
        && (yearSelect.value === "all" || card.dataset.year === yearSelect.value)
        && terms.every(term => searchable[index].includes(term));
      card.hidden = !show;
      if (show) count++;
    });
    document.querySelector("#publication-status").textContent = activeType === "all" && yearSelect.value === "all" && !search.value.trim() ? "All publications" : "Filtered publications";
    document.querySelector("#publication-empty").hidden = count !== 0;
    filterButtons.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.filter === activeType)));
    document.querySelector("#clear-filters").hidden = activeType === "all" && yearSelect.value === "all" && !search.value;
  }
  function resetFilters() { search.value = ""; yearSelect.value = "all"; activeType = "all"; filterPublications(); }
  search.addEventListener("input", filterPublications);
  yearSelect.addEventListener("change", filterPublications);
  filterButtons.forEach(button => button.addEventListener("click", () => { activeType = button.dataset.filter; filterPublications(); }));
  document.querySelector("#clear-filters").addEventListener("click", () => { resetFilters(); search.focus(); });
  function revealLinkedPublication() {
    const target = document.getElementById(location.hash.slice(1));
    if (target?.classList.contains("publication")) { resetFilters(); requestAnimationFrame(() => target.scrollIntoView()); }
  }
  window.addEventListener("hashchange", revealLinkedPublication);
  filterPublications();
  if (location.hash) revealLinkedPublication();
}

let toastTimer;
const toast = document.querySelector("#toast");
function showToast(message) {
  if (!toast) return;
  clearTimeout(toastTimer);
  toast.textContent = message;
  toast.hidden = false;
  toastTimer = setTimeout(() => { toast.hidden = true; }, 3500);
}
const citationDialog = document.querySelector("#citation-dialog");
document.querySelectorAll(".copy-citation").forEach(button => {
  button.addEventListener("click", async () => {
    const citation = button.dataset.citation;
    try {
      if (!navigator.clipboard?.writeText) throw new Error("Clipboard unavailable");
      await navigator.clipboard.writeText(citation);
      showToast("Citation copied.");
    } catch {
      const field = document.querySelector("#citation-text");
      field.value = citation;
      citationDialog.showModal();
      field.focus();
      field.select();
    }
  });
});
document.querySelector("#close-citation")?.addEventListener("click", () => citationDialog.close());

// Real research figures can be opened at reading size. Links still work without JS.
const figureDialog = document.querySelector("#figure-dialog");
document.querySelectorAll(".figure-open").forEach(link => {
  const img = link.querySelector("img");
  const showFallback = () => {
    link.hidden = true;
    link.parentElement.querySelector(".figure-load-error").hidden = false;
  };
  img.addEventListener("error", showFallback);
  if (img.complete && img.naturalWidth === 0) showFallback();
  link.addEventListener("click", event => {
    if (!figureDialog || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    const dialogImage = document.querySelector("#figure-dialog-image");
    dialogImage.src = link.dataset.figure;
    dialogImage.alt = link.dataset.caption;
    document.querySelector("#figure-dialog-caption").textContent = link.dataset.caption;
    document.querySelector("#figure-dialog-source").href = link.dataset.source || link.href;
    figureDialog.showModal();
  });
});
document.querySelector(".figure-close")?.addEventListener("click", () => figureDialog.close());
figureDialog?.addEventListener("click", event => {
  if (event.target === figureDialog) {
    const box = figureDialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) figureDialog.close();
  }
});
