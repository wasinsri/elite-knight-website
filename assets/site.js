const translations = document.querySelectorAll("[data-th][data-en]");
const ariaTranslations = document.querySelectorAll("[data-aria-th][data-aria-en]");
const titleTranslations = document.querySelectorAll("[data-title-th][data-title-en]");
const langButtons = document.querySelectorAll("[data-lang-button]");
const usesLanguageUrls = document.documentElement.dataset.languageRouting === "true";
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

if (contactForm && contactStatus) {
  contactForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const lang = document.documentElement.lang === "en" ? "en" : "th";
    const endpoint = contactForm.dataset.contactEndpoint;
    if (!endpoint) {
      contactStatus.textContent = lang === "en"
        ? "The contact form is not connected yet. Please email info@ek.co.th or call 063-664-1555."
        : "แบบฟอร์มยังไม่ได้เชื่อมต่อ กรุณาอีเมล info@ek.co.th หรือโทร 063-664-1555";
      contactStatus.focus();
      return;
    }

    const submitButton = contactForm.querySelector("button[type='submit']");
    if (submitButton) submitButton.disabled = true;
    contactStatus.textContent = lang === "en" ? "Sending..." : "กำลังส่งข้อความ...";
    contactStatus.focus();

    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify(Object.fromEntries(new FormData(contactForm)))
      });
      if (!response.ok) throw new Error("Contact form submission failed");
      contactStatus.textContent = lang === "en"
        ? "Thank you. Your message has been sent to Elite Knight."
        : "ขอบคุณครับ ส่งข้อความถึงทีม Elite Knight เรียบร้อยแล้ว";
      contactForm.reset();
    } catch (error) {
      contactStatus.textContent = lang === "en"
        ? "Sorry, the message could not be sent. Please email info@ek.co.th or call 063-664-1555."
        : "ขออภัยครับ ส่งข้อความไม่สำเร็จ กรุณาอีเมล info@ek.co.th หรือโทร 063-664-1555";
    } finally {
      if (window.turnstile) window.turnstile.reset();
      if (submitButton) submitButton.disabled = false;
    }
  });
}

scheduleArticleFooter();
applyLanguage(usesLanguageUrls ? document.documentElement.lang : localStorage.getItem("ekLanguage") || "th");
