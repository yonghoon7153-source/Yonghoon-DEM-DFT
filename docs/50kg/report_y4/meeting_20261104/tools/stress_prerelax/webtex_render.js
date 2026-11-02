// 웹앱 질감 렌더 — node webtex_render.js <root> <specs.json>  (Playwright Chromium · SwiftShader WebGL · 로컬 http 만)
const { chromium } = require('playwright');
const http = require('http'); const fs = require('fs'); const path = require('path');
const root = path.resolve(process.argv[2]); const specs = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const types = { '.js': 'text/javascript', '.html': 'text/html', '.bin': 'application/octet-stream' };
const srv = http.createServer((req, res) => {
  const p = path.resolve(path.join(root, decodeURIComponent(req.url.split('?')[0])));
  if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.statusCode = 404; return res.end(); }
  res.setHeader('Content-Type', types[path.extname(p)] || 'application/octet-stream'); fs.createReadStream(p).pipe(res);
});
srv.listen(0, '127.0.0.1', async () => {
  const port = srv.address().port;
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  try {
    for (const s of specs) {
      const page = await browser.newPage({ viewport: { width: s.W, height: s.H } });
      page.on('pageerror', e => console.log('[pageerror]', e.message));
      await page.goto(`http://127.0.0.1:${port}/render.html`);
      await page.waitForFunction(() => window.ready === true, null, { timeout: 60000 });
      const url = await page.evaluate(async (s) => await window.render(s), s);
      fs.writeFileSync(s.out, Buffer.from(url.split(',')[1], 'base64'));
      console.log('wrote', s.out); await page.close();
    }
  } finally { await browser.close(); srv.close(); }
});
