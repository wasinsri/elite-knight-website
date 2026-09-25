const translations = document.querySelectorAll("[data-th][data-en]");
const ariaTranslations = document.querySelectorAll("[data-aria-th][data-aria-en]");
const titleTranslations = document.querySelectorAll("[data-title-th][data-title-en]");
const placeholderTranslations = document.querySelectorAll("[data-placeholder-th][data-placeholder-en]");
const altTranslations = document.querySelectorAll("[data-alt-th][data-alt-en]");
const langButtons = document.querySelectorAll("[data-lang-button]");
const usesLanguageUrls = document.documentElement.dataset.languageRouting === "true";
const mobileMenuButton = document.querySelector("[data-mobile-menu-button]");
const mobileMenu = document.querySelector("[data-mobile-menu]");
const cookieBanner = document.querySelector("[data-cookie-banner]");
const cookieAccept = document.querySelector("[data-cookie-accept]");
const cookieDecline = document.querySelector("[data-cookie-decline]");
const accordionButtons = document.querySelectorAll("[data-accordion-button]");
const insightSearch = document.querySelector("[data-insight-search]");
const insightFilterButtons = document.querySelectorAll("[data-insight-filter]");
const insightGrid = document.querySelector("[data-insights-grid]");
const insightResults = document.querySelector("[data-insight-results]");
const insightSectionKicker = document.querySelector('section[aria-labelledby="article-list"] .section-kicker');

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

function initializeArticleCardActions() {
  document.querySelectorAll(".article-card").forEach((card) => {
    const cardBody = card.querySelector(".article-title-link")?.closest("h3")?.parentElement;
    const readLink = cardBody?.querySelector(":scope > a.inline-flex");
    const shareLinks = readLink?.nextElementSibling;
    if (!readLink || !shareLinks?.querySelector(".share-button")) return;
    const actions = document.createElement("div");
    actions.className = "article-card-actions";
    readLink.before(actions);
    actions.append(readLink, shareLinks);
    readLink.textContent = document.documentElement.lang === "en" ? "Read article" : "อ่านบทความ";
  });
}

function initializeInsights() {
  if (!insightGrid || !insightSearch || !insightResults) return;
  const cards = [...insightGrid.querySelectorAll(".article-card")].reverse();
  cards.forEach((card) => insightGrid.appendChild(card));
  const latestLimit = 15;
  let showAllLatest = false;
  const insightCategories = document.getElementById("insight-categories");
  let showAllButton = document.querySelector("[data-insights-show-all]");
  if (!showAllButton) {
    showAllButton = document.createElement("button");
    showAllButton.type = "button";
    showAllButton.className = "mt-10 inline-flex rounded bg-teal-700 px-5 py-3 font-bold text-white hover:bg-teal-900 focus:outline-none focus:ring-2 focus:ring-teal-200";
    showAllButton.hidden = true;
    insightGrid.insertAdjacentElement("afterend", showAllButton);
  }
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
      const visible = matchesCategory && matchesSearch && (!isLatestView || showAllLatest || index < latestLimit);
      card.hidden = !visible;
      if (visible) count += 1;
    });
    if (insightSectionKicker) {
      insightSectionKicker.textContent = language === "en" ? "Latest 15 Articles" : "บทความล่าสุด 15 เรื่อง";
    }
    insightResults.textContent = language === "en" ? `${count} article${count === 1 ? "" : "s"} found` : `พบบทความ ${count} รายการ`;
    showAllButton.hidden = !isLatestView || showAllLatest || cards.length <= latestLimit;
    showAllButton.textContent = language === "en" ? "View all articles" : "ดูบทความทั้งหมด";
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
  showAllButton.addEventListener("click", () => {
    showAllLatest = true;
    update();
    insightCategories?.scrollIntoView({
      behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth",
      block: "start"
    });
  });
  insightFilterButtons.forEach((button) => button.addEventListener("click", () => { selectedCategory = button.dataset.insightFilter; showAllLatest = false; const url = new URL(window.location); selectedCategory === "all" ? url.searchParams.delete("category") : url.searchParams.set("category", selectedCategory); window.history.replaceState({}, "", url); update(); }));
  update();
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
    altTranslations.forEach((node) => {
      node.setAttribute("alt", node.dataset[`alt${selected === "en" ? "En" : "Th"}`]);
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

const serviceIcons = {
  "service-panel-1": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" focusable="false"><path d="M4 7c0-1.7 3.6-3 8-3s8 1.3 8 3-3.6 3-8 3-8-1.3-8-3Z"/><path d="M4 7v10c0 1.7 3.6 3 8 3s8-1.3 8-3V7"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/></svg>',
  "service-panel-2": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" focusable="false"><path d="M12 3 5 6v5.5c0 4 3 7.7 7 9.5 4-1.8 7-5.5 7-9.5V6l-7-3Z"/><path d="m9.2 11.8 2 2 3.6-3.6"/></svg>',
  "service-panel-3": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" focusable="false"><path d="M3 17.5 9 11l4 4 8-8.5"/><path d="M15 6.5h6v6"/><path d="M3 21h18"/></svg>',
  "service-panel-4": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" focusable="false"><circle cx="9" cy="7.5" r="3"/><path d="M3 20v-1.5C3 16 5.7 14 9 14s6 2 6 4.5V20"/><path d="M16.5 10.5a2.5 2.5 0 1 0 0-5"/><path d="M17.5 14c2.1.5 3.5 2.1 3.5 4v2"/></svg>',
  "service-panel-5": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" focusable="false"><circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/></svg>'
};

accordionButtons.forEach((button) => {
  const icon = serviceIcons[button.getAttribute("aria-controls")];
  if (icon) {
    const iconMarkup = `<span class="ek-service-icon" aria-hidden="true">${icon}</span>`;
    const existingIcon = button.querySelector("svg");
    if (existingIcon) {
      existingIcon.closest("span")?.replaceWith(document.createRange().createContextualFragment(iconMarkup));
    } else {
      button.insertAdjacentHTML("afterbegin", iconMarkup);
    }
  }
  const panel = document.getElementById(button.getAttribute("aria-controls"));
  if (!panel) return;
  button.addEventListener("click", () => {
    const expanded = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!expanded));
    panel.hidden = expanded;
  });
});

if (cookieBanner && cookieAccept) {
  const stored = localStorage.getItem("ekCookieConsent");
  const lastFocus = () => (document.activeElement instanceof HTMLElement ? document.activeElement : null);
  cookieBanner.hidden = stored === "accepted" || stored === "declined";
  const closeBanner = (choice) => {
    localStorage.setItem("ekCookieConsent", choice);
    cookieBanner.hidden = true;
    if (choice === "accepted") window.dispatchEvent(new Event("ek:cookie-consent"));
  };
  cookieAccept.addEventListener("click", () => closeBanner("accepted"));
  if (cookieDecline) cookieDecline.addEventListener("click", () => closeBanner("declined"));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !cookieBanner.hidden) {
      const focused = lastFocus();
      closeBanner("declined");
      if (focused && cookieBanner.contains(focused)) document.body.focus();
    }
  });
}

applyLanguage(usesLanguageUrls ? document.documentElement.lang : localStorage.getItem("ekLanguage") || "th");
initializeArticleCardActions();
initializeInsights();

/* Conversion tracking. Events only reach GA4 after the visitor accepts cookies,
   because window.gtag is created by the consent-gated loader in each page head. */
function ekTrack(name, params) {
  if (typeof window.gtag !== "function") return;
  window.gtag("event", name, params || {});
}

document.addEventListener("click", (event) => {
  const link = event.target.closest && event.target.closest("a[href]");
  if (!link) return;
  const href = link.getAttribute("href") || "";
  if (href.startsWith("mailto:")) {
    ekTrack("contact_email_click", { link_url: href, page_path: location.pathname });
  } else if (href.startsWith("tel:")) {
    ekTrack("contact_phone_click", { link_url: href, page_path: location.pathname });
  } else if (link.classList.contains("share-button")) {
    ekTrack("article_share", { method: link.dataset.shareNetwork || link.hostname, page_path: location.pathname });
  }
});

if (document.body.classList.contains("ek-article")) {
  const marks = [25, 50, 75, 100];
  const fired = new Set();
  const onScroll = () => {
    const doc = document.documentElement;
    const max = doc.scrollHeight - window.innerHeight;
    if (max <= 0) return;
    const pct = Math.min(100, Math.round((window.scrollY / max) * 100));
    marks.forEach((mark) => {
      if (pct >= mark && !fired.has(mark)) {
        fired.add(mark);
        ekTrack("article_scroll", { percent_scrolled: mark, page_path: location.pathname });
      }
    });
    if (fired.size === marks.length) window.removeEventListener("scroll", onScroll);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
}

/* Contact form.
   No delivery endpoint is wired yet: set data-endpoint="<url>" on the <form>
   once the provider is chosen and the POST below starts running. Until then the
   form validates fully and tells the visitor to use phone or email. */
const contactForm = document.querySelector("[data-contact-form]");

if (contactForm) {
  const status = contactForm.querySelector("[data-form-status]");
  const isEnglish = document.documentElement.lang === "en";
  const say = (th, en) => (isEnglish ? en : th);

  const messages = {
    required: say("กรุณากรอกข้อมูลในช่องนี้", "This field is required."),
    email: say("กรุณากรอกอีเมลให้ถูกต้อง เช่น name@company.com", "Enter a valid email address, for example name@company.com."),
    topic: say("กรุณาเลือกหัวข้อที่สนใจ", "Please choose a topic."),
    consent: say("กรุณายืนยันความยินยอมก่อนส่งข้อมูล", "Please confirm your consent before sending."),
    short: say("กรุณาอธิบายเพิ่มอีกเล็กน้อย (อย่างน้อย 10 ตัวอักษร)", "Please add a little more detail (at least 10 characters)."),
    summary: say("ยังกรอกข้อมูลไม่ครบ กรุณาตรวจสอบช่องที่แจ้งไว้ด้านบน", "Some details are missing. Please check the fields flagged above."),
    pending: say(
      "ระบบส่งฟอร์มยังไม่เปิดใช้งาน ระหว่างนี้กรุณาติดต่อเราที่ 063-664-1555 หรือ info@ek.co.th ข้อมูลที่กรอกไว้ยังอยู่ในหน้านี้",
      "Form delivery is not connected yet. In the meantime please reach us on 063-664-1555 or info@ek.co.th. Your answers are still on this page."
    )
  };

  const errorNodeFor = (field) => contactForm.querySelector(`[data-error-for="${field.id}"]`);

  const setError = (field, message) => {
    const node = errorNodeFor(field);
    if (node) node.textContent = message || "";
    if (message) field.setAttribute("aria-invalid", "true");
    else field.removeAttribute("aria-invalid");
  };

  const validate = (field) => {
    const value = field.type === "checkbox" ? field.checked : field.value.trim();
    if (field.type === "checkbox") return value ? "" : messages.consent;
    if (!value) return field.tagName === "SELECT" ? messages.topic : messages.required;
    if (field.type === "email" && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) return messages.email;
    if (field.tagName === "TEXTAREA" && value.length < 10) return messages.short;
    return "";
  };

  const fields = [...contactForm.querySelectorAll("input[required], select[required], textarea[required]")];

  fields.forEach((field) => {
    field.addEventListener("blur", () => setError(field, validate(field)));
    field.addEventListener("input", () => {
      if (field.getAttribute("aria-invalid") === "true") setError(field, validate(field));
    });
  });

  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();
    let firstInvalid = null;
    fields.forEach((field) => {
      const message = validate(field);
      setError(field, message);
      if (message && !firstInvalid) firstInvalid = field;
    });

    if (firstInvalid) {
      status.dataset.state = "error";
      status.textContent = messages.summary;
      firstInvalid.focus();
      return;
    }

    const endpoint = contactForm.dataset.endpoint;
    if (!endpoint) {
      status.dataset.state = "pending";
      status.textContent = messages.pending;
      ekTrack("contact_form_submit_blocked", { reason: "no_endpoint", page_path: location.pathname });
      return;
    }

    status.dataset.state = "pending";
    status.textContent = say("กำลังส่งข้อมูล...", "Sending...");
    fetch(endpoint, {
      method: "POST",
      headers: { Accept: "application/json" },
      body: new FormData(contactForm)
    })
      .then((response) => {
        if (!response.ok) throw new Error(String(response.status));
        contactForm.reset();
        status.dataset.state = "success";
        status.textContent = say(
          "ขอบคุณครับ เราได้รับข้อความของคุณแล้ว ทีมงานจะติดต่อกลับภายในวันทำการถัดไป",
          "Thank you. We have your message and will reply within the next business day."
        );
        ekTrack("contact_form_submit", { page_path: location.pathname });
      })
      .catch(() => {
        status.dataset.state = "error";
        status.textContent = say(
          "ส่งข้อมูลไม่สำเร็จ กรุณาลองใหม่อีกครั้ง หรือติดต่อเราที่ 063-664-1555",
          "We could not send that. Please try again or call us on 063-664-1555."
        );
      });
  });
}
