// 🎆 One-shot effects that match a festival's feel (v2): fireworks over a prefecture, snow, petals, leaves,
// lantern glow, drum rings, tanabata streamers. Pure DOM + CSS animations, gone after a few seconds.
// The layer's data-fx also tints the whole stage for the moment (night for fireworks, dusk for lanterns…), see app.css.
import { el } from './dom';

export type FxKind = 'fireworks' | 'snow' | 'sakura' | 'momiji' | 'lanterns' | 'drums' | 'streamers';
const KINDS: FxKind[] = ['fireworks', 'snow', 'sakura', 'momiji', 'lanterns', 'drums', 'streamers'];
export const isFxKind = (s: string): s is FxKind => (KINDS as string[]).includes(s);

const rnd = (a: number, b: number) => a + Math.random() * (b - a);
const PALETTE = ['#e5708d', '#f2b84b', '#6fb0a6', '#4a9fd8', '#c9a6e6', '#fffdf9'];
type Pt = { x: number; y: number };

export function createFx(root: HTMLElement) {
  let timer = 0;
  function clear() {
    root.replaceChildren();
    delete root.dataset.fx;
  }
  function clearSoon(ms: number) {
    window.clearTimeout(timer);
    timer = window.setTimeout(clear, ms);
  }
  /** Sparks flying out of a point: four bursts around `at` (the prefecture on the map), one after another. */
  function fireworks(at: Pt) {
    for (let b = 0; b < 4; b++) {
      const cx = at.x + rnd(-90, 90), cy = at.y + rnd(-130, -20);
      const color = PALETTE[b % PALETTE.length]!;
      const delay = b * 380;
      for (let i = 0; i < 26; i++) {
        const a = (Math.PI * 2 * i) / 26 + rnd(-0.1, 0.1);
        const d = rnd(64, 124);
        root.append(el('span', { class: 'fx fx--spark', style: `left:${cx.toFixed(0)}px;top:${cy.toFixed(0)}px;--dx:${(Math.cos(a) * d).toFixed(0)}px;--dy:${(Math.sin(a) * d).toFixed(0)}px;--c:${color};animation-delay:${delay}ms` }));
      }
      root.append(el('span', { class: 'fx fx--flash', style: `left:${cx.toFixed(0)}px;top:${cy.toFixed(0)}px;--c:${color};animation-delay:${delay}ms` }));
    }
    clearSoon(3400);
  }
  /** Things falling across the whole stage: snow, petals, leaves, streamers. */
  function fall(cls: string, n: number, dur: [number, number], extra: (i: number) => string = () => '') {
    const W = root.clientWidth || 800;
    for (let i = 0; i < n; i++) {
      root.append(el('span', { class: `fx ${cls}`, style: `left:${rnd(0, W).toFixed(0)}px;--dur:${rnd(dur[0], dur[1]).toFixed(2)}s;animation-delay:${rnd(0, 1200).toFixed(0)}ms;${extra(i)}` }));
    }
    clearSoon(dur[1] * 1000 + 1400);
  }
  /** Warm lights drifting up around the prefecture. */
  function lanterns(at: Pt) {
    for (let i = 0; i < 18; i++) {
      root.append(el('span', { class: 'fx fx--lantern', style: `left:${(at.x + rnd(-110, 110)).toFixed(0)}px;top:${(at.y + rnd(-10, 50)).toFixed(0)}px;--dur:${rnd(2.4, 3.6).toFixed(2)}s;animation-delay:${rnd(0, 1000).toFixed(0)}ms;--s:${rnd(0.7, 1.4).toFixed(2)}` }));
    }
    clearSoon(4800);
  }
  /** Drum beats: rings spreading from the prefecture in time, notes jumping up beside it. */
  function drums(at: Pt) {
    for (let i = 0; i < 6; i++) {
      root.append(el('span', { class: 'fx fx--ring', style: `left:${at.x.toFixed(0)}px;top:${at.y.toFixed(0)}px;animation-delay:${i * 380}ms;--c:${PALETTE[i % 3]}` }));
      root.append(el('span', { class: 'fx fx--beat', style: `left:${(at.x + (i % 2 ? 56 : -56)).toFixed(0)}px;top:${(at.y - 70).toFixed(0)}px;animation-delay:${i * 380}ms;--c:${PALETTE[(i + 1) % 3]}` }, i % 2 ? '♪' : '♫'));
    }
    clearSoon(3400);
  }

  return {
    play(kind: FxKind, at: Pt) {
      clear();
      window.clearTimeout(timer);
      // a fresh data-fx restarts the stage tint even when the same kind plays twice in a row
      void root.offsetWidth;
      root.dataset.fx = kind;
      if (kind === 'fireworks') fireworks(at);
      else if (kind === 'snow') fall('fx--snow', 64, [2.8, 4.4], () => `--s:${rnd(0.5, 1.2).toFixed(2)}`);
      else if (kind === 'sakura') fall('fx--petal', 46, [3, 4.8], () => `--r:${rnd(0, 360).toFixed(0)}deg;--s:${rnd(0.7, 1.3).toFixed(2)}`);
      else if (kind === 'momiji') fall('fx--leaf', 44, [3, 5], (i) => `--r:${rnd(0, 360).toFixed(0)}deg;--c:${['#e0474c', '#f2b84b', '#d9773a'][i % 3]}`);
      else if (kind === 'streamers') fall('fx--ribbon', 34, [2.8, 4.4], (i) => `--c:${PALETTE[i % 5]};--r:${rnd(-25, 25).toFixed(0)}deg`);
      else if (kind === 'lanterns') lanterns(at);
      else drums(at);
    },
    stop() { window.clearTimeout(timer); clear(); },
  };
}
