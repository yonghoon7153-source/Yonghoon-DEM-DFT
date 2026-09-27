// 北(きた) · 南(みなみ) · 西(にし) 左(ひだり) · 東(ひがし) 右(みぎ) around the map, where my Canva map has them.
// The map is always north-up, so the words sit on the edges of the stage and never move with zoom.
import { places } from '../data';
import type { CompassWord, LabelMode } from '../types';
import { clear, el } from './dom';

function word(w: CompassWord, mode: LabelMode): HTMLElement {
  const main = mode === 'kana' ? w.kana : mode === 'ko' ? w.ko : w.ja;
  return el(
    'span',
    { class: 'compass__word', lang: mode === 'ko' ? 'ko' : 'ja' },
    mode === 'furi' ? el('span', { class: 'compass__furi' }, w.kana) : null,
    el('span', { class: 'compass__main' }, main),
  );
}

export function createCompass(stage: HTMLElement, before: Element | null) {
  const root = el('div', { class: 'compass', 'aria-hidden': 'true' });
  stage.insertBefore(root, before);
  return {
    setMode(mode: LabelMode) {
      clear(root);
      for (const d of places.compass ?? []) {
        root.append(
          el(
            'div',
            { class: `compass__dir compass__dir--${d.side}`, title: d.words.map((w) => `${w.ja} (${w.kana}) ${w.ko}`).join(' · ') },
            ...d.words.map((w) => word(w, mode)),
          ),
        );
      }
    },
  };
}
