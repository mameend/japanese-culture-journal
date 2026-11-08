# Seasonal home-page selections

The home page shows one recommendation for each category, in both Japanese and English. It uses Japan time (`Asia/Tokyo`): spring March–May, summer June–August, autumn September–November, winter December–February. This is an editorial browsing convention, not a claim about local weather or traditional seasonal boundaries.

## Content and selection

- The existing `.story-list > .story-card` elements in `index.html` and `index.en.html` are the source of published articles, titles, descriptions, links, images, dates and categories. Keep this full archive intact when adding an article. Do not add draft or future/unpublished article cards.
- `seasonal-picks.json` is the shared, language-independent editorial metadata. Keys are article slugs without `.html` or `.en.html`. The metadata alone cannot publish an article or create an article link.
- A reviewed match for the current season takes priority. Within each group, avoid showing the same article twice when another choice exists, then prefer the newest publication date. The order in the archive breaks ties. Cross-category articles may appear in both categories when necessary.
- A category without a seasonal match receives ordinary category reading, clearly labeled as such. It is not represented as season-specific. A category without articles receives a non-clickbait empty state and a link to its category page. Articles explicitly marked as unsuitable year-round are not selected outside their listed seasons.
- The selection also updates when a tab stays open across a season boundary or becomes visible again. There is no analytics, user profiling, remote AI call, API key, build step, or server dependency.

## Adding daily articles

1. Fetch the latest `main` before editing and preserve its existing changes. Add the two language cards to their existing home-page archives and category pages as usual. Do not rebuild the TOP from an older saved template: preserve the seasonal section, stylesheet, script, and category naming.
2. If an article has a substantiated seasonal connection, add one entry to `seasonal-picks.json` with `seasons` (any of `spring`, `summer`, `autumn`, `winter`), `evergreen` (boolean), short Japanese and English `reason` strings, and an `evidence` explanation tied to the published article. This is editorial metadata, not permission to invent facts or seasonal etiquette.
3. `evergreen: true` allows the article to be used as normal category reading outside its matched seasons. For content specific to a season, use `false`. A generic article can omit the entry or use empty `seasons` and `evergreen: true`. New ordinary articles are discovered automatically even without metadata.
4. Never infer seasonal wearing rules from a kimono's motif, or assume a photograph establishes the season of an article. Distinguish a practical/editorial recommendation (such as warm meals) from a historical or cultural factual claim. Keep recommendations aligned with the evidence and both language editions.
5. Preserve registered image usage and existing attribution. The recommendations reuse the existing archive card photos, already displayed on the same home pages. Do not introduce new image assets without the normal rights review.
6. Display the former Ideas category as **文化 / Culture**, with directory heading **暮らしのテーマ / Themes for everyday life**. Keep `category-ideas.html` and `category-ideas.en.html` URLs and the internal `ideas` key for compatibility.

## Verification

Run:

```
node --check seasonal-picks.js
node --test tests/seasonal-picks.test.js
python3 scripts/check_image_rights.py
python3 tests/check_homepage.py
```

The browser smoke suite needs Python Playwright and Chromium at `/usr/bin/chromium`. It serves a temporary loopback preview and checks both languages, desktop/tablet/mobile widths, month boundaries in Japan time, links, keyboard entry, Back/reload, missing metadata, and JavaScript-disabled browsing. In environments that prohibit Chromium sockets, report that browser test as blocked and inspect the deployed page with the supported browser instead; do not claim the smoke suite passed.

No-JavaScript visitors retain all six category links and the complete article archive. If metadata cannot load, the enhanced section still provides category reading and tells the visitor that seasonal selection is unavailable.
