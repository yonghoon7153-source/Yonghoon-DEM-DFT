// Tiny DOM helpers so we never touch innerHTML with data.
export function el<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  attrs: Record<string, string | undefined> = {},
  ...children: (Node | string | null | undefined | false)[]
): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v === undefined) continue;
    if (k === 'class') node.className = v;
    else if (k === 'style') node.setAttribute('style', v);
    else if (k.startsWith('on')) continue;
    else node.setAttribute(k, v);
  }
  for (const c of children) {
    if (c === null || c === undefined || c === false) continue;
    node.append(typeof c === 'string' ? document.createTextNode(c) : c);
  }
  return node;
}

export function clear(node: HTMLElement) {
  while (node.firstChild) node.removeChild(node.firstChild);
}

/** <ruby>漢字<rt>かな</rt></ruby> when a reading exists, plain text otherwise. */
export function ruby(ja: string, kana?: string): Node {
  if (!kana || kana === ja) return document.createTextNode(ja);
  const r = document.createElement('ruby');
  r.lang = 'ja';
  r.append(ja);
  const rt = document.createElement('rt');
  rt.textContent = kana;
  r.append(rt);
  return r;
}
