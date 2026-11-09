"""Check local links, fragments, bilingual metadata and archive counts.

Run from any directory: python3 scripts/check_links.py
External editorial sources are reviewed separately in each article's source ledger.
"""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://mameend.github.io/japanese-culture-journal/'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.links = []
        self.canonicals = []
        self.alternates = {}
        self.language = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'html':
            self.language = a.get('lang')
        if tag in ('a', 'link') and 'href' in a:
            self.links.append(a['href'])
        if tag in ('img', 'script') and 'src' in a:
            self.links.append(a['src'])
        if tag == 'img':
            assert 'alt' in a, 'An image is missing its alt attribute'
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonicals.append(a.get('href'))
        if tag == 'link' and a.get('rel') == 'alternate':
            language = a.get('hreflang')
            assert language not in self.alternates, f'Duplicate hreflang: {language}'
            self.alternates[language] = a.get('href')


texts = {p.name: p.read_text() for p in ROOT.glob('*.html')}
pages = {name: Page(text) for name, text in texts.items()}
checked = 0
for name, page in pages.items():
    assert len(page.ids) == len(set(page.ids)), f'{name}: duplicate id'
    assert page.canonicals == [BASE + name], f'{name}: canonical mismatch'
    stem = name.removesuffix('.en.html').removesuffix('.html')
    expected = {'ja': BASE + stem + '.html', 'en': BASE + stem + '.en.html'}
    assert page.alternates == expected, f'{name}: hreflang mismatch'
    assert page.language == ('en' if name.endswith('.en.html') else 'ja'), name
    other = stem + ('.html' if page.language == 'en' else '.en.html')
    assert other in page.links, f'{name}: missing language switch'
    for href in page.links:
        parsed = urlsplit(href)
        if href.startswith(BASE):
            target = unquote(parsed.path.removeprefix('/japanese-culture-journal/'))
        elif parsed.scheme or parsed.netloc:
            continue
        else:
            target = unquote(parsed.path) or name
        target = target or 'index.html'
        assert (ROOT / target).is_file(), f'{name}: missing target {href}'
        if parsed.fragment and target.endswith('.html'):
            assert unquote(parsed.fragment) in pages[target].ids, f'{name}: missing fragment {href}'
        checked += 1

for lang in ('ja', 'en'):
    suffix = '.en.html' if lang == 'en' else '.html'
    counts = {}
    for category in ('tea', 'flowers', 'ceramics', 'kimono', 'food', 'ideas'):
        name = 'category-' + category + suffix
        counts[category] = texts[name].count('<article class="story-card">')
    for name in ['index' + suffix] + ['category-' + key + suffix for key in counts]:
        text = texts[name]
        count = text.count('<article class="story-card">')
        label = f'{count} 本の記事' if lang == 'ja' else f'{count} ' + ('article' if count == 1 else 'articles')
        assert f'aria-label="{label}"' in text, f'{name}: archive aria count mismatch'
        assert f'<p class="list-count">{label}</p>' in text, f'{name}: visible archive count mismatch'
        directory = re.search(r'<section class="category-directory">(.*?)</section>', text, re.S).group(1)
        for category, count in counts.items():
            block = re.search(r'<a href="category-' + category + re.escape(suffix) + r'">(.*?)</a>', directory, re.S).group(1)
            label = f'{count} 本' if lang == 'ja' else f'{count} ' + ('article' if count == 1 else 'articles')
            assert f'<small>{label}</small>' in block, f'{name}: {category} directory count mismatch'
    archive = texts['index' + suffix]
    assert 'seasonal-picks.css' in archive and 'seasonal-picks.js' in archive
    assert 'class="seasonal-picks"' in archive

print(f'Link checks passed: {len(pages)} pages; {checked} local references; fragments, language pairs, metadata, counts and seasonal section verified.')
