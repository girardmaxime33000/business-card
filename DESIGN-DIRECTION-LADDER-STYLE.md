# Ladder Style — Design & Art Direction Specification

girardmaxime33.com redesign. Reference document for the `ladder-style` branch. Defines art direction only — no implementation in this document.

---

## 1. Visual Narrative & Core Aesthetic

**Creative concept:** Surgical Precision & Editorial Depth.

**Brand personality:** Authoritative, bespoke, technical, calm, elevated. The site behaves like a senior consultant's private memo, not a marketing page — declarative statements, measured pacing, no persuasion tactics.

**Design rationale:** B2B buyers evaluating a six-figure engagement pattern-match trust off restraint, not decoration. A dark, high-precision surface with editorial typography signals: this person operates at board level, thinks in systems, and doesn't need to oversell. Every visual choice below optimizes for perceived seniority and analytical rigor over conversion tricks.

---

## 2. Typography Architecture

| Role | Typeface | Notes |
|---|---|---|
| Display / H1–H2 | **Fraunces** (variable, optical size + soft) | Editorial serif with sharp contrast and slight quirk in italics. Weight 340–460 for body headings, 600–650 for hero. Used sparingly — headlines and pull quotes only. |
| Secondary display / H3–H5 | **General Sans** or **Söhne** (fallback: Inter Display) | Geometric sans, semi-bold (600), tight tracking (-1%). Used for card titles, section labels. |
| Body / UI | **Inter** (variable) | 400/500 weights only. 16px base, 1.6 line-height on body copy, 1.4 on UI chrome. |
| Monospace | **JetBrains Mono** | Metrics, KPIs, tags, timestamps, code-like data (`+240% MQL`, `EU/US/JP`, `v2.4`). Always uppercase or tabular-nums for numbers. |

**Pairing rule:** Fraunces never appears below 24px. Inter never carries brand voice (no taglines in Inter — reserve emotional weight for the serif). Monospace text is always accompanied by a muted-graphite label in Inter, never floats alone.

**Hierarchy scale (px, desktop):** 72 / 48 / 32 / 24 / 18 / 16 / 14 (mono 13).

---

## 3. Color System & Tonal Balance

| Token | Hex | Usage |
|---|---|---|
| `--bg-obsidian` | `#0B0D12` | Primary dark background (hero, nav, footer) |
| `--bg-offwhite` | `#F7F6F2` | Alternating light section blocks |
| `--surface-raised` | `#12151C` | Cards/panels on dark bg |
| `--surface-raised-light` | `#FFFFFF` | Cards/panels on light bg |
| `--accent-primary` | `#10B981` (emerald) | CTAs, active states, growth metrics |
| `--accent-signal` | `#00F0FF` (electric cyan) | Rare — live status dot, hover glow only, never body text |
| `--text-primary-dark` | `#F4F5F7` | Body text on dark |
| `--text-primary-light` | `#0B0D12` | Body text on light |
| `--text-muted` | `#8A909C` | Subtext, captions, meta on dark |
| `--text-muted-light` | `#5B6070` | Subtext on light |
| `--border-hairline` | `rgba(244,245,247,0.08)` | 1px card borders on dark |
| `--border-hairline-light` | `rgba(11,13,18,0.10)` | 1px card borders on light |

**Rule:** one accent color drives action per screen — emerald for CTAs/metrics, cyan reserved exclusively for a single "live" indicator (status badge, availability dot). Never both as competing accents in the same viewport. No gradients except a 4%-opacity radial glow behind hero copy.

---

## 4. Layout, Grid & Spatial Feel

- **Grid:** 12-column, max-width 1280px, 24px gutter desktop / 16px mobile. Content blocks intentionally break the grid asymmetrically (e.g., a case-study card spans cols 1–7 while its metric panel spans cols 8–12, offset).
- **Vertical rhythm:** 8px base unit. Section padding: 160px desktop / 80px mobile top+bottom. Never less than 96px between sections.
- **Cards/surfaces:** 1px hairline border (see tokens above), 10px radius, no drop shadow on dark surfaces — use a 1px inner top highlight (`rgba(255,255,255,0.04)`) instead of shadow to simulate glass. On hover: border brightens to `rgba(16,185,129,0.4)` + 12px emerald glow at 8% opacity, 180ms ease-out.
- **Data/portfolio presentation:** floating UI mockups tilted 2–4° with a soft dark drop shadow; KPI numbers in JetBrains Mono at 40–56px next to a 12px Inter uppercase label; tag pills — 6px radius, 1px hairline border, 12px mono text, 4px/10px padding.

---

## 5. Imagery, Motion & Micro-Interactions

- **Photography:** high-contrast monochrome or near-monochrome (single emerald or cyan color-grade accent), moody minimal-architecture or macro tech details (PCB traces, glass, concrete). No stock "people in suits shaking hands."
- **Motion:** 150–200ms ease-out (`cubic-bezier(0.16, 1, 0.3, 1)`) on all interactive transitions. Card hover = border + glow only, no scale/translate beyond 2px lift. Scroll reveal stays as currently implemented (`IntersectionObserver`, threshold 0.1) — do not replace with heavier scroll-jacking.
- **Micro-interactions:** CTA buttons get a 1px border sweep on hover (emerald fill wipes left-to-right, 200ms), not a color snap. Live-status badge pulses opacity 0.6↔1 on a 2s loop — the only looping animation permitted on the page.

---

## 6. Key Conversion Components

- **Hero:** value-first headline in Fraunces (e.g., a single declarative sentence, 48–72px), one-line Inter subhead, primary CTA (solid emerald, dark text) + secondary CTA (ghost, hairline border), and a small live-status mono badge (`● Available for Q4 engagements`) top-left of the headline block.
- **Case studies / social proof:** card grid, 1–2 per row desktop. Each card: client/context label (mono, muted) → headline result in Fraunces + huge mono metric (e.g., `+240%`) → one supporting sentence in Inter. No star ratings, no logos-as-decoration — logos appear once, small, in a dedicated trust strip.
- **Contact/booking:** single-column minimalist form, one field per row, 48px input height, bottom-border-only inputs (no boxes) that turn emerald on focus, Calendly embedded inline below the form rather than in a modal — keeps the page feeling like one continuous document rather than a funnel.

---

## 7. AI Asset Generation Prompts (Midjourney)

1. **Hero mood board:** `moody editorial photograph, deep obsidian background #0B0D12, single shaft of warm light hitting a matte black architectural column, subtle emerald green rim light, minimalist composition, negative space for text overlay on left third, shot on Hasselblad, high contrast, no people, cinematic, --ar 16:9 --style raw --v 6`

2. **Abstract network nodes:** `abstract 3D render of interconnected glowing nodes and thin data lines, dark obsidian void background, nodes in emerald #10B981 and electric cyan #00F0FF accents, thin 1px connecting lines, sense of precision engineering and systems thinking, subtle depth of field, minimal and technical, no text, --ar 3:2 --style raw --v 6`

3. **Dark-mode texture background:** `extreme macro texture, brushed matte black metal surface with faint circuit-board etching pattern, very subtle emerald green glow in the grooves, almost monochrome, low contrast, suitable as a subtle full-bleed website background texture, seamless, --tile --ar 16:9 --style raw --v 6`

---

## Implementation notes for this branch

- Treat this as a parallel visual system, not a token swap on the existing Tailwind config — `tailwind.config.js` colors, `tailwind-input.css`, and the hero/card markup in `index.html` will need structural changes (grid spans, card borders, font imports for Fraunces + General Sans + JetBrains Mono in addition to the current Plus Jakarta Sans/JetBrains Mono pair).
- Existing i18n (`data-i18n*` + `t.fr`/`t.en`) and build pipeline (`build-en.py` → `tailwindcss`) rules from `CLAUDE.md` still apply once implementation starts on this branch.
- No code changes made yet — this document is the spec to build against.
