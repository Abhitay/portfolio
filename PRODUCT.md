# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary: recruiters and hiring managers evaluating Abhitay Shinde for data science / ML / GenAI roles — skimming for fit, depth, and proof before reaching out or advancing him. Secondary: engineering and data-science peers and interviewers who actually read the case studies and judge rigor, tradeoffs, and production sense. Most arrive from a résumé, LinkedIn, or a job application, often mid-triage, on both desktop and mobile.

## Product Purpose

A personal portfolio site for Abhitay Shinde (Data Scientist). Its job is to convert a visitor into a conversation — an interview, an intro, or outreach — by presenting his work, publications, experience, and credentials credibly enough that a skeptical technical reader trusts them. Success is a recruiter shortlisting him or a peer coming away convinced he ships real systems.

## Positioning

"Ships production GenAI, not demos." The differentiated claim is engineering rigor applied to real systems: retrieval/RAG, human-gated agents, evaluation harnesses, semantic caching, and fine-tuned guarded text-to-SQL — each written up with honest tradeoffs and failure modes, not just wins — combined with causal-inference / experimentation depth and peer-reviewed research. The through-line a neighboring candidate could not truthfully copy: every case study shows the tradeoff it navigated, and every credential is independently verifiable.

## Operating Context

Visitors typically land from an application, LinkedIn, or the résumé PDF and skim quickly. A technical reader may open individual case-study pages, and may verify claims out-of-band via Google Scholar, Coursera verify links, GitHub, or employer names. The résumé (`docs/Shinde-Resume.pdf`) is a first-class exit. The site is read, not operated — there is no login, task flow, or persisted state.

## Capabilities and Constraints

- Static site: hand-written HTML/CSS/JS, no framework and no build step, served by GitHub Pages from `docs/` at the custom domain abhitay.me.
- Surfaces: homepage (hero, Selected Projects, Experience, Publications & Media, Education + Certifications, Contact/footer) plus one standalone page per case study.
- Case studies follow a fixed three-section narrative: Introduction and Problem · Technical Approach · Results.
- No backend, analytics beyond gtag, or dynamic content; all content is self-maintained by editing the source directly.
- Content is authored in the first person and kept free of em dashes by house convention.

## Brand Commitments

- Name: **Abhitay Shinde**, Data Scientist.
- **B&W editorial identity is a committed brand, not a placeholder**: minimal black / white / warm-grey palette, Fraunces (serif display) paired with Inter (sans), hairline-separated editorial lists, section captions in a lighter grey with a single black keyword. No color accents, glassmorphism, or decorative gradients.
- Voice: precise and understated with occasional dry wit (e.g. section captions like "made with black coffee and a curious mind").
- Real employer/school logos are used and tinted to their brand background where it helps them blend into the rounded tile.

## Evidence on Hand

- Peer-reviewed publications with Google Scholar citation links: metro predictive maintenance, diabetes detection (recall-optimized), NLP-to-SQL for mobile learning, traditional-image-processing watermark removal, semi-supervised disease prediction.
- Certifications with real Coursera verify codes (University of Washington ML, IBM Data Science, SAS, Wesleyan/Edinburgh, Arizona State, Deep Teaching Solutions) plus non-Coursera items (NIIT, Internshala, Udemy).
- Real employers with logos (e.g. Julius Baer, TD Bank, Ask2AI) and education (Columbia M.S. Data Science, NMIMS B.Tech Hons., Utpal Shanghvi School).
- Media coverage: ThePrint (ANI PR) feature and a 1st-place hackathon win (EcoGuards, REVA University + Kyndryl), with event image and video links.
- Résumé PDF at `docs/Shinde-Resume.pdf`; case-study diagrams as hand-made SVGs in `docs/figures/`.
- **All content is real and verifiable. Future work must never fabricate metrics, testimonials, employers, publications, or credentials, and must not invent an "open to work" availability signal beyond what the user states.**

## Product Principles

1. **Proof over claims.** Every substantive assertion resolves to verifiable evidence (Scholar, verify links, named employers); nothing is asserted that a reader cannot check.
2. **Rigor is the brand.** Case studies lead with the problem and show the tradeoff and failure mode, not a highlight reel — that honesty is the differentiator.
3. **Convert to conversation.** Contact and résumé stay frictionless and prominent; the site exists to start an outreach, so nothing should bury that path.
4. **Restraint as signal.** The minimal editorial identity *is* the point; resist decoration, added color, and pill/box chrome. When in doubt, remove.
5. **Real, never fabricated.** No invented numbers, quotes, or availability claims — ever.

## Accessibility & Inclusion

No formal external standard was mandated, but the codebase treats accessibility as a craft commitment: keyboard `:focus-visible` rings, and honored `prefers-reduced-motion`, `prefers-reduced-transparency`, and `prefers-contrast` preferences. Future work should preserve these and keep color contrast within the monochrome palette legible.
