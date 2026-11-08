const assert = require('node:assert/strict');
const fs = require('node:fs');
const test = require('node:test');
const { seasonAt, slugOf, validateRules, chooseArticle } = require('../seasonal-picks.js');
const data = JSON.parse(fs.readFileSync(require('node:path').join(__dirname, '../seasonal-picks.json'), 'utf8'));
const article = (slug, categories = ['tea'], date = '2026-11-08') => ({ slug, categories, date });

test('all twelve months follow Japanese meteorological seasons', () => {
  const expected = ['winter','winter','spring','spring','spring','summer','summer','summer','autumn','autumn','autumn','winter'];
  expected.forEach((season, index) => assert.equal(seasonAt(new Date(`2026-${String(index+1).padStart(2,'0')}-15T12:00:00Z`)), season));
});
test('season transitions use Tokyo midnight, regardless of visitor timezone', () => {
  for (const [month, before, after] of [[3,'winter','spring'],[6,'spring','summer'],[9,'summer','autumn'],[12,'autumn','winter']]) {
    const boundary = Date.parse(`2026-${String(month).padStart(2,'0')}-01T00:00:00+09:00`);
    assert.equal(seasonAt(new Date(boundary - 1)), before);
    assert.equal(seasonAt(new Date(boundary)), after);
  }
});
test('both language URLs share one editorial record', () => {
  assert.equal(slugOf('food-wagashi-names.en.html'), 'food-wagashi-names');
  assert.equal(slugOf('food-wagashi-names.html'), 'food-wagashi-names');
});
test('metadata has supported seasons, bilingual reasons and evidence', () => {
  assert.deepEqual(validateRules(data), data.articles);
  assert.throws(() => validateRules({version:1,articles:{test:{seasons:['rainy'],evergreen:true}}}));
  assert.throws(() => validateRules({version:1,articles:{test:{seasons:['autumn'],evergreen:true}}}));
});
test('seasonal matches win over newer category reading', () => {
  const list = [article('new'), article('seasonal')];
  const rules = {seasonal:{seasons:['autumn'],evergreen:false}};
  assert.equal(chooseArticle(list,'tea','autumn',rules,new Set()).article.slug, 'seasonal');
  assert.equal(chooseArticle(list,'tea','spring',rules,new Set()).article.slug, 'new');
});
test('avoid repeated cross-category picks when another eligible story exists', () => {
  const list = [article('shared',['tea','ceramics']),article('other',['ceramics'])];
  assert.equal(chooseArticle(list,'ceramics','spring',{},new Set(['shared'])).article.slug, 'other');
  assert.equal(chooseArticle(list.slice(0,1),'ceramics','spring',{},new Set(['shared'])).article.slug, 'shared');
});
test('empty and out-of-season-only categories do not invent a recommendation', () => {
  assert.equal(chooseArticle([],'ideas','winter',{},new Set()), null);
  assert.equal(chooseArticle([article('spring')],'tea','winter',{spring:{seasons:['spring'],evergreen:false}},new Set()), null);
});
test('new articles enter automatically and metadata cannot publish absent cards', () => {
  assert.equal(chooseArticle([article('old'),article('new',['tea'],'2026-11-09')],'tea','winter',{},new Set()).article.slug, 'new');
  assert.equal(chooseArticle([],'tea','winter',{draft:{seasons:['winter'],evergreen:true}},new Set()), null);
});
test('production autumn picks are grounded in published article text', () => {
  for (const slug of Object.keys(data.articles)) for (const suffix of ['.html','.en.html']) assert.ok(fs.existsSync(require('node:path').join(__dirname, `../${slug}${suffix}`)));
  const list = [article('between-tea-and-ceramics',['tea','ceramics']),article('ceramics-banko',['ceramics'])];
  assert.equal(chooseArticle(list,'ceramics','autumn',data.articles,new Set(['between-tea-and-ceramics'])).article.slug,'ceramics-banko');
});
