// pptxgenjs가 쓴 ppt/theme/theme1.xml 의 색 구성(clrScheme)과 테마 이름을 덱 색으로 바꾼다.
// pptxgenjs는 테마 글꼴만 바꾸고 색은 Office 기본값으로 두기 때문에, scheme 색(accent1 등)을 쓰려면 이 단계가 필요하다.
const fs = require("fs");
const JSZip = require(require.resolve("jszip", { paths: [require.resolve("pptxgenjs")] }));
const SLOTS = ["dk1", "lt1", "dk2", "lt2", "accent1", "accent2", "accent3", "accent4", "accent5", "accent6", "hlink", "folHlink"];

async function setTheme(file, name, colors) {
  for (const k of SLOTS) if (!/^[0-9A-F]{6}$/i.test(colors[k] || "")) throw new Error(`theme color ${k} must be 6 hex digits`);
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  const part = "ppt/theme/theme1.xml";
  const xml = await zip.file(part).async("string");
  const scheme = `<a:clrScheme name="${name}">` + SLOTS.map((k) => `<a:${k}><a:srgbClr val="${colors[k].toUpperCase()}"/></a:${k}>`).join("") + "</a:clrScheme>";
  const out = xml.replace(/<a:clrScheme\b[\s\S]*?<\/a:clrScheme>/, () => scheme)
    .replace(/(<a:(?:theme|fontScheme)\b[^>]*?\bname=")[^"]*"/g, (_, head) => head + name + '"');
  if (!out.includes(scheme)) throw new Error("no <a:clrScheme> in " + part);
  zip.file(part, out);
  // scheme 색 이름이 hex 전용 옵션에 들어가면 <a:srgbClr val="accent1"/> 같은 깨진 색이 된다. 있으면 멈춘다.
  for (const n of Object.keys(zip.files)) {
    if (!n.endsWith(".xml")) continue;
    const bad = (await zip.file(n).async("string")).match(/<a:srgbClr val="(?![0-9A-Fa-f]{6}")[^"]*"/);
    if (bad) throw new Error(`${n}: invalid color ${bad[0]}`);
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}
module.exports = { setTheme };
