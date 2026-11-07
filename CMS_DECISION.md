# CMS assessment — initial, reversible

**Decision for now:** keep editorial work in this folder and defer a CMS subscription until the first article and visual direction are ready for a site prototype. Nothing here creates an account, uploads content, or publishes a page.

## Shortlist

| Option | Fits when | Trade-off |
|---|---|---|
| **Webflow** | A highly art-directed, image-led publication site is the priority and a visual builder is comfortable. Its current Premium site plan includes CMS; the displayed US price is $25/month billed yearly. Localization is an add-on, shown from $9/month per locale. CMS localization creates distinct items per locale, so each translation needs deliberate maintenance. | More visual control, but more design and configuration work; paid plan and localization cost should be checked for Japan, taxes, and current checkout terms before choosing. |
| **Ghost(Pro)** | Publishing, newsletters, and paid memberships are central from the start. Managed hosting avoids self-hosting and the product is built around publication and membership. | Less freedom for a bespoke visual layout than a design-first builder; confirm current plan limits, bilingual URL/workflow needs, and total price before choosing. |

Webflow's published pricing and help pages were checked on 2026-11-08: [plans and pricing](https://webflow.com/pricing), [localizing CMS collection content](https://help.webflow.com/hc/en-us/articles/33961252209171-Localize-Collection-content). Ghost's official [Ghost(Pro) pricing](https://ghost.org/pricing) page describes membership products; check the current plan price and limits when evaluating a trial.

## Working recommendation

Start with the file-based editorial desk in this repository and GitHub Pages for the first public prototype. It publishes the existing static HTML without a CMS or server to maintain. The prepared release workflow is manual and human-gated; see `GITHUB_PAGES_SETUP.md`. For the eventual public site, test Webflow first if visual storytelling and art direction are the main differentiators; test Ghost first if newsletter and membership revenue are the immediate business model. Revisit this after the first article is approved and the desired publishing cadence, newsletter, commerce, and budget are known. Avoid custom PHP/WordPress as requested.

## Decision log

- 2026-11-08 — no CMS selected; no external account or site created. Reassess after article 1's editorial prototype.
- 2026-11-08 — GitHub Pages selected as the first static-site prototype path. Local files and a manual deployment workflow are prepared; no GitHub repository, remote, or public site exists yet.
