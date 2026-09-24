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
- Use the existing Tailwind utility vocabulary consistently. The Tailwind CDN compiler has been removed from every page: the utilities and the preflight reset now live at the top of `assets/site.css`, scoped with `:where(.ek-site)` so their specificity matches what the CDN produced. When you use a utility class that is not defined there yet, add its rule in that block; do not re-add `cdn.tailwindcss.com` and do not introduce another page-specific utility or reset strategy.
- Keep custom CSS in `assets/site.css` for reusable styles, site-wide components, and behavior that is awkward as inline utility classes.
- Keep custom JavaScript in `assets/site.js`; avoid inline scripts unless they are page metadata snippets already present, such as analytics or JSON-LD.
- Do not add npm dependencies, bundlers, or generated files without a clear user request.
- Keep changes scoped to the requested page or component. Avoid broad rewrites of duplicated headers, footers, or navigation unless the task is specifically to centralize or refactor them.

## Page Templates And Cross-Page Consistency

- Treat the existing page shell as a controlled template, not as optional example markup. New pages must reuse the same document structure, shared assets, header, navigation, language controls, footer, cookie banner, and script loading pattern as the closest existing page type.
- Use `articles/generative-ai-enterprise-safety-checklist.html` as the canonical template for every new Thai article. Use `en/articles/generative-ai-enterprise-safety-checklist.html` as the canonical English article template. Change article-specific metadata and content, but preserve the shared shell and component classes.
- For a new service or corporate page, start from the closest current page of the same type. Do not compose a new header, footer, language selector, cookie banner, or responsive navigation from memory.
- The desktop header must always contain the logo and these five navigation items in this order: Home, Expertise, Services, Insights, Contact. Only the current page may use the `active` class and `aria-current="page"`.
- The mobile menu must contain the same five navigation items in the same order and must retain `data-mobile-menu-button`, `aria-expanded`, `aria-controls="mobile-menu"`, and `data-mobile-menu`.
- Use `assets/logo.jpg` for root-page header logos and `../assets/logo.jpg` for pages one directory below the root. Keep the shared `brand-mark` class and do not add page-specific width, height, padding, or navigation-container overrides.
- Keep navigation dimensions and positioning in `assets/site.css`. New pages must not override `.ek-nav`, `.ek-nav > nav`, `.brand-mark`, `.max-w-7xl`, `[data-mobile-menu-button]`, or the global box-sizing/reset rules inline or in page-specific styles.
- Every page must reference the same current `assets/site.css` cache version. Never invent a different query-string version for one page. When `assets/site.css` changes, update the stylesheet cache version across every HTML file in the same change and verify there is exactly one version in use.
- Reuse the standard TH/EN selector in both desktop and mobile navigation. Root Thai pages link to `en/<page>.html`; English pages link back with `../<page>.html`; article pages must use their correct `articles/` and `en/articles/` relative paths.
- Every public page must include the standard footer with the company name, official LinkedIn and Facebook links, five site links, Cookie Policy, Bangkok address, office hours, telephone, and email.
- Every public page must include the standard cookie banner using `data-cookie-banner`, `data-cookie-accept`, and the correct relative link to `cookie-policy.html`.
- Every public page must include all three favicon declarations: `favicon-192.png`, `favicon-32.png`, and the Apple touch icon, with paths adjusted for the page directory. `favicon-master.png` is the 1254px source art only and must never be referenced from a page.
- Every article page must include LinkedIn, Facebook, and X share buttons above the article body. Every article card on both `insights.html` and `en/insights.html` must also include all three share buttons.
- Article cards must use the shared `article-card` and `share-button` classes. Do not add card-specific spacing that causes actions or share controls to shift vertically between cards.
- When adding an article, create or update the Thai and English article pair in the same task, add one card to both Insights pages, and add both canonical URLs to `sitemap.xml` with accurate `<lastmod>` values. Give every article pair one unique, semantically relevant 16:9 thumbnail from `images.unsplash.com`, reuse that same thumbnail in both language cards, and keep its descriptive `alt` text paired in Thai and English.
- On `insights.html` and `en/insights.html`, article cards belong only in the `data-insights-grid` inside the “All Articles” section. Never place an article card in the `insight-categories` section: that grid contains category overview links only.
- Preserve the newest-first behavior of the main Insights list. `assets/site.js` reverses the source cards in `data-insights-grid`, so append a new article card to the end of that source grid; it will display first in the browser.
- When a new article is added to the main Insights list, add its slug and category or categories to `articleCategories` in `assets/site.js`. Verify that the matching category filter displays the card on both Thai and English Insights pages.
- Preserve paired `data-th` and `data-en` content, translated ARIA labels, `hreflang`, canonical URLs, and language-specific visible text when copying a template.

## GitHub Publishing

- When the user asks to upload, publish, or push changes to GitHub, use the GitHub connector as the default publishing method.
- Do not rely on local `git push` for publication unless the user explicitly asks for it or the GitHub connector is unavailable.
- Before publishing, confirm the target branch and review the exact files being sent. Keep unrelated local changes out of the upload.
- After publishing through the connector, verify the target files on GitHub and report the branch or commit to the user.

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
- Keep analytics snippets intact unless the user asks to remove or change them. Analytics must stay behind the cookie-consent gate: copy the `let analyticsLoaded` block from `index.html` and never add a direct `<script src="https://www.googletagmanager.com/...">` tag.
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
  - Keep `datePublished`, `dateModified`, `author`, `publisher`, `mainEntityOfPage`, `image`, and `articleSection` accurate for articles. Article `author` is the Person node `https://www.ek.co.th/about.html#wasin-srisawat` (Wasin Srisawat, Consultant); `publisher` stays the organization.
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

Run `python3 tools/check-consistency.py` before every publish. It fails on a
mixed asset cache version, a missing cookie banner / favicon / skip link /
hreflang / canonical, analytics outside the consent gate, a re-added Tailwind
CDN tag, a utility class with no rule in `assets/site.css`, invalid JSON-LD, a
broken relative path, a missing `alt`, and unbalanced `data-th` / `data-en`.
The same script runs in CI via `.github/workflows/site-checks.yml`.

Then verify the change as a static site:

- Open the changed HTML file directly in a browser or serve the repository with a simple static server.
- Check at least one desktop width and one mobile width.
- Test the Thai/English language toggle on changed pages.
- Test the mobile menu if navigation changed.
- Test accordions, contact form status, cookie banner, and article/footer behavior if touched.
- Check browser console for JavaScript errors.
- Verify links and asset paths, especially for files under `articles/` where relative paths differ from root pages.
- Compare the new page against its canonical template before publishing. Confirm that only page-specific content, metadata, active navigation state, and relative paths differ.
- Confirm all HTML files reference one shared `site.css` cache version. A page-specific CSS version is a release-blocking consistency error.
- At a 1440px viewport, compare the header navigation bounding box with `index.html`, `about.html`, or the relevant language equivalent. Header height, container width, vertical position, logo position, and menu position must match.
- At a 390px viewport, confirm a 76px header, a stable logo position, and a fixed-width mobile menu button in the same position as existing pages.
- For every new article pair, verify exactly one cookie banner, three favicon declarations, four language buttons across desktop and mobile controls, one mobile-menu button, one mobile menu, three article share buttons, and one standard footer per file.
- On both Insights pages, verify that every `.article-card` contains exactly three `.share-button` links and that Thai and English card counts match.
- For each new article card on both Insights pages, verify all of the following before publishing: it appears exactly once in `data-insights-grid`, never appears in `insight-categories`, is appended as the final source card in `data-insights-grid`, has three share buttons, and is returned by its configured category filter. At the default view, confirm it renders as the first visible article after `assets/site.js` initializes.
- Parse every JSON-LD block as JSON and check all relative `href` and `src` targets before publishing.
- Run `git diff --check` and review the exact publication file list. Do not include unrelated changes.

## Common Pitfalls

- Do not change Thai copy without updating the paired English `data-en` copy, and vice versa.
- Do not use root-relative paths unless hosting is confirmed to serve from the domain root. Existing pages mainly use relative paths.
- Do not break article pages by using `assets/...` from inside `articles/`; use `../assets/...` where appropriate.
- Do not remove duplicate-looking header or footer markup casually. It is repeated across static pages by design.
- Do not replace Tailwind CDN usage with a local Tailwind build unless the user asks for that migration.
