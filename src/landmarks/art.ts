// Landmark stickers (ADR 0011): look-alikes of the places in my mind map and 보충, keyed by data/landmarks.json `icon`.
// Each value is the inside of a 100×100 SVG. Split in two files to keep each readable.
import { artA } from './art-a';
import { artB } from './art-b';

export const landmarkArt: Record<string, string> = { ...artA, ...artB };

const SVG_NS = 'http://www.w3.org/2000/svg';
let parser: DOMParser | null = null;

/**
 * Draws a sticker into `target` (a 100×100 box): the white cut-out edge — the same drawing again, thickly outlined in
 * white by app.css — under the drawing itself. Used by the map and the 東京23区 popup alike.
 */
export function drawLandmark(target: SVGGElement, icon: string): void {
  parser ??= new DOMParser();
  const inner = landmarkArt[icon] ?? '';
  for (const cls of ['landmark__edge', 'landmark__ink']) {
    const g = document.createElementNS(SVG_NS, 'g');
    g.setAttribute('class', cls);
    const doc = parser.parseFromString(`<svg xmlns="${SVG_NS}">${inner}</svg>`, 'image/svg+xml');
    for (const child of Array.from(doc.documentElement.childNodes)) g.appendChild(document.importNode(child, true));
    target.appendChild(g);
  }
}
