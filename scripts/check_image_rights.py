"""Fail publication when a displayed local photo is unregistered or has changed."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'img':
            self.images.append(attrs.get('src', ''))
        if tag in ('a', 'link') and attrs.get('href'):
            self.links.append(attrs['href'])

with (ROOT / 'assets.csv').open(encoding='utf-8-sig', newline='') as file:
    rows = list(csv.DictReader(file))
assert len({r['asset_id'] for r in rows}) == len(rows), 'Duplicate asset IDs'
photos = {r['file_path']: r for r in rows if r['file_path']}
assert len(photos) == sum(bool(r['file_path']) for r in rows), 'Duplicate file registrations'
used = {}
pages = sorted(ROOT.glob('*.html'))
for path in pages:
    page = Page()
    page.feed(path.read_text())
    for source in page.images:
        url = urlsplit(source)
        assert not url.scheme and not url.netloc, f'{path.name}: external photo must be archived and registered'
        name = unquote(url.path)
        assert name in photos, f'{path.name}: unregistered photo {name}'
        row = photos[name]
        assert not row['rights_status'].startswith('retired'), f'{path.name}: retired photo {name}'
        assert row['commercial_use_confirmed'] == 'yes', f'{name}: not approved for commercial publication'
        assert (ROOT / name).is_file(), f'{name}: missing photo'
        assert row['source_or_original_url'].startswith('https://'), f'{name}: missing source'
        assert row['license_or_permission'] and row['modification_conditions'], f'{name}: missing terms'
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == row['sha256'], f'{name}: changed photo needs review'
        if 'metmuseum.org' in row['source_or_original_url']:
            oid = row['source_or_original_url'].rstrip('/').split('/')[-1]
            assert json.loads((ROOT / f'met-{oid}.json').read_text())['isPublicDomain'] is True
        used.setdefault(name, set()).add(path.name)
    for source in page.links:
        url = urlsplit(source)
        if url.scheme or url.netloc or not url.path:
            continue
        assert (path.parent / unquote(url.path)).is_file(), f'{path.name}: broken local link {source}'
for name, row in photos.items():
    if row['rights_status'].startswith('retired'):
        assert not (ROOT / name).exists(), f'{name}: retired file still served'
    else:
        assert used.get(name) == set(row['used_in'].split('; ')), f'{name}: use inventory is stale'
print(f'Image rights checks passed: {len(pages)} HTML pages, {len(used)} active photos; registration, hashes, retirement and local links verified.')
