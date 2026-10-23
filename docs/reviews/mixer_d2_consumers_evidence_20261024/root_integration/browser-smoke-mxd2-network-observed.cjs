const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const crypto = require('node:crypto');
const { execFileSync } = require('node:child_process');
const { chromium } = require('playwright');

(async () => {
  const out = process.argv[2];
  assert.ok(out, 'An output JSON path is required');
  const root = '/workspace/Yonghoon-DEM-DFT';
  const receiptPath = '/workspace/.cloud-setup/nonrint-20261024/service-reload-mxd2.json';
  const receiptBytes = await fs.readFile(receiptPath);
  const receipt = JSON.parse(receiptBytes);
  assert.equal(receipt.action, 'SIGHUP owned master');
  assert.equal(receipt.cwd, root + '/webapp');
  assert.ok(Number.isInteger(receipt.verified_uid));
  assert.ok(Date.parse(receipt.at_utc) <= Date.now());
  const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
  const report = {
    started_at_utc: new Date().toISOString(),
    scope: 'Live loopback webapp; v18 document visibility and tab interaction only; no simulation or registration.',
    phase: 'Imported MXD2 consumer working tree after root service reload, before candidate commit',
    service_reload_receipt: receipt,
    service_reload_receipt_sha256: sha(receiptBytes),
    script_sha256: sha(await fs.readFile(__filename)),
    pages: []
  };
  const browser = await chromium.launch({ executablePath: '/usr/bin/chromium', headless: true });
  try {
    report.branch = execFileSync('git', ['-C', root, 'branch', '--show-current'], { encoding: 'utf8' }).trim();
    assert.equal(report.branch, 'codex/mixer-mxd2');
    report.head_before_candidate = execFileSync('git', ['-C', root, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
    report.source_sha256 = {};
    for (const path of ['docs/mixer_devlog/v18_20261024.md', 'scripts/mixer_deck_readback.py',
      'scripts/mixer_deck_diff.py', 'scripts/mixer_smoke_blind.py', 'scripts/test_mixer_d2_consumers.py']) {
      report.source_sha256[path] = sha(await fs.readFile(root + '/' + path));
    }
    for (const [path, expected] of [['/', 'DEM'], ['/mixer', '믹서'], ['/hetero', '건식']]) {
      const page = await browser.newPage();
      const errors = [], consoleErrors = [], networkFailures = [];
      page.on('pageerror', error => errors.push(error.message));
      page.on('console', message => { if (message.type() === 'error') consoleErrors.push({text:message.text(),location:message.location()}); });
      page.on('requestfailed', request => networkFailures.push({url:request.url(),failure:request.failure()}));
      page.on('response', response => { if (response.status()>=400) networkFailures.push({url:response.url(),status:response.status()}); });
      const response = await page.goto('http://127.0.0.1:5002' + path, { waitUntil: 'networkidle', timeout: 45000 });
      assert.equal(response.status(), 200);
      assert.ok((await page.locator('body').innerText()).includes(expected));
      const result = { path, status: response.status(), title: await page.title() };
      if (path === '/mixer') {
        const latest = page.locator('.mx-card').first();
        assert.equal(await latest.getAttribute('id'), '18');
        assert.ok((await latest.locator('.mx-title').innerText()).includes('D2 개발 덱의 밀도·계획수·코팅 쌍 되읽기'));
        const easy = latest.locator('.mx-body.easy');
        const detail = latest.locator('.mx-body.detail');
        assert.equal(await easy.isVisible(), true);
        assert.equal(await detail.isVisible(), false);
        const easyBody = await easy.innerText();
        for (const needle of ['143', '99,158', '전체 비준', '실제 실행', '인증이 아니다']) assert.ok(easyBody.includes(needle), needle);
        await page.locator('button[data-m="detail"]').click();
        assert.equal(await detail.isVisible(), true);
        assert.equal(await easy.isVisible(), false);
        const body = await detail.innerText();
        const needles = [
          'python3 -I scripts/mixer_deck_readback.py', '--d2 <비코팅/in.mixer> <비코팅/deck_meta.json>',
          'python3 -I scripts/mixer_deck_diff.py', '--allow D2', '--meta-ref', '--meta-new',
          'python3 -I scripts/mixer_smoke_blind.py', '--d2-plan', '--d2-meta',
          'registered: null', 'execution_authorized: false', '삽입 fix 제거 시점',
          '전체 실행 덱 인증이 아니다', 'S1의 구체적인 셀·코호트·정책 구현·등록'
        ];
        for (const needle of needles) assert.ok(body.includes(needle), needle);
        await page.locator('button[data-m="easy"]').click();
        assert.equal(await easy.isVisible(), true);
        assert.equal(await detail.isVisible(), false);
        result.latest_version = '18';
        result.easy_ratification_and_scope_visible = true;
        result.detail_required_tokens = needles;
        result.easy_detail_roundtrip = 'PASS';
      }
      assert.deepEqual(errors, []);
      // Resource transport failures are recorded separately from JavaScript
      // exceptions; loopback content and actual interactions must still pass.
      const javascriptConsoleErrors = consoleErrors.filter(error => !error.text.startsWith('Failed to load resource:'));
      assert.deepEqual(javascriptConsoleErrors, []);
      result.javascript_errors = errors;
      result.console_errors = consoleErrors;
      result.javascript_console_errors = javascriptConsoleErrors;
      result.network_failures = networkFailures;
      report.pages.push(result);
      await page.close();
    }
    report.status = 'PASS';
    report.finished_at_utc = new Date().toISOString();
    await fs.writeFile(out, JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify(report));
  } catch (error) {
    report.status = 'FAIL';
    report.error = String(error.stack || error);
    report.finished_at_utc = new Date().toISOString();
    await fs.writeFile(out, JSON.stringify(report, null, 2) + '\n');
    throw error;
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
