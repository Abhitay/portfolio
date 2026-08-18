---
name: Abhitay Shinde Portfolio
description: A black-and-white editorial broadsheet for a data scientist who ships production GenAI.
colors:
  ink: "#0a0a0a"
  paper: "#ffffff"
  muted: "#6f6b66"
  faint: "#8b867e"
  surface: "#f6f4f1"
  border: "#e7e3dd"
  border-strong: "#d3cec6"
  success: "#1f7a52"
  warning: "#9a6a00"
  danger: "#b42318"
typography:
  display:
    fontFamily: "Fraunces, Iowan Old Style, Georgia, serif"
    fontSize: "clamp(40px, 6vw, 60px)"
    fontWeight: 500
    lineHeight: 1.05
    letterSpacing: "-0.025em"
  heading:
    fontFamily: "Fraunces, Iowan Old Style, Georgia, serif"
    fontSize: "30px"
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  caption:
    fontFamily: "Fraunces, Iowan Old Style, Georgia, serif"
    fontSize: "clamp(34px, 4.4vw, 58px)"
    fontWeight: 500
    lineHeight: 1.08
    letterSpacing: "-0.02em"
    fontStyle: "italic"
  body:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.7
    letterSpacing: "0"
  label:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    fontSize: "12px"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0.12em"
rounded:
  flat: "0"
  figure: "8px"
  tile: "11px"
  pill: "999px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "40px"
  section: "56px"
components:
  nav-button:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "9px 18px"
    height: "38px"
  tag:
    backgroundColor: "transparent"
    textColor: "{colors.muted}"
    rounded: "{rounded.flat}"
    padding: "0"
  work-item:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.flat}"
    padding: "30px 0"
  finding-note:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.figure}"
    padding: "22px 26px"
---

# Design System: Abhitay Shinde Portfolio

## Overview

**Creative North Star: "The Broadsheet"**

This is a black-and-white editorial publication about one person, set with the confidence of a newspaper front page. A serif masthead carries oversized display type; grey italic standfirsts run a single word struck solid black; content is organized into hairline-separated columns and lists rather than cards. Nothing floats, nothing glows, nothing is colored. The restraint is the argument: a data scientist who writes up his own work with honest tradeoffs earns trust by looking considered, not decorated.

The personality is **quietly witty**. The default voice is precise and understated, but dry personality surfaces exactly where a broadsheet allows it: the right-aligned section captions ("made with black coffee and a curious mind", "rooms I was lucky to be in"). That wit is always the accent, never the substance, and it always rides the same typographic device rather than a novelty treatment.

Density is generous and reading-first. A single centered column (~80% viewport width, capped near 1470px) holds everything; whitespace and hairline rules do the work that borders and shadows would do elsewhere. The system is deliberately near-monochrome, so the few status hues exist only for rare case-study annotations and never enter the chrome.

**Key Characteristics:**
- Serif display (Fraunces) + sans body (Inter); no third voice.
- Strict ink / paper / warm-grey palette; no color in the interface.
- Hairline rules and whitespace instead of cards, boxes, or shadows.
- Right-aligned grey italic section captions with one word struck black.
- Tags and links are grey underlined text, never pills.

## Colors

A near-monochrome palette: near-black ink on warm white paper, with a warm-grey ramp doing all the secondary work. The warmth (a faint brown in the greys) keeps it from reading as clinical pure-grey.

### Neutral
- **Ink** (#0a0a0a): Primary text, display headlines, the struck keyword in captions, and the full-bleed contact/footer ground. The only "strong" value in the system.
- **Paper** (#ffffff): The page background and the ground behind the translucent nav.
- **Muted** (#6f6b66): Secondary text, body copy in supporting roles, tags, and link labels. The workhorse grey.
- **Faint** (#8b867e): Tertiary text, the grey of section captions and inline meta (GPA, dates), and small kickers. Held at ≥3:1 on paper so the large captions stay legible.
- **Surface** (#f6f4f1): The single warm off-white fill, used only for inset "finding" asides in case studies. Never stacked or used for cards.
- **Border** (#e7e3dd): Hairline rules between list rows and section starts.
- **Border-Strong** (#d3cec6): Underline color under tags and links; the outline of the nav Resume button and logo tiles.

### Status (rare, case-study only)
- **Success** (#1f7a52), **Warning** (#9a6a00), **Danger** (#b42318): Reserved for occasional evidence annotations inside case-study prose. They never appear in navigation, tags, buttons, or the homepage.

### Named Rules
**The Monochrome Rule.** The interface is ink, paper, and warm-grey only. No blue links, no brand color, no gradients. The sole tinted exception is a company/school logo tile whose background is matched to that logo's own brand ground so the mark blends into the rounded tile.

**The One Ground Rule.** There is exactly one dark region: the contact + footer band in Ink. Its inversion signals the end of the page; it is never repeated elsewhere.

## Typography

**Display Font:** Fraunces (with Iowan Old Style, Georgia, serif)
**Body Font:** Inter (with system-ui sans fallbacks)

**Character:** A high-contrast literary serif paired with a neutral grotesque. Fraunces brings the broadsheet's editorial authority and an expressive true italic; Inter keeps the reading and UI text plain and modern. The tension between the two is the whole type system.

### Hierarchy
- **Display** (Fraunces 500, clamp(40px,6vw,60px), line-height 1.05, tracking -0.025em): Hero headline and case-study titles. Large, tightly tracked.
- **Heading** (Fraunces 500, 30px / 21px, line-height 1.2, tracking -0.01em): Section (h2) and sub-section (h3) titles.
- **Caption** (Fraunces 500 *italic*, clamp(34px,4.4vw,58px), grey with one Ink word): The section standfirst, right-aligned on the same baseline row as the kicker (masthead) and wrapping to two lines. The signature element of the system.
- **Body** (Inter 400, 16px, line-height 1.7, tracking 0): All running prose and descriptions.
- **Label** (Inter 600, 11-12px, uppercase, tracking 0.1-0.14em): Section kickers ("01 · Experience") and the hero location eyebrow. The top label level.
- **Sub-header** (Inter 600, 13px, sentence case, no tracking): Sub-group labels inside a section ("In the Press", "Certifications"). Same sans family as the kicker but sentence case and untracked, so it reads a clear level down without twinning the all-caps kicker.

### Named Rules
**The Struck-Word Rule.** Every section caption is grey Fraunces *italic* with exactly one word (or short phrase) set upright-weight in solid Ink. One struck word per caption, always at a meaningful noun. It is the only place italic and the only place a lone black accent appears in grey text.

**The Optical Masthead Rule.** Large display type carries negative tracking (-0.025em) and `font-optical-sizing: auto`; body stays at 0 tracking. Never apply one letter-spacing value across sizes.

**The No-Em-Dash Rule.** House copy never uses em dashes, in body or captions. Use a period, a comma, or restructure.

## Layout

A single centered reading column, not a grid of cards. Sections are ~82.4% of viewport width, capped at 1470px, centered, with ~56px vertical padding between them. Content within a section is one column at full measure; supporting meta (tags, read-time, dates) sits as a hairline meta row above or beside its title rather than in a side rail.

Groups of items (Experience, Education, Research Publications, Certifications, case studies) are vertical lists whose rows are divided by 1px Border hairlines, first row flush. The Certifications block is a two-column reference list (issuer left ~225px, items right) that collapses to one column below 640px. Case-study body sections open with an oversized serif numeral (01/02/03) and a thin top rule, echoing the Contents index.

Spacing is in a loose 4 / 8 / 16 / 24 / 40 / 56px rhythm. The layout scales fluidly with `clamp()` type; it stays a single column at every breakpoint (the column just narrows), and the mobile nav collapses to a translucent hamburger below ~768px.

## Elevation & Depth

The system is **flat by default**. Depth comes from hairline rules, whitespace, and one inverted ground (the Ink contact/footer band), never from drop shadows on content. There are no card shadows, no elevation ramp.

### Shadow Vocabulary (the only shadow)
- **Toggle lift** (`box-shadow: 0 8px 16px rgba(0,0,0,0.08)`): Appears only on hover of the mobile menu toggle, as a small tactile response. Nothing else in the system casts a shadow.

### Named Rules
**The Flat-By-Default Rule.** Surfaces are flat at rest and stay flat. The single permitted shadow is the mobile toggle's hover lift; if a new element wants a shadow to separate itself, use a hairline rule or whitespace instead.

**The Translucent-Chrome Rule.** The only translucency is the sticky nav (`backdrop-filter: blur(12px) saturate(180%)` over `rgba(255,255,255,0.86)`), with content scrolling under it and a hairline appearing only once scrolled past the hero. It degrades to solid under `prefers-reduced-transparency`.

## Shapes

The default corner is **square (0 radius)**: hairlines and text, not rounded containers. Roundness is reserved and specific: **pills (999px)** for the two outlined controls (nav Resume button, and contact "pill-links" which are visually rendered as underlined text), **tiles (11px)** for the 46px company/school logo squares, and **soft (8px)** for figures and the inset finding asides. There are no rounded content cards; a "card" in this system is a hairline-separated list row, not a box.

Borders are always hairline 1px in Border or Border-Strong, used as dividers and underlines rather than enclosures. Underlines sit 3px below text in Border-Strong and darken to Ink on hover.

## Components

### Buttons
- **Shape:** Pill (999px), outlined, quiet.
- **Nav Resume button:** Transparent fill, 1px Border-Strong outline, Ink label, 9px 18px padding, 38px tall. The only persistent button in the chrome.
- **Hover / Focus:** Subtle background/border shift; on press, scales to 0.95 (compositor transform, cubic-bezier(0.22,1,0.36,1)). Keyboard focus shows a 2px `currentColor` focus-visible ring.

### Tags
- **Style:** Grey (Muted) text with a 1px Border-Strong underline offset 3px. No fill, no border box, no padding. Used for project tech tags, case-study tags, experience skills, and hero/contact meta.
- **State:** Underline darkens toward Ink on hover.

### Cards / Containers
- **There are no boxed cards.** Related content is a hairline-separated list row: 1px Border top rule, first row flush, generous vertical padding (~22-32px). Experience, Education, Publications, and case-study project rows all use this pattern.
- **Finding aside (case studies only):** The one filled surface. Surface (#f6f4f1) ground, 8px radius, 22px 26px padding, no border, a serif kicker lead. A quiet inset note, never a colored callout.

### Navigation
- **Style:** Sticky, translucent (blur + saturate over 86% white), content scrolls under. Wordmark left in Fraunces; links right in Inter with an animated underline on hover/active; Resume as the outlined pill.
- **States:** Hairline bottom border fades in only after scrolling past the hero. Mobile (<768px) collapses to a translucent rounded hamburger toggle.

### Section Caption (signature component)
- Right-aligned, grey Fraunces italic, one word struck Ink. Paired with a left-aligned uppercase Inter kicker ("02 · Experience"). This masthead pairing opens every homepage section.

## Do's and Don'ts

### Do:
- **Do** keep the palette to Ink / Paper / warm-grey; let hairlines and whitespace carry structure.
- **Do** separate groups with 1px Border hairline rows, first row flush, not boxes.
- **Do** render tags and inline links as grey underlined text (Border-Strong underline, 3px offset).
- **Do** give every section a struck-word caption: grey Fraunces italic with exactly one Ink word.
- **Do** tighten large display type (-0.025em) and keep body at 0 tracking.
- **Do** tint a logo tile to its own brand background so the mark blends into the 11px tile.

### Don't:
- **Don't** introduce any accent color, gradient, or glassmorphism into the interface (logo-tile tints are the only exception).
- **Don't** use pill chips, bordered cards, or drop shadows on content; the mobile toggle's hover lift is the only shadow.
- **Don't** use em dashes anywhere in copy or captions.
- **Don't** add a second dark region; the contact/footer band is the only inverted ground.
- **Don't** stack the Surface fill on itself or use it for cards; it is only the case-study finding aside.
- **Don't** fabricate metrics, testimonials, logos, or an availability claim; every visible credential must be real and verifiable.
