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

applyLanguage(localStorage.getItem("ekLanguage") || "th");
