// Renders mind-map boxes (NoteItem trees) as connected chips.
import type { NoteItem } from '../types';
import { el } from './dom';

export interface TreeStyle { color: string; ink: string }

export function renderTree(items: NoteItem[], style: TreeStyle, depth = 0): HTMLUListElement {
  const leafOnly = depth === 0 && items.length > 5 && items.every((it) => !it.children?.length);
  const cls = depth === 0 ? `tree tree--root${leafOnly ? ' tree--wrap' : ''}` : 'tree';
  const ul = el('ul', { class: cls, style: depth === 0 ? `--c:${style.color};--branch:${mix(style.ink)}` : undefined });
  for (const it of items) ul.append(renderNode(it, style, depth));
  return ul;
}

function mix(ink: string) {
  return `color-mix(in oklab, ${ink} 35%, white)`;
}

function renderNode(it: NoteItem, style: TreeStyle, depth: number): HTMLLIElement {
  const li = el('li', { class: 'node' });
  li.append(renderChip(it));
  const photo = photoLink(it);
  if (photo) li.append(photo);
  if (it.children?.length) li.append(renderTree(it.children, style, depth + 1));
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

export function hasJapanese(s: string): boolean {
  return /[぀-ヿ一-龯]/.test(s) && !/[가-힯]/.test(s);
}
