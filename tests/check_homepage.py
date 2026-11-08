"""Local browser smoke tests. Requires Playwright and system Chromium.
Run: python3 tests/check_homepage.py [base URL]
Without a URL, serves the repository on an ephemeral loopback port.
"""
import contextlib
import functools
import http.server
import sys
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

@contextlib.contextmanager
def local_site():
    if len(sys.argv) > 1:
        yield sys.argv[1].rstrip('/') + '/'
        return
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        yield f'http://127.0.0.1:{server.server_port}/'
    finally:
        server.shutdown()

with local_site() as base, sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium')
    for lang, filename in [('ja','index.html'),('en','index.en.html')]:
        for width in [1440, 768, 390, 320]:
            page = browser.new_page(viewport={'width':width,'height':1000}, timezone_id='America/Los_Angeles')
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.clock.install(time=__import__('datetime').datetime(2026,11,8,10,tzinfo=__import__('datetime').timezone.utc))
            response = page.goto(base+filename)
            assert response.status == 200
            page.wait_for_selector('.seasonal-card')
            assert page.locator('.seasonal-card').count() == 6
            article_count = page.locator('.story-list > .story-card').count()
            assert article_count > 0
            assert page.locator('.seasonal-picks').get_attribute('data-season') == 'autumn'
            assert page.locator('.seasonal-card h3 a').count() + page.locator('.seasonal-empty').count() == 6
            assert page.locator('.category-nav').inner_text().find('文化' if lang=='ja' else 'Culture') >= 0
            assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), f'overflow: {lang}/{width}'
            assert page.locator('img').evaluate_all('(images) => images.filter(i => i.complete && i.naturalWidth === 0).length') == 0
            for href in page.locator('.seasonal-card a').evaluate_all('(links) => links.map(a => a.getAttribute("href"))'):
                assert href.endswith('.en.html') == (lang=='en'), href
            assert not errors, errors
            if width in [1440,390]: page.screenshot(path=f'/tmp/koto-{lang}-{width}.png', full_page=False)
            # Keyboard users can reach every story title and category link.
            page.keyboard.press('Tab')
            assert page.locator(':focus').get_attribute('class') == 'skip'
            selected_url = page.locator('.seasonal-card h3 a').first.get_attribute('href')
            page.locator('.seasonal-card h3 a').first.click()
            assert page.url.endswith(selected_url)
            page.go_back(); page.wait_for_selector('.seasonal-card')
            assert page.locator('.seasonal-card').count()==6
            page.reload(); page.wait_for_selector('.seasonal-card')
            assert page.locator('.seasonal-card').count()==6
            page.close()
        # Check every season and an already open tab crossing Tokyo midnight.
        page = browser.new_page()
        page.clock.install(time=__import__('datetime').datetime(2026,11,30,14,59,30,tzinfo=__import__('datetime').timezone.utc))
        page.goto(base+filename); page.wait_for_selector('.seasonal-card')
        assert page.locator('.seasonal-picks').get_attribute('data-season')=='autumn'
        page.clock.fast_forward(61_000)
        assert page.locator('.seasonal-picks').get_attribute('data-season')=='winter'
        for month,season in [(3,'spring'),(6,'summer'),(9,'autumn'),(12,'winter')]:
            page.clock.set_system_time(__import__('datetime').datetime(2027,month,15,tzinfo=__import__('datetime').timezone.utc)); page.reload(); page.wait_for_selector('.seasonal-card')
            assert page.locator('.seasonal-picks').get_attribute('data-season')==season
            assert page.locator('.seasonal-card').count()==6
        page.close()
        # Broken metadata must preserve browsing without false seasonal claims.
        page=browser.new_page();page.route('**/seasonal-picks.json',lambda route:route.fulfill(status=500,body='unavailable'))
        page.goto(base+filename);page.wait_for_selector('.seasonal-card')
        assert page.locator('[data-match="seasonal"]').count()==0
        assert page.locator('.story-list > .story-card').count()==article_count
        page.close()
        # No-JavaScript fallback keeps all categories and the full archive usable.
        page=browser.new_page(java_script_enabled=False);page.goto(base+filename)
        assert page.locator('.seasonal-fallback').count()==6
        assert page.locator('.story-list > .story-card').count()==article_count
        page.close()
    browser.close()
print('Homepage browser checks passed: JP/EN; desktop/tablet/mobile/320px; 4 seasons; JST boundary; keyboard; article navigation; Back/reload; failed metadata; no JS.')
