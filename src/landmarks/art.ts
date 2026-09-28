// Landmark stickers (ADR 0011): look-alikes of the places in my mind map and 보충, and of the 기본 정보 観光 spots (#93),
// keyed by data/landmarks.json `icon`. Each value is the inside of a 100×100 SVG. Split by file to keep each readable:
// art-a · art-b — my boxes (east · west) and the shared kinds; art-c ~ art-f — the 観光 spots, by region.
// Loaded on demand by ./draw (its own chunk), not imported directly.
import { artA } from './art-a';
import { artB } from './art-b';
import { artC } from './art-c';
import { artD } from './art-d';
import { artE } from './art-e';
import { artF } from './art-f';

export const landmarkArt: Record<string, string> = { ...artA, ...artB, ...artC, ...artD, ...artE, ...artF };
