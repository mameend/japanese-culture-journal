/* Seasonal recommendations use reviewed editorial metadata, never title keywords.
 * The ordinary home-page story list remains the source of published articles.
 */
(function (root) {
  'use strict';

  const SEASONS = ['spring', 'summer', 'autumn', 'winter'];
  const CATEGORIES = ['tea', 'flowers', 'ceramics', 'kimono', 'food', 'ideas'];
  const COPY = {
    ja: {
      titles: ['春の暮らしに、読みたいもの', '夏の暮らしに、読みたいもの', '秋の暮らしに、読みたいもの', '冬の暮らしに、読みたいもの'],
      periods: ['3–5月', '6–8月', '9–11月', '12–2月'],
      categories: ['茶', '花', '器', '着物', '食', '文化'],
      intro: '季節の楽しみを、日々の暮らしへ。季節につながる記事を優先し、見つからないときは各カテゴリの読みものをご紹介します。',
      seasonal: '今の季節に', fallback: 'このカテゴリから',
      empty: '新しい読みものを準備中',
      emptyText: 'ものの背景を知る楽しみ、文化にふれる発見を。記事が加わると、ここでもご紹介します。',
      noMatch: 'この季節の読みものを待ちながら',
      noMatchText: 'カテゴリ一覧では、ほかの季節の読みものもお楽しみいただけます。',
      browse: 'の記事一覧へ', calendar: '日本の季節に合わせて自動で切り替わります。',
      unavailable: '季節別の選書を読み込めなかったため、カテゴリごとの読みものをご紹介しています。'
    },
    en: {
      titles: ['A little inspiration for spring', 'A little inspiration for summer', 'A little inspiration for autumn', 'A little inspiration for winter'],
      periods: ['Mar–May', 'Jun–Aug', 'Sep–Nov', 'Dec–Feb'],
      categories: ['Tea', 'Flowers', 'Ceramics', 'Kimono', 'Food', 'Culture'],
      intro: 'Small pleasures for everyday life. We choose stories with a connection to the season first, then other reading from each category.',
      seasonal: 'For this season', fallback: 'From this category',
      empty: 'More stories on the way',
      emptyText: 'The stories behind objects and discoveries across cultures. New reading will appear here as it is published.',
      noMatch: 'More seasonal reading to come',
      noMatchText: 'Explore this category for stories connected to other seasons.',
      browse: ' stories', calendar: 'Selections change automatically with the seasons in Japan.',
      unavailable: 'Seasonal selections could not be loaded. Here is reading from each category instead.'
    }
  };

  function seasonAt(date) {
    const month = Number(new Intl.DateTimeFormat('en-US', { timeZone: 'Asia/Tokyo', month: 'numeric' }).format(date));
    return month >= 3 && month <= 5 ? 'spring' : month >= 6 && month <= 8 ? 'summer' : month >= 9 && month <= 11 ? 'autumn' : 'winter';
  }

  function slugOf(path) {
    return path.split('/').pop().replace(/(?:\.en)?\.html$/, '');
  }

  function validateRules(data) {
    if (!data || data.version !== 1 || !data.articles || Array.isArray(data.articles) || typeof data.articles !== 'object') throw new Error('Invalid seasonal metadata');
    Object.entries(data.articles).forEach(([slug, rule]) => {
      if (!/^[a-z0-9-]+$/.test(slug) || !rule || !Array.isArray(rule.seasons) || rule.seasons.some(s => !SEASONS.includes(s)) || typeof rule.evergreen !== 'boolean') throw new Error('Invalid article metadata');
      if (rule.seasons.length && (!rule.reason || typeof rule.reason.ja !== 'string' || !rule.reason.ja.trim() || typeof rule.reason.en !== 'string' || !rule.reason.en.trim() || typeof rule.evidence !== 'string' || !rule.evidence.trim())) throw new Error('Seasonal selections need bilingual reasons and evidence');
    });
    return data.articles;
  }

  // Favor a seasonal match, then a different article from those already selected.
  // A cross-category article can still fill both slots if it is the only choice.
  function chooseArticle(articles, category, season, rules, used) {
    const candidates = articles.filter(article => article.categories.includes(category)).map((article, index) => {
      const rule = rules[article.slug];
      const seasonal = !!rule && rule.seasons.includes(season);
      const eligible = !rule || seasonal || rule.evergreen;
      return { article, seasonal, eligible, index };
    }).filter(item => item.eligible);
    candidates.sort((a, b) => Number(b.seasonal) - Number(a.seasonal) || Number(used.has(a.article.slug)) - Number(used.has(b.article.slug)) || b.article.date.localeCompare(a.article.date) || a.index - b.index);
    return candidates[0] || null;
  }

  function readArticles(document) {
    return Array.from(document.querySelectorAll('.story-list > .story-card')).map(card => {
      const title = card.querySelector('.story-copy h2 a, .story-copy h3 a');
      if (!title) return null;
      const url = title.getAttribute('href');
      // Only actual, local article cards may become recommendations.
      if (!/^[a-z0-9-]+(?:\.en)?\.html$/.test(url)) return null;
      const categories = Array.from(card.querySelectorAll('.tags a')).map(link => {
        const match = (link.getAttribute('href') || '').match(/^category-([a-z]+)(?:\.en)?\.html$/);
        return match ? match[1] : null;
      }).filter(category => CATEGORIES.includes(category));
      const date = card.querySelector('.story-copy > small');
      return { slug: slugOf(url), url, categories, card, title, date: date ? date.textContent.trim().replace(/\./g, '-') : '' };
    }).filter(Boolean);
  }

  function element(document, tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }

  function render(document, section, articles, rules, loaded, date) {
    const lang = document.documentElement.lang === 'en' ? 'en' : 'ja';
    const copy = COPY[lang];
    const season = seasonAt(date);
    const seasonIndex = SEASONS.indexOf(season);
    const suffix = lang === 'en' ? '.en.html' : '.html';
    const used = new Set();
    const grid = element(document, 'div', 'seasonal-grid');
    CATEGORIES.forEach((category, index) => {
      const chosen = chooseArticle(articles, category, season, rules, used);
      const card = element(document, 'article', 'seasonal-card');
      card.dataset.category = category;
      const categoryLink = element(document, 'a', 'seasonal-category', `${String(index + 1).padStart(2, '0')} / ${copy.categories[index]}`);
      categoryLink.href = `category-${category}${suffix}`;
      card.append(categoryLink);
      if (chosen) {
        const article = chosen.article;
        used.add(article.slug);
        card.dataset.article = article.slug;
        card.dataset.match = chosen.seasonal ? 'seasonal' : 'category';
        const originalImage = article.card.querySelector('.card-image');
        if (originalImage) {
          const picture = originalImage.cloneNode(true);
          picture.classList.add('seasonal-image');
          picture.querySelectorAll('[id]').forEach(node => node.removeAttribute('id'));
          card.append(picture);
        }
        card.append(element(document, 'p', 'seasonal-label', chosen.seasonal ? copy.seasonal : copy.fallback));
        const heading = element(document, 'h3');
        heading.append(article.title.cloneNode(true));
        card.append(heading);
        const originalDescription = article.card.querySelector('.story-copy > p');
        const description = chosen.seasonal ? rules[article.slug].reason[lang] : originalDescription ? originalDescription.textContent : '';
        card.append(element(document, 'p', 'seasonal-description', description));
      } else {
        card.classList.add('seasonal-empty');
        const hasArticles = articles.some(article => article.categories.includes(category));
        const mark = element(document, 'div', 'seasonal-empty-mark', copy.categories[index]);
        mark.setAttribute('aria-hidden', 'true');
        card.append(mark, element(document, 'p', 'seasonal-label', lang === 'ja' ? 'これからの楽しみ' : 'Coming soon'), element(document, 'h3', '', hasArticles ? copy.noMatch : copy.empty), element(document, 'p', 'seasonal-description', hasArticles ? copy.noMatchText : copy.emptyText));
      }
      const browse = element(document, 'a', 'seasonal-browse', lang === 'ja' ? `${copy.categories[index]}${copy.browse} →` : `All ${copy.categories[index].toLowerCase()}${copy.browse} →`);
      browse.href = categoryLink.href;
      card.append(browse);
      grid.append(card);
    });
    section.querySelector('#seasonal-heading').textContent = copy.titles[seasonIndex];
    section.querySelector('.seasonal-period').textContent = `${season.toUpperCase()} / ${copy.periods[seasonIndex]}`;
    section.querySelector('.seasonal-intro').textContent = loaded ? copy.intro : copy.unavailable;
    section.querySelector('.seasonal-calendar').textContent = copy.calendar;
    section.querySelector('.seasonal-grid').replaceWith(grid);
    section.dataset.season = season;
  }

  async function start(document) {
    const section = document.querySelector('.seasonal-picks');
    if (!section) return;
    const articles = readArticles(document);
    let rules = {}, loaded = false;
    try {
      const response = await fetch('seasonal-picks.json');
      if (!response.ok) throw new Error('Seasonal metadata unavailable');
      rules = validateRules(await response.json());
      loaded = true;
    } catch (_) { /* The complete article archive and category links remain available. */ }
    let renderedSeason;
    const refresh = () => {
      const date = new Date();
      const nextSeason = seasonAt(date);
      if (nextSeason !== renderedSeason) {
        render(document, section, articles, rules, loaded, date);
        renderedSeason = nextSeason;
      }
    };
    refresh();
    // Refresh a tab left open across a seasonal boundary without interrupting it.
    document.addEventListener('visibilitychange', () => { if (!document.hidden) refresh(); });
    root.setInterval(() => { if (!document.hidden) refresh(); }, 60 * 1000);
  }

  const api = { seasonAt, slugOf, validateRules, chooseArticle, readArticles, render };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof document !== 'undefined') start(document);
})(typeof window !== 'undefined' ? window : globalThis);
