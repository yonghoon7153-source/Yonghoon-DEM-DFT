// md(+TeX) → standalone HTML (KaTeX server-side) — usage: node build_html.mjs in.md out.html fontdir katexdir
import fs from 'fs';
import path from 'path';
import katex from 'katex';
import { marked } from 'marked';
const [,, inp, out, fontdir, katexdir] = process.argv;
let src = fs.readFileSync(inp, 'utf8');
const store = [];
const put = (html) => { store.push(html); return `@@MATH${store.length - 1}@@`; };
// display math $$...$$ (may span lines)
src = src.replace(/\$\$([\s\S]+?)\$\$/g, (_, tex) => put(katex.renderToString(tex.trim(), { displayMode: true, throwOnError: true, strict: 'ignore' })));
// inline math $...$ (no newline, not escaped)
src = src.replace(/(^|[^\\$])\$([^\n$]+?)\$/g, (m, pre, tex) => pre + put(katex.renderToString(tex, { displayMode: false, throwOnError: true, strict: 'ignore' })));
// pandoc 그림 크기 꼴 ![alt](src){width=NN%} → HTML img (marked 는 속성 문법을 모른다)
src = src.replace(/!\[([^\]]*)\]\(([^)\s]+)\)\{width=(\d+)%\}/g, (_, alt, s, w) => `<p class="fig"><img alt="${alt}" src="${s}" style="width:${w}%"></p>`);
marked.setOptions({ gfm: true });
let body = marked.parse(src);
body = body.replace(/@@MATH(\d+)@@/g, (_, i) => store[+i]);
const css = fs.readFileSync(path.join(katexdir, 'katex.min.css'), 'utf8').replace(/url\(fonts\//g, `url(file://${katexdir}/fonts/`);
const html = `<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>report</title>
<style>${css}</style>
<style>
@font-face{font-family:'NSKR';src:url(file://${fontdir}/NotoSansKR-400.ttf);font-weight:400}
@font-face{font-family:'NSKR';src:url(file://${fontdir}/NotoSansKR-700.ttf);font-weight:700}
@page{size:A4;margin:18mm 17mm 18mm 17mm;@bottom-center{content:counter(page)}}
html{font-family:'NSKR',sans-serif;font-size:10pt;line-height:1.62;color:#111}
body{margin:0;overflow-wrap:break-word}
h1{font-size:16pt;line-height:1.35;margin:0 0 4pt 0}
h2{font-size:13pt;margin:20pt 0 6pt 0;padding-bottom:2pt;border-bottom:1px solid #999;break-after:avoid}
h3{font-size:11pt;margin:14pt 0 4pt 0;break-after:avoid}
h4{font-size:10pt;margin:10pt 0 3pt 0;break-after:avoid}
p{margin:4pt 0 6pt 0;text-align:justify}
ul,ol{margin:3pt 0 6pt 0;padding-left:16pt} li{margin:1.5pt 0}
table{border-collapse:collapse;width:100%;margin:6pt 0 10pt 0;font-size:8.6pt;line-height:1.42;break-inside:auto}
thead{display:table-header-group} tr{break-inside:avoid}
th,td{border-top:0.6pt solid #888;border-bottom:0.6pt solid #888;padding:3pt 4pt;vertical-align:top;text-align:left;overflow-wrap:break-word}
th{background:#f0f0f0;font-weight:700}
code{font-family:'DejaVu Sans Mono',monospace;font-size:8.3pt;background:#f4f4f4;padding:0 2pt;border-radius:2pt;overflow-wrap:anywhere;word-break:break-word}
pre{background:#f6f6f6;border:0.5pt solid #ccc;padding:5pt 7pt;font-size:7.8pt;line-height:1.35;overflow-wrap:anywhere;white-space:pre-wrap;break-inside:avoid}
pre code{background:none;padding:0}
blockquote{margin:6pt 0;padding:4pt 9pt;border-left:2.5pt solid #777;background:#fafafa;color:#222}
.katex{font-size:1.05em} .katex-display{margin:7pt 0}
img{max-width:100%} p.fig{text-align:center;margin:8pt 0 2pt 0;break-inside:avoid} figure{margin:8pt 0 10pt 0;text-align:center;break-inside:avoid} figcaption{font-size:8.8pt;color:#333;text-align:left;margin-top:3pt}
hr{border:0;border-top:0.6pt solid #aaa;margin:12pt 0}
.meta{font-size:8.8pt;color:#333}
</style></head><body>${body}</body></html>`;
fs.writeFileSync(out, html);
console.log('html', out, html.length);
