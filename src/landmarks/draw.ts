// Draws the landmark stickers (ADR 0011). Their pictures (src/landmarks/art-*.ts, over 170 of them) load the first time
// a sticker is needed — the first screen never shows one — so the page itself stays light.
const SVG_NS = 'http://www.w3.org/2000/svg';
let art: Record<string, string> | null = null;
let loading: Promise<void> | null = null;
let parser: DOMParser | null = null;

/** Loads the sticker pictures once; resolves at once after the first time. */
export function loadLandmarkArt(): Promise<void> {
  loading ??= import('./art').then((m) => { art = m.landmarkArt; });
  return loading;
}

export const landmarkArtReady = (): boolean => art !== null;

/**
 * Draws a sticker into `target` (a 100×100 box): the white cut-out edge — the same drawing again, thickly outlined in
 * white by app.css — under the drawing itself. Used by the map and the 東京23区 popup alike. False (nothing drawn)
 * while the pictures are not loaded yet.
 */
export function drawLandmark(target: SVGGElement, icon: string): boolean {
  if (!art) return false;
  parser ??= new DOMParser();
  const inner = art[icon] ?? '';
  for (const cls of ['landmark__edge', 'landmark__ink']) {
    const g = document.createElementNS(SVG_NS, 'g');
    g.setAttribute('class', cls);
    const doc = parser.parseFromString(`<svg xmlns="${SVG_NS}">${inner}</svg>`, 'image/svg+xml');
    for (const child of Array.from(doc.documentElement.childNodes)) g.appendChild(document.importNode(child, true));
    target.appendChild(g);
  }
  return true;
}
