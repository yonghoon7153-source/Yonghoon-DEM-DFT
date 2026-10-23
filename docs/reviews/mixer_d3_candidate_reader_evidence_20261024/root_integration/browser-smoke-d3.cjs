const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const crypto = require('node:crypto');
const { execFileSync } = require('node:child_process');
const { chromium } = require('playwright');

(async () => {
  const out = process.argv[2];
  assert.ok(out, 'An output JSON path is required');
  const source = '/workspace/Yonghoon-DEM-DFT/docs/mixer_devlog/v19_20261024.md';
  const browser = await chromium.launch({executablePath:'/usr/bin/chromium',headless:true});
  const report = {started_at_utc:new Date().toISOString(),scope:'Live loopback webapp; document visibility and tab interaction only; no simulation or registration.',phase:'Imported D3 reader working tree before candidate commit',pages:[]};
  try {
    report.branch = execFileSync('git',['-C','/workspace/Yonghoon-DEM-DFT','branch','--show-current'],{encoding:'utf8'}).trim();
    assert.equal(report.branch,'codex/mixer-d3-design');
    report.head_before_candidate = execFileSync('git',['-C','/workspace/Yonghoon-DEM-DFT','rev-parse','HEAD'],{encoding:'utf8'}).trim();
    report.devlog_sha256 = crypto.createHash('sha256').update(await fs.readFile(source)).digest('hex');
    report.reader_sha256 = crypto.createHash('sha256').update(await fs.readFile('/workspace/Yonghoon-DEM-DFT/scripts/mixer_d3_candidates.py')).digest('hex');
    for (const [path, expected] of [['/','DEM'],['/mixer','믹서'],['/hetero','건식']]) {
      const page = await browser.newPage();
      const errors = [];
      page.on('pageerror', e => errors.push(e.message));
      const response = await page.goto('http://127.0.0.1:5002'+path,{waitUntil:'networkidle',timeout:45000});
      assert.equal(response.status(),200);
      assert.ok((await page.locator('body').innerText()).includes(expected));
      const result = {path,status:response.status(),title:await page.title()};
      if (path === '/mixer') {
        const latest = page.locator('.mx-card').first();
        assert.equal(await latest.getAttribute('id'),'19');
        assert.ok((await latest.locator('.mx-title').innerText()).includes('D3 유한 후보 판독기'));
        const easy = latest.locator('.mx-body.easy');
        assert.equal(await easy.isVisible(),true);
        assert.ok((await easy.innerText()).includes('개발 단계'));
        await page.locator('button[data-m="detail"]').click();
        const detail = latest.locator('.mx-body.detail');
        assert.equal(await detail.isVisible(),true);
        assert.equal(await easy.isVisible(),false);
        const body = await detail.innerText();
        const needles = ['python3 -I scripts/mixer_d3_candidates.py','--contract','--observations','UNASSESSED','all-compatible / mixed / none-compatible / incomplete','V2-Q1–Q4','비준'];
        for (const needle of needles) assert.ok(body.includes(needle),needle);
        await page.locator('button[data-m="easy"]').click();
        assert.equal(await easy.isVisible(),true);
        assert.equal(await detail.isVisible(),false);
        result.latest_version='19';
        result.easy_development_label_visible=true;
        result.detail_required_tokens=needles;
        result.easy_detail_roundtrip='PASS';
      }
      assert.deepEqual(errors,[]);
      result.javascript_errors=errors;
      report.pages.push(result);
      await page.close();
    }
    report.status='PASS';
    report.finished_at_utc=new Date().toISOString();
    await fs.writeFile(out,JSON.stringify(report,null,2)+'\n');
    console.log(JSON.stringify(report));
  } catch (error) {
    report.status='FAIL';
    report.error=String(error.stack || error);
    report.finished_at_utc=new Date().toISOString();
    await fs.writeFile(out,JSON.stringify(report,null,2)+'\n');
    throw error;
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode=1; });
