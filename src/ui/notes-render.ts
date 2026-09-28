// Renders mind-map boxes (NoteItem trees) as connected chips.
import { countBoxes } from '../data';
import type { NoteItem } from '../types';
import { el, ruby } from './dom';

export interface TreeStyle { color: string; ink: string }
/** `fold`: boxes at this depth show 「+N칸」 instead of their branches; `onFold` may take the tap (true) instead of opening in place. */
export interface TreeOptions { fold?: number; onFold?(it: NoteItem): boolean }

export function renderTree(items: NoteItem[], style: TreeStyle, depth = 0, opts: TreeOptions = {}): HTMLUListElement {
  const leafOnly = depth === 0 && items.length > 5 && items.every((it) => !it.children?.length);
  const cls = depth === 0 ? `tree tree--root${leafOnly ? ' tree--wrap' : ''}` : 'tree';
  const ul = el('ul', { class: cls, style: depth === 0 ? `--c:${style.color};--branch:${mix(style.ink)}` : undefined });
  for (const it of items) ul.append(renderNode(it, style, depth, opts));
  return ul;
}

function mix(ink: string) {
  return `color-mix(in oklab, ${ink} 35%, white)`;
}

function renderNode(it: NoteItem, style: TreeStyle, depth: number, opts: TreeOptions): HTMLLIElement {
  const li = el('li', { class: 'node' });
  li.append(renderChip(it));
  const photo = photoLink(it);
  if (photo) li.append(photo);
  const kids = it.children ?? [];
  if (kids.length && opts.fold !== undefined && depth >= opts.fold) {
    const more = el('button', { type: 'button', class: 'nfold', title: '펼치기' }, `+${countBoxes(kids)}칸 ▸`);
    more.addEventListener('click', () => {
      if (opts.onFold?.(it)) return;
      more.replaceWith(renderTree(kids, style, depth + 1));
    });
    li.append(more);
  } else if (kids.length) li.append(renderTree(kids, style, depth + 1, opts));
  return li;
}

export function renderChip(it: NoteItem): HTMLElement {
  const isLink = !!it.url;
  const chip = isLink
    ? el('a', { class: 'nchip nchip--link', href: it.url, target: '_blank', rel: 'noopener noreferrer' })
    : el('div', { class: it.kind === 'photo' ? 'nchip nchip--photo' : 'nchip' });
  if (it.cap) chip.append(el('span', { class: 'nchip__cap' }, it.cap));
  const t = el('span', { class: 'nchip__t' }, it.kind === 'photo' ? `📷 ${it.t} (사진 자리)` : it.t);
  if (hasJapanese(it.t)) t.lang = 'ja';
  chip.append(t);
  if (it.star) chip.append(el('span', { class: 'nchip__star', title: '★' }, '★'));
  if (it.ko) chip.append(el('span', { class: 'nchip__ko' }, it.ko));
  if (isLink) chip.append(el('span', { class: 'nchip__ext', 'aria-hidden': 'true' }, '↗'));
  if (it.sub) chip.append(el('span', { class: 'nchip__sub', lang: hasJapanese(it.sub) ? 'ja' : undefined }, it.sub));
  if (it.gloss) chip.append(el('span', { class: 'nchip__gloss', lang: 'ko', title: '한국어 풀이 — Claude 가 붙임 (마인드맵 원문 아님)' }, it.gloss));
  return chip;
}

/** One line saying the gray Korean lines are Claude's, when any of these trees has one. */
export function glossNote(...lists: NoteItem[][]): HTMLElement | null {
  const has = (items: NoteItem[]): boolean => items.some((it) => !!it.gloss || has(it.children ?? []));
  return lists.some(has) ? el('p', { class: 'gloss-note' }, '회색 한국어 줄 = Claude 가 붙인 풀이 (원문 아님)') : null;
}

/** 📷 next to a box that had a photo in the Canva: the photo itself is not ours to copy, so it opens an image search. */
function photoLink(it: NoteItem): HTMLElement | null {
  if (!it.photo) return null;
  return photoSearch(typeof it.photo === 'string' ? it.photo : it.t);
}

/** 📷 — opens an image search; the photos themselves stay out of the site (CLAUDE.md rule 6). */
export function photoSearch(q: string): HTMLElement {
  return el('a', {
    class: 'nphoto', href: `https://www.google.com/search?tbm=isch&q=${encodeURIComponent(q)}`,
    target: '_blank', rel: 'noopener noreferrer', title: `사진 보기 — ${q}`, 'aria-label': `사진 보기: ${q}`,
  }, '📷');
}

/**
 * A 名物 / 観光 word of the 기본 정보: reading above, Korean below, and 📷 to look it up (searched with `where`, the
 * prefecture's name). `data-t` is the word, for a landmark sticker to find it and make it blink.
 */
export function termChip(t: { ja: string; kana?: string; ko?: string }, where: string): HTMLElement {
  return el('span', { class: 'term', 'data-t': t.ja },
    el('span', { class: 'term__text' }, el('span', { class: 'term__ja', lang: 'ja' }, ruby(t.ja, t.kana)), t.ko ? el('span', { class: 'term__ko' }, t.ko) : null),
    photoSearch(`${t.ja} ${where}`));
}

export function hasJapanese(s: string): boolean {
  return /[぀-ヿ一-龯]/.test(s) && !/[가-힯]/.test(s);
}
