"""Build the English static edition from the shared Japanese layout and reviewed text.

Run from anywhere with Python 3. No dependencies or runtime translation API.
The exact-match checks fail if source copy changes without a translation update.
"""
import json
import re
from html import unescape
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name == "scripts" else HERE
OUTPUT = ROOT / "outputs" if (ROOT / "outputs").is_dir() else ROOT
ARTICLE = ROOT / "articles/tea-and-ceramics" if (ROOT / "articles/tea-and-ceramics").is_dir() else ROOT
source = (OUTPUT / "between-tea-and-ceramics.html").read_text(encoding="utf-8")
translations = json.loads((ARTICLE / "translations.en.json").read_text(encoding="utf-8"))
for original, translated in translations:
    if original not in source:
        raise SystemExit(f"Missing translation source: {original[:100]}")
    source = source.replace(original, translated)
source = source.replace('<html lang="ja">', '<html lang="en">')
source = source.replace(
    '<link rel="canonical" href="https://mameend.github.io/japanese-culture-journal/between-tea-and-ceramics.html">',
    '<link rel="canonical" href="https://mameend.github.io/japanese-culture-journal/between-tea-and-ceramics.en.html">')
source = source.replace('<a class="brand" href="index.html"', '<a class="brand" href="between-tea-and-ceramics.en.html"')
source = source.replace(
    '<div class="languages" aria-label="言語"><span aria-current="page">JP</span><a href="between-tea-and-ceramics.en.html" lang="en" hreflang="en" aria-label="Read in English">EN</a></div>',
    '<div class="languages" aria-label="Language"><a href="between-tea-and-ceramics.html" lang="ja" hreflang="ja" aria-label="日本語で読む">JP</a><span aria-current="page" style="margin-left:12px">EN</span></div>')
source = source.replace('</style>', 'html[lang="en"] .article-body p{font-family:Georgia,serif;font-size:18px;line-height:1.95;letter-spacing:0;text-align:left}html[lang="en"] .hero h1{font-family:Georgia,serif;letter-spacing:0;line-height:1.2;font-weight:400}html[lang="en"] .hero-dek{letter-spacing:0;line-height:1.9}html[lang="en"] .article-body h2{letter-spacing:0}html[lang="en"] .contents a{font-family:var(--sans);letter-spacing:0}html[lang="en"] .article-intro{font-family:Georgia,serif;letter-spacing:0;line-height:1.8}html[lang="en"] .pullquote{font-family:Georgia,serif;letter-spacing:0;line-height:1.7}html[lang="en"] .about p{font-family:Georgia,serif;letter-spacing:0;line-height:1.9}html[lang="en"] .languages a{margin-left:0}html[lang="en"] .colophon .credits-note{font:11px/1.9 var(--sans)}@media(max-width:720px){html[lang="en"] .article-body p{font-size:17px}html[lang="en"] .colophon .credits-note{font-size:11px}}\n</style>')
(OUTPUT / "between-tea-and-ceramics.en.html").write_text(source, encoding="utf-8")

# Keep the reviewable Markdown drafts in sync with the displayed article text.
def plain(markup):
    return unescape(re.sub(r"<[^>]+>", "", markup.replace("<br>", "\n").replace("</span>", "</span> "))).strip()

for language, markup, title in [
    ("ja", (OUTPUT / "between-tea-and-ceramics.html").read_text(encoding="utf-8"), "お茶と器のあいだ"),
    ("en", source, "Between Tea and Ceramics"),
]:
    article = markup.split('<article class="article-body"', 1)[1].split('<div class="colophon"', 1)[0]
    intro = re.search(r'<div class="article-intro">(.*?)</div>', article, re.S).group(1)
    blocks = [f"# {title}", "> Current article text, synchronized from the HTML edition. Publication authorization is recorded separately in approval.md.", plain(intro)]
    for match in re.finditer(r'<(h2|p|blockquote)\b[^>]*>(.*?)</\1>', article, re.S):
        tag, content = match.groups()
        text = plain(content)
        blocks.append(("## " if tag == "h2" else "> " if tag == "blockquote" else "") + text)
    (ARTICLE / f"draft.{language}.md").write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
print("Built English edition with all translation sources matched.")
