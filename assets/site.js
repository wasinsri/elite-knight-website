const translations = document.querySelectorAll("[data-th][data-en]");
const ariaTranslations = document.querySelectorAll("[data-aria-th][data-aria-en]");
const titleTranslations = document.querySelectorAll("[data-title-th][data-title-en]");
const langButtons = document.querySelectorAll("[data-lang-button]");
const mobileMenuButton = document.querySelector("[data-mobile-menu-button]");
const mobileMenu = document.querySelector("[data-mobile-menu]");
const contactForm = document.querySelector("[data-contact-form]");
const contactStatus = document.querySelector("[data-contact-status]");
const cookieBanner = document.querySelector("[data-cookie-banner]");
const cookieAccept = document.querySelector("[data-cookie-accept]");
const accordionButtons = document.querySelectorAll("[data-accordion-button]");
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
        </div>
        <div class="grid gap-2 text-sm">
          <a href="../index.html">หน้าแรก</a>
          <a href="../about.html">ความเชี่ยวชาญ</a>
          <a href="../services.html">บริการ</a>
          <a href="../insights.html">คลังความรู้</a>
          <a href="../contact.html">ติดต่อเรา</a>
          <a href="../cookie-policy.html">นโยบายการใช้งานคุกกี้</a>
          <div class="mt-2 flex gap-3">
            <a class="social-icon" href="https://x.com/" target="_blank" rel="noopener" aria-label="Elite Knight on X">X</a>
            <a class="social-icon" href="https://www.facebook.com/" target="_blank" rel="noopener" aria-label="Elite Knight on Facebook">f</a>
            <a class="social-icon" href="https://www.linkedin.com/" target="_blank" rel="noopener" aria-label="Elite Knight on LinkedIn">in</a>
          </div>
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
  translations.forEach((node) => {
    node.innerHTML = node.dataset[selected];
  });
  ariaTranslations.forEach((node) => {
    node.setAttribute("aria-label", node.dataset[`aria${selected === "th" ? "Th" : "En"}`]);
  });
  titleTranslations.forEach((node) => {
    node.setAttribute("title", node.dataset[`title${selected === "th" ? "Th" : "En"}`]);
  });
  langButtons.forEach((button) => {
    const isActive = button.dataset.langButton === selected;
    button.classList.toggle("lang-active", isActive);
    button.classList.toggle("lang-inactive", !isActive);
    button.setAttribute("aria-pressed", String(isActive));
  });
  localStorage.setItem("ekLanguage", selected);
}

langButtons.forEach((button) => {
  button.addEventListener("click", () => applyLanguage(button.dataset.langButton));
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
  });
}

if (contactForm && contactStatus) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const lang = document.documentElement.lang === "en" ? "en" : "th";
    contactStatus.textContent = lang === "en"
      ? "Thank you. This static demo form is ready for integration with your preferred email or CRM system."
      : "ขอบคุณครับ แบบฟอร์มตัวอย่างนี้พร้อมเชื่อมต่อกับอีเมลหรือระบบ CRM ที่ต้องการ";
    contactStatus.focus();
    contactForm.reset();
  });
}

scheduleArticleFooter();
applyLanguage(localStorage.getItem("ekLanguage") || "th");
