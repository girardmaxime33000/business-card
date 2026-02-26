# CLAUDE.md — AI Assistant Guide for `business-card`

## Project Overview

Personal portfolio / business card website for **Maxime Girard**, a Director of Marketing & Growth professional. The site showcases 10+ years of B2B/B2B2C experience with a modern, dark-themed design.

**Live-ready:** No build step — open `index.html` directly in a browser.

---

## Repository Structure

```
business-card/
└── index.html   # Single file: all HTML, CSS, and JavaScript (≈1 100 lines)
```

No `package.json`, no framework, no build tools.

---

## Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Markup     | HTML5 (semantic elements)           |
| Styling    | Pure CSS3 — variables, grid, flex, keyframes |
| Scripting  | Vanilla JS (Intersection Observer)  |
| Fonts      | Google Fonts — Syne + DM Sans       |
| Dev tools  | None required                       |

---

## Running the Project

```bash
# Option 1 — directly in the browser
open index.html          # macOS
xdg-open index.html      # Linux

# Option 2 — lightweight local server (optional)
python3 -m http.server 8080
# then visit http://localhost:8080
```

No installation, no `npm install`, no compilation.

---

## Page Sections

The site is structured as a single scrolling page with these anchor sections:

| Section ID        | Content                                         |
|-------------------|-------------------------------------------------|
| *(hero)*          | Name, title, animated availability tag, metrics |
| `#profil`         | Professional pitch + 3 value cards              |
| `#experiences`    | Timeline of 6 positions with results            |
| `#cas-usage`      | 3 project case studies (AI/Growth focus)        |
| `#competences`    | Skill groups (strategy, growth, data, AI, dev)  |
| `#references`     | 4 testimonial quotes                            |
| `#contact`        | Email, phone, LinkedIn                          |

---

## CSS Design System

All design tokens live in `:root` at the top of the `<style>` block.

### Color Palette

```css
--bg:     #080810   /* dark navy background */
--bg2:    #0e0e1a   /* slightly lighter background */
--orange: #E8612A   /* primary accent / CTA color */
--muted:  #7a7a9a   /* secondary / muted text */
```

### Typography

- **Syne** — headings, display text (bold, geometric)
- **DM Sans** — body copy, labels
- Responsive sizing via `clamp()` throughout

### CSS Conventions

- CSS custom properties for all repeated values
- Section comments: `/* ── SECTION NAME ── */`
- Kebab-case class names (`hero-name`, `exp-item`, `metric-value`)
- BEM-influenced naming (block-element pattern)
- Breakpoints: `900px` and `600px`

---

## Animation System

Scroll-reveal uses two CSS classes toggled by JavaScript:

```
.reveal               → initial state (opacity: 0, transform: translateY(20px))
.reveal + .visible    → final state   (opacity: 1, transform: none)
.reveal-delay-1 … -4  → staggered delays (0.1 s steps)
```

The `IntersectionObserver` in `<script>` adds `.visible` when elements enter the viewport (threshold `0.1`, rootMargin `0px 0px -40px 0px`). Hero metrics are triggered immediately with a 100 ms base delay.

---

## Editing Guidelines for AI Assistants

### Modifying Content

- All content is inline in `index.html` — no CMS, no data files.
- Text changes: edit the HTML directly within the relevant `<section>`.
- Metrics/numbers appear in `.metric-value` / `.metric-label` elements and in `<strong>` tags inside experience bullets.

### Modifying Styles

- Change design tokens in `:root` to update the whole theme.
- Add new component styles after the relevant section comment.
- Do **not** introduce an external CSS file unless explicitly requested.

### Modifying JavaScript

- The JS block is at the bottom of `<body>`.
- Keep it vanilla — no imports, no modules, no npm dependencies.
- The `IntersectionObserver` callback is the only logic; extend it carefully.

### Adding a New Section

1. Add the `<section id="new-section">` block in `index.html`.
2. Add the corresponding CSS under a new `/* ── NEW SECTION ── */` comment.
3. Add `.reveal` (and optional `.reveal-delay-N`) classes to animatable elements.
4. Add a `<a href="#new-section">` link in the `<nav>` if appropriate.

---

## Git Workflow

```bash
# Feature/fix work
git add index.html
git commit -m "feat: <short description>"

# Push (the active development branch)
git push -u origin claude/claude-md-mm3m1y50s14iov0n-mgnOT
```

Branch naming convention for AI sessions: `claude/<session-id>`.

---

## Testing

There is no automated test suite. Verify changes by:

1. Opening `index.html` in a browser.
2. Checking all sections render correctly.
3. Resizing to mobile widths (≤ 600 px) and tablet (≤ 900 px).
4. Scrolling to confirm reveal animations trigger properly.
5. Clicking all nav links and CTA buttons.

---

## Deployment

The site is a static HTML file — deployable anywhere:

- **GitHub Pages** — commit `index.html` to a `gh-pages` branch or `/docs` folder.
- **Netlify / Vercel** — drag-and-drop or point to the repo root.
- **Any CDN / web host** — upload `index.html` directly.

No build step, no CI configuration needed.

---

## Key Contacts / Metadata

| Field    | Value                           |
|----------|---------------------------------|
| Owner    | Maxime Girard                   |
| Email    | girard.maxime33@gmail.com       |
| LinkedIn | linkedin.com/in/girardmaxime    |
| Language | French (page content)           |
