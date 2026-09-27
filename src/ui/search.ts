import { regionOf, searchPrefectures } from '../data';
import type { Prefecture } from '../types';
import { clear, el } from './dom';

export function createSearch(root: HTMLElement, onPick: (slug: string) => void) {
  const input = root.querySelector<HTMLInputElement>('input')!;
  const list = root.querySelector<HTMLUListElement>('ul')!;
  let results: Prefecture[] = [];
  let active = -1;

  function render() {
    clear(list);
    if (!results.length) {
      list.hidden = true;
      input.setAttribute('aria-expanded', 'false');
      return;
    }
    results.forEach((p, i) => {
      const r = regionOf(p);
      const li = el(
        'li',
        { role: 'option', id: `sr-${p.slug}`, 'aria-selected': String(i === active), style: `--c:${r.color}` },
        el('span', { class: 'r-dot', 'aria-hidden': 'true' }),
        el('span', { class: 'r-ja', lang: 'ja' }, p.name.ja),
        el('span', { class: 'r-kana', lang: 'ja' }, p.name.kana),
        el('span', { class: 'r-ko' }, p.name.ko),
      );
      li.addEventListener('mousedown', (e) => e.preventDefault()); // keep focus in the input
      li.addEventListener('click', () => pick(p));
      list.append(li);
    });
    list.hidden = false;
    input.setAttribute('aria-expanded', 'true');
  }

  function pick(p: Prefecture) {
    input.value = '';
    results = [];
    active = -1;
    render();
    input.blur();
    onPick(p.slug);
  }

  input.addEventListener('input', () => {
    results = searchPrefectures(input.value);
    active = results.length ? 0 : -1;
    render();
  });
  input.addEventListener('focus', () => {
    if (input.value) {
      results = searchPrefectures(input.value);
      render();
    }
  });
  input.addEventListener('blur', () => {
    results = [];
    render();
  });
  input.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown' && results.length) {
      e.preventDefault();
      active = (active + 1) % results.length;
      render();
    } else if (e.key === 'ArrowUp' && results.length) {
      e.preventDefault();
      active = (active - 1 + results.length) % results.length;
      render();
    } else if (e.key === 'Enter') {
      const p = results[active] ?? results[0];
      if (p) pick(p);
    } else if (e.key === 'Escape') {
      input.value = '';
      results = [];
      render();
      input.blur();
    }
  });

  return { focus: () => input.focus() };
}
