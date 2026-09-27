import type { Prefecture } from '../types';
import { regionOf, notesFor, countBoxes } from '../data';
import { clear, el } from './dom';

export function createTooltip(node: HTMLElement, stage: HTMLElement) {
  let raf = 0;
  return {
    show(p: Prefecture, ev: MouseEvent) {
      clear(node);
      const r = regionOf(p);
      node.style.setProperty('--c', r.color);
      const n = countBoxes(notesFor(p).items);
      node.append(
        el('span', { class: 't-ja', lang: 'ja' }, p.name.ja),
        el('span', { class: 't-kana', lang: 'ja' }, p.name.kana),
        el('span', { class: 't-ko' }, `${p.name.ko} · ${p.name.en}`),
        n ? el('span', { class: 't-hint' }, `✎ 메모 ${n}개`) : el('span', { class: 't-hint' }, p.mascot ? '눌러서 누가 사는지 보기' : '눌러서 자세히'),
      );
      node.hidden = false;
      this.move(ev);
    },
    move(ev: MouseEvent) {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const rect = stage.getBoundingClientRect();
        let x = ev.clientX - rect.left;
        let y = ev.clientY - rect.top;
        const w = node.offsetWidth + 20;
        const h = node.offsetHeight + 24;
        if (x + w > rect.width) x -= w + 8;
        if (y + h > rect.height) y -= h;
        node.style.transform = `translate(${x + 14}px, ${y + 18}px)`;
      });
    },
    hide() {
      node.hidden = true;
    },
  };
}
