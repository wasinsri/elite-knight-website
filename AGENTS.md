# Project Instructions

This repository is the static website for Elite Knight Co., Ltd. It is a multi-page corporate consulting site for Data, AI, Cybersecurity, Digital Excellence, Management Consulting, and Strategic PMO services.

GitHub repository: `wasinsri/elite-knight-website`
GitHub URL: `https://github.com/wasinsri/elite-knight-website`

## Project Shape

- This is a static HTML/CSS/JavaScript site. There is no `package.json`, build step, or frontend framework checked in.
- Main pages include `index.html`, `about.html`, `services.html`, `insights.html`, `contact.html`, and `cookie-policy.html`.
- Shared styling lives in `assets/site.css`.
- Shared browser behavior lives in `assets/site.js`.
- Shared imagery and brand assets live under `assets/`, especially `assets/logo.jpg`.
- Article pages live under `articles/` and should keep relative links working from that subdirectory.

## Development Rules

- Preserve the static-site architecture unless the user explicitly asks for a framework or build system.
- Prefer editing existing HTML, `assets/site.css`, and `assets/site.js` directly.
- Use Tailwind utility classes consistently because pages currently load Tailwind from the CDN.
- Keep custom CSS in `assets/site.css` for reusable styles, site-wide components, and behavior that is awkward as inline utility classes.
- Keep custom JavaScript in `assets/site.js`; avoid inline scripts unless they are page metadata snippets already present, such as analytics or JSON-LD.
- Do not add npm dependencies, bundlers, or generated files without a clear user request.
- Keep changes scoped to the requested page or component. Avoid broad rewrites of duplicated headers, footers, or navigation unless the task is specifically to centralize or refactor them.

## Language And Content

- The default document language is Thai (`lang="th"`).
- Many user-facing text nodes use paired `data-th` and `data-en` attributes. When adding or changing visible copy, update both Thai and English values.
- For translated ARIA labels, keep paired `data-aria-th` and `data-aria-en` values.
- For translated title attributes, keep paired `data-title-th` and `data-title-en` values.
- Preserve the language switcher behavior in `assets/site.js`; it reads these data attributes and stores the selected language in `localStorage` as `ekLanguage`.
- Preserve the company positioning and terminology: Data, AI, Governance, Cybersecurity, Digital Trust, Digital Excellence, Management Consulting, Strategic PMO, and enterprise consulting.
- Keep contact details consistent unless the user explicitly changes them: Mobile `063-664-1555`, email `info@ek.co.th`, and the Bangkok address already used across the site.

## Design And UX

- Keep the visual direction professional, enterprise-grade, and restrained.
- Continue using the existing teal, slate, white, and soft neutral palette.
- Maintain responsive behavior for desktop and mobile, especially the sticky navigation, mobile menu, hero sections, card grids, accordions, contact form, article cards, and cookie banner.
- Keep cards and panels simple with modest radius and clear spacing.
- Do not introduce decorative visual styles that conflict with the current consulting/technology brand.
- Use real, semantically relevant imagery for hero or article visuals when imagery is needed. Avoid abstract filler images when the subject should be inspectable.

## Accessibility

- Preserve the skip link to `#main-content` and keep `main` focusable with `tabindex="-1"`.
- Keep nav buttons, accordions, language controls, forms, and cookie controls keyboard-accessible.
- Maintain accurate `aria-expanded`, `aria-controls`, `aria-label`, `role`, and `aria-live` attributes when changing interactive UI.
- Ensure images have meaningful `alt` text unless decorative.
- Preserve visible focus styles in `assets/site.css`.
- Respect reduced-motion handling already defined in CSS.

## SEO, Metadata, And Compliance

- Keep page-specific `<title>`, meta description, canonical URL, Open Graph, Twitter card, and favicon metadata aligned with the page content.
- Preserve JSON-LD structured data where present and update it when business contact or organization details change.
- Keep analytics snippets intact unless the user asks to remove or change them.
- Keep cookie notice and cookie policy behavior consistent with `ekCookieConsent` in `localStorage`.
- When adding new pages, include suitable metadata, navigation links if needed, footer links if needed, and language pairs for visible copy.

## SEO And AI SEO Strategy

- Treat SEO and AI SEO as first-class requirements for every content or page change.
- Keep each page focused on one clear search intent and entity. Page titles should combine the topic, consulting category, market where useful, and brand name without keyword stuffing.
- Write meta descriptions that state the service or article topic, audience, business outcome, and Thailand/Bangkok context when relevant.
- Maintain entity consistency across all pages: `Elite Knight Co., Ltd.`, `บริษัท เอลีท ไนท์ จำกัด`, Mobile `063-664-1555`, email `info@ek.co.th`, address, and the positioning around Data, AI, Governance, Cybersecurity, Digital Trust, Digital Excellence, Management Consulting, Strategic PMO, and enterprise consulting.
- Use structured data for machine-readable clarity:
  - Home and contact pages should include `ProfessionalService` or `Organization` style data with logo, contact details, area served, expertise, and business description.
  - Service landing pages should include `Service`, `FAQPage`, and `BreadcrumbList`.
  - Article pages should include `BlogPosting` or `Article`, `FAQPage` where relevant, and `BreadcrumbList`.
  - Keep `datePublished`, `dateModified`, `author`, `publisher`, `mainEntityOfPage`, `image`, and `articleSection` accurate for articles.
- Do not include placeholder social profile links in `sameAs` or footers. Only use real official profile URLs; otherwise omit them.
- Keep `sitemap.xml` current whenever pages are added, removed, renamed, or materially updated. Include `<lastmod>` dates.
- Build internal links intentionally:
  - Service pages should link to relevant insights and contact.
  - Articles should link back to the most relevant service page.
  - The home page and services overview should link to dedicated service landing pages.
- Support answer-engine and LLM discovery by adding concise, visible FAQ sections, definition-style summaries, “who this is for” sections, business outcomes, and delivery/advisory language that can be quoted or summarized cleanly.
- Prefer concrete consulting terms that match buyer intent: `AI consulting`, `Data Governance`, `AI Governance`, `Digital Transformation Consulting`, `Cybersecurity Consulting`, `Strategic PMO`, `Portfolio Management`, `Management Consulting`, `ISO/IEC 42001`, `ISO/IEC 27001`, `NIST`, `COBIT`, and `ITIL`.
- Avoid thin landing pages. Each service page should explain the problem, expected outcomes, fit, related frameworks or capabilities, FAQ, and next-step CTA.
- For bilingual content, visible Thai and English copy should remain paired through `data-th` and `data-en` when the page uses the language switcher. If a separate English URL structure is introduced later, add `hreflang` and keep Thai/English canonical relationships correct.

## Verification

Because there is no build system, verify changes as a static site:

- Open the changed HTML file directly in a browser or serve the repository with a simple static server.
- Check at least one desktop width and one mobile width.
- Test the Thai/English language toggle on changed pages.
- Test the mobile menu if navigation changed.
- Test accordions, contact form status, cookie banner, and article/footer behavior if touched.
- Check browser console for JavaScript errors.
- Verify links and asset paths, especially for files under `articles/` where relative paths differ from root pages.

## Common Pitfalls

- Do not change Thai copy without updating the paired English `data-en` copy, and vice versa.
- Do not use root-relative paths unless hosting is confirmed to serve from the domain root. Existing pages mainly use relative paths.
- Do not break article pages by using `assets/...` from inside `articles/`; use `../assets/...` where appropriate.
- Do not remove duplicate-looking header or footer markup casually. It is repeated across static pages by design.
- Do not replace Tailwind CDN usage with a local Tailwind build unless the user asks for that migration.
