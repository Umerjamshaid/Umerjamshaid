import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {join} from 'node:path';
import test from 'node:test';

const root = process.env.METRICS_SOURCE;
assert.ok(root, 'Set METRICS_SOURCE to the patched original source checkout');
const loadPlugin = async (name) => {
  let source = await readFile(join(root, 'source/plugins', name, 'index.mjs'), 'utf8');
  // The language analyzer is unused for push events without commit details.
  source = source.replace(/^import .*recent_analyzer.*$/m, 'const recent_analyzer = () => { throw new Error("Unexpected analyzer call") }');
  return (await import(`data:text/javascript,${encodeURIComponent(source)}`)).default;
};
const metadata = (name, options) => ({plugins: {[name]: {
  enabled: () => true,
  inputs: () => options,
  extras: () => false,
}}});
const filters = {repo: () => true};
const format = {error: (error) => error};

test('habits handles missing commit arrays, null commits, and commits without authors', async () => {
  const plugin = await loadPlugin('habits');
  const payloads = [{}, {commits: null}, {commits: [null, {}]}];
  const events = payloads.map(payload => ({
    type: 'PushEvent', actor: {login: 'Umerjamshaid'}, repo: {name: 'Umerjamshaid/demo'},
    created_at: new Date().toISOString(), payload,
  }));
  const result = await plugin({
    login: 'Umerjamshaid', account: 'user', q: {habits: true},
    data: {config: {}, shared: {'repositories.skipped': [], 'commits.authoring': ['umerjamshaid']}},
    rest: {activity: {listEventsForAuthenticatedUser: async () => ({data: events})}},
    imports: {metadata: metadata('habits', {from: 100, days: 14, charts: false,
      'languages.threshold': '0%', skipped: []}), filters, format},
  }, {enabled: true});
  assert.equal(result.commits.fetched, 3);
  assert.equal(Object.values(result.commits.days).filter(Number.isFinite).length > 0, true);
});

test('lines counts only the owner and tolerates deleted contributor accounts', async () => {
  const plugin = await loadPlugin('lines');
  const stats = [
    {author: null, weeks: [{a: 100, d: 50, c: 20, w: 1700000000}]},
    {author: {login: 'Umerjamshaid'}, weeks: [{a: 7, d: 2, c: 1, w: 1700000000}]},
    {author: {login: 'someone-else'}, weeks: [{a: 200, d: 20, c: 10, w: 1700000000}]},
  ];
  const result = await plugin({
    login: 'Umerjamshaid', account: 'user', q: {lines: true},
    data: {account: 'user', shared: {'repositories.skipped': []},
      user: {repositories: {nodes: [{name: 'demo', owner: {login: 'Umerjamshaid'}}]}}},
    rest: {repos: {getContributorsStats: async () => ({data: stats})}},
    imports: {metadata: metadata('lines', {skipped: [], sections: ['repositories'],
      'repositories.limit': 4, delay: 0}), filters, format},
  }, {enabled: true});
  assert.equal(result.added, 7);
  assert.equal(result.deleted, 2);
  assert.equal(result.changed, 1);
});

test('achievements keeps its response alias while replacing the retired Projects field', async () => {
  const query = await readFile(join(root, 'source/plugins/achievements/queries/achievements.graphql'), 'utf8');
  assert.doesNotMatch(query, /\bprojects\s*\(/);
  assert.match(query, /projects:\s*projectsV2\(/);
});
