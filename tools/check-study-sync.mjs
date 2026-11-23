// Browser Web Crypto contract tests with synthetic data only; no private files or remote service.
import assert from 'node:assert/strict';
import { createCipheriv, createHash, randomBytes, randomUUID } from 'node:crypto';
import { createRequire } from 'node:module';
import { build } from 'esbuild';

const { chromium } = createRequire(import.meta.url)(process.env.PLAYWRIGHT_MODULE || 'playwright');
const { outputFiles } = await build({ entryPoints: ['src/ui/study-sync.ts'], bundle: true,
  format: 'iife', globalName: 'StudySync', write: false, platform: 'browser' });
const secret = randomBytes(32);
const profile = { schemaVersion: 1, kind: 'nihonchizu-study-connection', feedId: randomUUID(),
  deckId: 'test-deck', url: '/study-feed/my-deck.v1.enc.json', key: secret.toString('base64url') };
const deck = { schemaVersion: 1, deckId: 'test-deck', title: '합성 검증 자료',
  cards: [{ id: 'one', ja: 'こんにちは', en: 'Hello.', ko: '안녕하세요.' }] };
function encrypt(data = deck, revisionOverride) {
  const bytes = Buffer.from(JSON.stringify(data));
  const revision = revisionOverride || createHash('sha256').update(bytes).digest('hex');
  const iv = randomBytes(12);
  const cipher = createCipheriv('aes-256-gcm', secret, iv);
  cipher.setAAD(Buffer.from(`nihonchizu-encrypted-deck:1:${profile.feedId}:${revision}`));
  const ciphertext = Buffer.concat([cipher.update(bytes), cipher.final(), cipher.getAuthTag()]);
  return { schemaVersion: 1, kind: 'nihonchizu-encrypted-deck', feedId: profile.feedId,
    revision, updatedAt: '2026-11-21T12:00:00.000Z', iv: iv.toString('base64url'), ciphertext: ciphertext.toString('base64url') };
}
const good = encrypt();
let payload = good, status = 200, redirected = false;
const requests = [];
const browser = await chromium.launch();
try {
  const page = await browser.newPage();
  await page.route('http://localhost:43117/**', async (route) => {
    const request = route.request();
    if (new URL(request.url()).pathname === '/') {
      await route.fulfill({ status: 200, contentType: 'text/html', body: '<!doctype html><title>Local contract test</title>' });
    } else {
      requests.push({ url: request.url(), headers: request.headers(), body: request.postData() });
      await route.fulfill({ status: redirected ? 302 : status, headers: redirected ? { location: '/redirected' } : {},
        contentType: 'application/json', body: JSON.stringify(payload) });
    }
  });
  await page.goto('http://localhost:43117/');
  await page.addScriptTag({ content: outputFiles[0].text });
  const fetchResult = (connection = profile) => page.evaluate(async (connection) => {
    try { return { ok: true, result: await StudySync.fetchStudyDeck(connection) }; }
    catch (error) { return { ok: false, message: error.message, name: error.name }; }
  }, connection);
  const ok = await fetchResult();
  assert.equal(ok.ok, true); assert.equal(ok.result.deck.cards[0].ja, 'こんにちは');
  assert.equal(ok.result.revision, good.revision);
  assert.ok(!JSON.stringify(requests).includes(profile.key));
  assert.ok(requests.every((r) => r.url === 'http://localhost:43117/study-feed/my-deck.v1.enc.json' && r.body === null));
  let rejected = 0;
  async function fails(connection = profile) {
    const result = await fetchResult(connection); assert.equal(result.ok, false);
    assert.ok(!result.message.includes(profile.key));
    assert.match(result.message, /단어장/); rejected++;
  }
  await fails({ ...profile, key: 'A'.repeat(43) });
  await fails({ ...profile, key: 'A'.repeat(42) + 'B' }); // Nonzero unused padding bits.
  await fails({ ...profile, key: profile.key + '=' });
  for (const url of ['https://example.com/feed', '//example.com/feed', profile.url + '?key=x', profile.url + '#x']) {
    await fails({ ...profile, url });
  }
  payload = { ...good, ciphertext: (good.ciphertext[0] === 'A' ? 'B' : 'A') + good.ciphertext.slice(1) }; await fails();
  payload = { ...good, feedId: randomUUID() }; await fails();
  payload = { ...good, iv: randomBytes(16).toString('base64url') }; await fails();
  payload = { ...good, ciphertext: 'AA' }; await fails();
  payload = { ...good, updatedAt: '2026-02-30T12:00:00Z' }; await fails();
  payload = encrypt({ ...deck, deckId: 'other-deck' }); await fails();
  payload = encrypt(deck, '0'.repeat(64)); await fails(); // Valid AES tag, incorrect plaintext hash.
  payload = encrypt({ ...deck, cards: [] }); await fails();
  for (const ja of [{ 32: ['one'] }, { 2: ['missing'] }, { 2: ['one', 'one'] }]) {
    payload = encrypt({ ...deck, today: { ja, en: {} } }); await fails();
  }
  payload = good; status = 404; await fails(); status = 200;
  redirected = true; await fails(); redirected = false;
  const transport = await page.evaluate(async ({ profile, good }) => {
    const nativeFetch = globalThis.fetch, observations = [];
    const limit = 16 * 1024 * 1024, encoder = new TextEncoder();
    let cancelled = false, opts;
    try {
      globalThis.fetch = async (_url, options) => {
        opts = options;
        return new Response(new ReadableStream({
          pull(controller) { controller.enqueue(new Uint8Array(1024 * 1024)); },
          cancel() { cancelled = true; },
        }));
      };
      try { await StudySync.fetchStudyDeck(profile); observations.push('unexpected-size-success'); }
      catch { observations.push('stream-limit-rejected'); }
      const options = { credentials: opts.credentials, cache: opts.cache, redirect: opts.redirect, mode: opts.mode,
        referrerPolicy: opts.referrerPolicy, includesKey: JSON.stringify(opts).includes(profile.key) };
      const exact = JSON.stringify(good), pad = limit - encoder.encode(exact).byteLength;
      globalThis.fetch = async () => new Response(exact + ' '.repeat(pad));
      const result = await StudySync.fetchStudyDeck(profile);
      observations.push(result.deck.deckId === profile.deckId ? 'exact-limit-accepted' : 'wrong-deck');
      const controller = new AbortController(); controller.abort();
      try { await StudySync.fetchStudyDeck(profile, controller.signal); }
      catch (error) { observations.push(error.name); }
      return { observations, options, cancelled };
    } finally { globalThis.fetch = nativeFetch; }
  }, { profile, good });
  assert.deepEqual(transport.observations, ['stream-limit-rejected', 'exact-limit-accepted', 'AbortError']);
  assert.deepEqual(transport.options, { credentials: 'omit', cache: 'no-store', redirect: 'error', mode: 'same-origin', referrerPolicy: 'no-referrer', includesKey: false });
  assert.equal(transport.cancelled, true);
  console.log(JSON.stringify({ passed: ['Node encryption/browser decryption', `${rejected} invalid inputs rejected`,
    'fixed same-origin request without key', '16 MiB exact/oversize stream', 'request options', 'AbortError'], privateDataUsed: false }, null, 2));
} finally { await browser.close(); }
