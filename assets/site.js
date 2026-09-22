const translations = document.querySelectorAll("[data-th][data-en]");
const ariaTranslations = document.querySelectorAll("[data-aria-th][data-aria-en]");
const titleTranslations = document.querySelectorAll("[data-title-th][data-title-en]");
const placeholderTranslations = document.querySelectorAll("[data-placeholder-th][data-placeholder-en]");
const langButtons = document.querySelectorAll("[data-lang-button]");
const usesLanguageUrls = document.documentElement.dataset.languageRouting === "true";
const mobileMenuButton = document.querySelector("[data-mobile-menu-button]");
const mobileMenu = document.querySelector("[data-mobile-menu]");
const cookieBanner = document.querySelector("[data-cookie-banner]");
const cookieAccept = document.querySelector("[data-cookie-accept]");
const accordionButtons = document.querySelectorAll("[data-accordion-button]");
const insightSearch = document.querySelector("[data-insight-search]");
const insightFilterButtons = document.querySelectorAll("[data-insight-filter]");
const insightGrid = document.querySelector("[data-insights-grid]");
const insightResults = document.querySelector("[data-insight-results]");

const articleCategories = {
  "ai-transformation-use-case": ["data-ai"], "data-governance-ai": ["data-ai", "governance"],
  "generative-ai-enterprise-safety-checklist": ["data-ai", "governance"], "pdpa-generative-ai-enterprise": ["data-ai", "governance"],
  "ai-risk-assessment-use-case": ["data-ai", "governance"], "ai-governance-thailand-getting-started": ["data-ai", "governance"], "iso-iec-42001-ai-management-system": ["data-ai", "governance"],
  "third-party-cyber-risk-90-day-plan": ["cybersecurity"], "iso-27001-gap-assessment": ["cybersecurity", "governance"], "cyber-resilience-executive-metrics": ["cybersecurity"],
  "digital-trust-enterprise-services": ["cybersecurity", "digital-excellence"], "digital-strategy-to-portfolio": ["digital-excellence", "management-pmo"],
  "operating-model-strategy-execution": ["management-pmo"], "strategic-pmo-vs-traditional-pmo": ["management-pmo"]
  , "benefits-realization-pmo": ["management-pmo"], "digital-service-reliability": ["digital-excellence"], "customer-journey-operating-model": ["digital-excellence"]
};

function setInsightCategoryFromLink(card) {
  const link = card.querySelector(".article-title-link");
  const slug = link?.getAttribute("href")?.split("/").pop()?.replace(".html", "");
  return articleCategories[slug] || [];
}

function initializeInsights() {
  if (!insightGrid || !insightSearch || !insightResults) return;
  const cards = [...insightGrid.querySelectorAll(".article-card")].reverse();
  cards.forEach((card) => insightGrid.appendChild(card));
  const categoryPages = {
    "data-ai": "data-ai-insights.html",
    governance: "governance-insights.html",
    cybersecurity: "cybersecurity-insights.html",
    "digital-excellence": "digital-excellence-insights.html",
    "management-pmo": "management-pmo-insights.html"
  };
  const overviewLink = document.createElement("a");
  overviewLink.className = "mt-4 inline-flex font-bold text-teal-700 hover:text-teal-900";
  overviewLink.hidden = true;
  insightResults.insertAdjacentElement("afterend", overviewLink);
  let selectedCategory = new URLSearchParams(window.location.search).get("category") || "all";
  if (!articleCategories || !["all", ...Object.values(articleCategories).flat()].includes(selectedCategory)) selectedCategory = "all";
  const language = document.documentElement.lang === "en" ? "en" : "th";
  const update = () => {
    const term = insightSearch.value.trim().toLocaleLowerCase();
    let count = 0;
    cards.forEach((card, index) => {
      const matchesCategory = selectedCategory === "all" || setInsightCategoryFromLink(card).includes(selectedCategory);
      const matchesSearch = !term || card.textContent.toLocaleLowerCase().includes(term);
      const isLatestView = selectedCategory === "all" && !term;
      const visible = matchesCategory && matchesSearch && (!isLatestView || index < 15);
      card.hidden = !visible;
      if (visible) count += 1;
    });
    insightResults.textContent = language === "en" ? `${count} article${count === 1 ? "" : "s"} found` : `พบบทความ ${count} รายการ`;
    insightFilterButtons.forEach((button) => {
      const active = button.dataset.insightFilter === selectedCategory;
      button.setAttribute("aria-pressed", String(active));
      button.classList.toggle("bg-teal-700", active); button.classList.toggle("text-white", active);
      button.classList.toggle("border", !active); button.classList.toggle("border-slate-300", !active); button.classList.toggle("bg-white", !active); button.classList.toggle("text-slate-700", !active);
    });
    const categoryPage = categoryPages[selectedCategory];
    overviewLink.hidden = !categoryPage;
    if (categoryPage) {
      overviewLink.href = categoryPage;
      overviewLink.textContent = language === "en" ? "View category overview →" : "ดูภาพรวมหมวด →";
    }
  };
  insightSearch.addEventListener("input", update);
  insightFilterButtons.forEach((button) => button.addEventListener("click", () => { selectedCategory = button.dataset.insightFilter; const url = new URL(window.location); selectedCategory === "all" ? url.searchParams.delete("category") : url.searchParams.set("category", selectedCategory); window.history.replaceState({}, "", url); update(); }));
  update();
}
function ensureArticleFooter() {
  const isArticlePage = window.location.pathname.includes("/articles/") || window.location.pathname.includes("articles/");
  if (!isArticlePage || document.querySelector("footer")) return;

  const footer = document.createElement("footer");
  footer.className = "bg-slate-950 py-12 text-slate-300";
  footer.innerHTML = `
      <div class="mx-auto grid max-w-7xl gap-8 px-5 md:grid-cols-3 lg:px-8">
        <div>
          <div class="flex items-center gap-3">
            <img class="footer-mark" src="../assets/logo.jpg" alt="Elite Knight Co., Ltd. logo">
            <p class="text-lg font-black text-white">บริษัท เอลีท ไนท์ จำกัด</p>
          </div>
          <p class="mt-3 text-sm leading-6">Engineering the Future with Data and AI</p>
          <div class="mt-2 flex gap-3">
            <a class="social-icon" href="https://www.linkedin.com/company/elite-knight/" target="_blank" rel="noopener" aria-label="Elite Knight on LinkedIn">in</a>
            <a class="social-icon" href="https://www.facebook.com/ek.co.th" target="_blank" rel="noopener" aria-label="Elite Knight on Facebook">f</a>
          </div>
        </div>
        <div class="grid gap-2 text-sm">
          <a href="../index.html">หน้าแรก</a>
          <a href="../about.html">ความเชี่ยวชาญ</a>
          <a href="../services.html">บริการ</a>
          <a href="../insights.html">คลังความรู้</a>
          <a href="../contact.html">ติดต่อเรา</a>
          <a href="../cookie-policy.html">นโยบายการใช้งานคุกกี้</a>
        </div>
        <div class="text-sm leading-7">
          <p>เลขที่ 1/128 หมู่บ้านอิ่มอัมพร ซอยทวีวัฒนา 20 ถนนทวีวัฒนา แขวงศาลาธรรมสพน์ เขตทวีวัฒนา กรุงเทพมหานคร 10170</p>
          <p>เปิดบริการ: จันทร์ - ศุกร์ 9.00 - 17.30 น.</p>
          <p>Mobile: 063-664-1555</p>
          <p>Email: info@ek.co.th</p>
        </div>
      </div>
  `;
  const siteScript = document.querySelector("script[src*='site.js']");
  if (siteScript && siteScript.parentNode === document.body) {
    document.body.insertBefore(footer, siteScript);
  } else {
    document.body.appendChild(footer);
  }
}

function scheduleArticleFooter() {
  ensureArticleFooter();
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", ensureArticleFooter, { once: true });
  }
  window.addEventListener("load", ensureArticleFooter, { once: true });
  setTimeout(ensureArticleFooter, 250);
  setTimeout(ensureArticleFooter, 1000);
}

function applyLanguage(lang) {
  const selected = lang === "en" ? "en" : "th";
  document.documentElement.lang = selected;
  // Localized pages already contain their language in HTML, including local links.
  // Keep the in-place switch only for the standalone design preview.
  if (!usesLanguageUrls) {
    translations.forEach((node) => {
      node.innerHTML = node.dataset[selected];
    });
    ariaTranslations.forEach((node) => {
      node.setAttribute("aria-label", node.dataset[`aria${selected === "th" ? "Th" : "En"}`]);
    });
    titleTranslations.forEach((node) => {
      node.setAttribute("title", node.dataset[`title${selected === "th" ? "Th" : "En"}`]);
    });
    placeholderTranslations.forEach((node) => {
      node.setAttribute("placeholder", node.dataset[`placeholder${selected === "th" ? "Th" : "En"}`]);
    });
  }
  langButtons.forEach((button) => {
    const isActive = button.dataset.langButton === selected;
    button.classList.toggle("lang-active", isActive);
    button.classList.toggle("lang-inactive", !isActive);
    if (button.tagName === "A") {
      if (isActive) button.setAttribute("aria-current", "page");
      else button.removeAttribute("aria-current");
    } else {
      button.setAttribute("aria-pressed", String(isActive));
    }
  });
  localStorage.setItem("ekLanguage", selected);
}

langButtons.forEach((button) => {
  if (!usesLanguageUrls) {
    button.addEventListener("click", () => applyLanguage(button.dataset.langButton));
  }
});

if (mobileMenuButton && mobileMenu) {
  mobileMenuButton.addEventListener("click", () => {
    const isOpen = mobileMenu.classList.toggle("hidden") === false;
    mobileMenuButton.setAttribute("aria-expanded", String(isOpen));
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !mobileMenu.classList.contains("hidden")) {
      mobileMenu.classList.add("hidden");
      mobileMenuButton.setAttribute("aria-expanded", "false");
      mobileMenuButton.focus();
    }
  });
}

accordionButtons.forEach((button) => {
  const panel = document.getElementById(button.getAttribute("aria-controls"));
  if (!panel) return;
  button.addEventListener("click", () => {
    const expanded = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!expanded));
    panel.hidden = expanded;
  });
});

if (cookieBanner && cookieAccept) {
  const hasConsent = localStorage.getItem("ekCookieConsent") === "accepted";
  cookieBanner.hidden = hasConsent;
  cookieAccept.addEventListener("click", () => {
    localStorage.setItem("ekCookieConsent", "accepted");
    cookieBanner.hidden = true;
    window.dispatchEvent(new Event("ek:cookie-consent"));
  });
}

scheduleArticleFooter();
applyLanguage(usesLanguageUrls ? document.documentElement.lang : localStorage.getItem("ekLanguage") || "th");
initializeInsights();
