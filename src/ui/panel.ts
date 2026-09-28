// The diary-page panel: prefecture view, region view, and the general memo view.
import { airportsOf, countBoxes, extrasFor, extrasForRegion, generalExtras, groupOf, mascotSearchUrl, mascotsOf, mountains, notes, notesFor, places, prefById, prefBySlug, prefecturesIn, regionById, regionNotes, regionOf, regionTitle, stationsOf, supplementFor } from '../data';
import type { Mascot } from '../types';
import type { NoteExtra, NoteItem, Prefecture, Region } from '../types';
import { mascotVisualHtml } from '../mascots/visual';
import { clear, el, ruby } from './dom';
import { glossNote, photoSearch, renderTree } from './notes-render';

export interface PanelCallbacks {
  onClose(): void;
  onSelectPrefecture(slug: string): void;
  onSelectRegion(id: string): void;
  onRevealMascot(id: string): void;
  isMascotFound(id: string): boolean;
  /** mountain mode: current number and whether names are hidden for self-testing */
  rangeState?(): { active: number | null; hide: boolean };
  onRange?(no: number): void;
  onHideRangeNames?(hide: boolean): void;
  onMountainsOff?(): void;
  /** Tokyo: a 23-ward map whose wards pop up my boxes */
  hasWardMap?(slug: string): boolean;
  onWardMap?(focus?: string): void;
}

export type PanelView = { type: 'prefecture'; id: string } | { type: 'region'; id: string } | { type: 'mountains'; id: 'mountains' } | null;

export function createPanel(root: HTMLElement, cb: PanelCallbacks) {
  const body = root.querySelector<HTMLElement>('#panel-body')!;
  const closeBtn = root.querySelector<HTMLButtonElement>('#panel-close')!;
  root.insertBefore(el('div', { class: 'panel__grab', 'aria-hidden': 'true' }), body);
  let current: PanelView = null;

  closeBtn.addEventListener('click', () => {
    close();
    cb.onClose();
  });

  function open() {
    root.classList.add('is-open');
    root.setAttribute('aria-hidden', 'false');
    body.scrollTop = 0;
  }
  function close() {
    root.classList.remove('is-open');
    root.setAttribute('aria-hidden', 'true');
    current = null;
  }

  function showPrefecture(slug: string) {
    const p = prefBySlug.get(slug);
    if (!p) return;
    current = { type: 'prefecture', id: slug };
    clear(body);
    body.append(...renderPrefecture(p));
    open();
  }

  function showRegion(id: string) {
    const r = regionById.get(id);
    if (!r) return;
    current = { type: 'region', id };
    clear(body);
    body.append(...renderRegion(r));
    open();
  }

  function showMountains() {
    const again = current?.type === 'mountains';
    current = { type: 'mountains', id: 'mountains' };
    const top = body.scrollTop;
    clear(body);
    body.append(...renderMountains());
    if (again) body.scrollTop = top;
    else open();
  }

  /** Re-render the current view (e.g. after a mascot was found). */
  function refresh() {
    if (!current) return;
    const top = body.scrollTop;
    clear(body);
    if (current.type === 'prefecture') body.append(...renderPrefecture(prefBySlug.get(current.id)!));
    else if (current.type === 'region') body.append(...renderRegion(regionById.get(current.id)!));
    else body.append(...renderMountains());
    body.scrollTop = top;
  }

  // ---------------------------------------------------------------- mountain mode (worksheet 高い山脈・山地・高地)
  const revealed = new Set<number>();
  function renderMountains(): HTMLElement[] {
    const st = cb.rangeState?.() ?? { active: null, hide: false };
    if (!st.hide) revealed.clear();
    const isMasked = (no: number) => st.hide && !revealed.has(no);
    const reveal = (no: number) => {
      if (isMasked(no)) revealed.add(no);
      cb.onRange?.(no);
    };
    const out: HTMLElement[] = [];
    out.push(el('div', { class: 'ph' }, el('span', { class: 'chip--region chip--range' }, el('span', {}, '⛰'), el('small', {}, '산맥 모드'))));
    out.push(el('h2', { class: 'ph__name ph__name--range', lang: 'ja' }, el('span', { class: 'ph__furi' }, 'たかいさんみゃく・さんち・こうち'), '高い山脈・山地・高地'));
    out.push(el('p', { class: 'ph__alt' }, `산맥 · 산지 · 고지 ${mountains.ranges.length}개 — 번호를 누르면 지도에서 찾아요`));
    const hideBtn = el('button', { type: 'button', class: 'range-tool', 'aria-pressed': String(st.hide) }, st.hide ? '🙈 이름 가리는 중' : '👀 이름 가리기');
    hideBtn.addEventListener('click', () => cb.onHideRangeNames?.(!st.hide));
    const offBtn = el('button', { type: 'button', class: 'range-tool range-tool--off' }, '산맥 끄기');
    offBtn.addEventListener('click', () => cb.onMountainsOff?.());
    out.push(el('div', { class: 'range-tools' }, hideBtn, offBtn));

    // the chosen range, in full (its one-line fact lives here so the list stays even)
    const act = mountains.ranges.find((r) => r.no === st.active);
    if (!act) out.push(el('p', { class: 'range-focus range-focus--hint' }, '지도의 번호나 아래 이름을 누르면 여기에 자세히 나와요'));
    else if (isMasked(act.no)) {
      const b = el('button', { type: 'button', class: 'range-focus range-focus--masked' },
        el('span', { class: 'range-focus__no' }, String(act.no)),
        el('span', { class: 'range-focus__body' }, el('b', { class: 'range-focus__name' }, '이름이 뭘까요?'), el('span', { class: 'range-focus__fact' }, '떠올려 보고 눌러서 확인 👀')));
      b.addEventListener('click', () => reveal(act.no));
      out.push(b);
    } else {
      out.push(el('div', { class: 'range-focus', 'aria-live': 'polite' },
        el('span', { class: 'range-focus__no' }, String(act.no)),
        el('span', { class: 'range-focus__body' },
          el('span', { class: 'range-focus__kana', lang: 'ja' }, act.name.kana),
          el('span', { class: 'range-focus__line' }, el('b', { class: 'range-focus__name', lang: 'ja' }, act.name.ja), el('span', { class: 'range-focus__ko' }, act.name.ko)),
          act.ko ? el('span', { class: 'range-focus__fact' }, act.ko) : null)));
    }

    const list = el('ol', { class: 'range-list' });
    for (const r of mountains.ranges) {
      const b = el('button', { type: 'button', class: `range-item${r.no === st.active ? ' is-active' : ''}${isMasked(r.no) ? ' is-masked' : ''}`, 'aria-pressed': String(r.no === st.active), title: r.ko ?? '' },
        el('span', { class: 'range-item__no' }, String(r.no)),
        el('span', { class: 'range-item__text' },
          el('span', { class: 'range-item__kana', lang: 'ja' }, r.name.kana),
          el('span', { class: 'range-item__name', lang: 'ja' }, r.name.ja),
          el('span', { class: 'range-item__ko' }, r.name.ko)));
      b.addEventListener('click', () => reveal(r.no));
      list.append(el('li', {}, b));
    }
    out.push(el('section', { class: 'sec sec--ranges' }, list));

    if (mountains.notes.length) {
      const memo = el('div', { class: 'range-notes' });
      for (const n of mountains.notes) memo.append(el('div', { class: 'range-notes__item' }, el('b', { lang: 'ja' }, n.t), n.sub ? el('span', { lang: 'ja' }, ` ${n.sub}`) : null, n.ko ? el('p', {}, n.ko) : null));
      out.push(el('section', { class: 'sec' }, el('h3', {}, el('span', { class: 'emoji' }, '✎'), '내 메모', el('span', { class: 'n' }, '학습지에 적어 둔 것')), memo));
    }
    out.push(el('p', { class: 'meta-line' }, '선은 능선을 따라 대략 그린 것이에요. 번호는 학습지 「高い山脈・山地・高地」 그대로.'));
    return out;
  }

  // ---------------------------------------------------------------- prefecture
  function renderPrefecture(p: Prefecture): HTMLElement[] {
    const r = regionOf(p);
    const my = notesFor(p);
    const nBoxes = countBoxes(my.items);
    const out: HTMLElement[] = [];

    const regionBtn = el('button', { class: 'chip--region', type: 'button', style: `--c:${r.color}` }, el('span', { lang: 'ja' }, regionTitle(r)), el('small', {}, r.name.ko));
    regionBtn.addEventListener('click', () => cb.onSelectRegion(r.id));
    out.push(el('div', { class: 'ph' }, regionBtn, my.star ? el('span', { class: 'star', title: '마인드맵에 ★ 표시' }, '★') : null, el('span', { class: 'ph__id' }, `No.${String(p.id).padStart(2, '0')}`)));

    out.push(el('h2', { class: 'ph__name', lang: 'ja' }, p.name.ja, el('span', { class: 'ph__kana' }, p.name.kana)));
    out.push(el('p', { class: 'ph__alt' }, `${p.name.ko} · `, el('span', { class: 'romaji' }, p.name.romaji)));
    // how I wrote this prefecture on my mind map, when it is not the standard spelling
    const mine = [notes.prefectures[p.slug]?.root?.ja, notes.prefectures[p.slug]?.root?.ko].filter(Boolean).join(' · ');
    if (mine) out.push(el('p', { class: 'ph__mine', title: '마인드맵 박스에 적은 그대로' }, el('span', { class: 'k' }, '✎ 내 표기'), mine));
    out.push(
      el('p', { class: 'ph__cap' }, el('span', { class: 'k' }, '県庁所在地'), el('span', { lang: 'ja' }, p.capital.ja), el('span', { class: 'kana', lang: 'ja' }, p.capital.kana ?? ''), el('span', { class: 'kana' }, p.capital.ko ?? '')),
    );
    // 🚄 가는 법 (v2): the prefecture's airports and named shinkansen stations, straight from transit.json
    const air = airportsOf(p), sta = stationsOf(p);
    if (air.length || sta.length) {
      const go = el('p', { class: 'ph__cap ph__go' }, el('span', { class: 'k' }, '가는 법'));
      for (const a of air) go.append(el('span', { class: 'go', title: a.name.ko }, '✈ ', el('span', { lang: 'ja' }, a.name.ja), el('span', { class: 'kana', lang: 'ja' }, a.name.kana)));
      for (const s of sta) go.append(el('span', { class: 'go', title: s.lines.join(' · ') }, '🚄 ', el('span', { lang: 'ja' }, `${s.station.ja}駅`), el('span', { class: 'kana', lang: 'ja' }, s.station.kana ?? '')));
      out.push(go);
    }

    // my mind map
    const notesSec = el('section', { class: 'sec sec--notes' }, el('h3', {}, el('span', { class: 'emoji' }, '✎'), '내 마인드맵', el('span', { class: 'n' }, nBoxes ? `${nBoxes} boxes` : '')));
    const wardMap = !!cb.hasWardMap?.(p.slug);
    if (wardMap) {
      const b = el('button', { type: 'button', class: 'ward-map-btn' }, el('span', { 'aria-hidden': 'true' }, '🗺'), '23区 지도로 보기', el('small', {}, '구를 누르면 칸이 떠요'));
      b.addEventListener('click', () => cb.onWardMap?.());
      notesSec.append(b);
    }
    if (my.items.length) {
      const note = glossNote(my.items, ...extrasFor(p).map((e) => e.items));
      if (note) notesSec.append(note);
      // Tokyo: the ward branches live in the 23区 popup, so here each ward shows 「+N칸」 (tap → popup on that ward)
      const wards = new Set(places.wards.map((w) => w.name.ja));
      const opts = wardMap ? { fold: 1, onFold: (it: NoteItem) => (wards.has(it.t) ? (cb.onWardMap?.(it.t), true) : false) } : {};
      notesSec.append(renderTree(my.items, { color: r.color, ink: r.ink }, 0, opts));
    }
    else notesSec.append(el('p', { class: 'empty' }, `아직 ${p.short.ja} 메모가 없어요. Canva 마인드맵에 적고 data/notes.json 에 옮기면 여기 나타나요 ✿`));
    out.push(notesSec);

    // Claude's supplement for prefectures I have not written about yet — kept apart from my own voice
    const sup = supplementFor(p);
    if (sup.length) {
      out.push(el('section', { class: 'sec sec--supplement' },
        el('h3', {}, el('span', { class: 'emoji' }, '✦'), '보충', el('span', { class: 'n' }, 'Claude 가 채운 메모 · 내 마인드맵 아님')),
        renderTree(sup, { color: r.color, ink: r.ink })));
    }

    // extras that mention this prefecture
    const extras = extrasFor(p);
    if (extras.length) {
      const sec = el('section', { class: 'sec sec--extras' }, el('h3', {}, el('span', { class: 'emoji' }, '🧷'), '함께 보기'));
      for (const ex of extras) sec.append(renderExtra(ex, r, false));
      out.push(sec);
    }

    // friends (real local mascots of this prefecture)
    const friends = mascotsOf(p).filter((m) => !m.secret || cb.isMascotFound(m.id));
    if (friends.length) {
      const sec = el('section', { class: 'sec sec--friends' }, el('h3', {}, el('span', { class: 'emoji' }, '✦'), '이 県의 친구들', el('span', { class: 'n' }, `${friends.filter((m) => cb.isMascotFound(m.id)).length}/${friends.length} · 눌러서 만나기`)));
      const row = el('div', { class: 'friends' });
      for (const m of friends) row.append(friendCard(m, p.short.ja));
      sec.append(row);
      const met = friends.filter((m) => cb.isMascotFound(m.id));
      for (const m of met) sec.append(mascotCard(m));
      out.push(sec);
    }

    // facts (図鑑)
    const facts = el('div', { class: 'facts' });
    const dl = el('dl', {});
    dl.append(
      el('dt', {}, '名物', el('small', {}, '명물')),
      el('dd', {}, el('div', { class: 'terms' }, ...p.meibutsu.map((t) => termChip(t, p.short.ja)))),
      el('dt', {}, '観光', el('small', {}, '관광')),
      el('dd', {}, el('div', { class: 'terms' }, ...p.spots.map((t) => termChip(t, p.short.ja)))),
      el('dt', {}, 'ひとこと', el('small', {}, '한마디')),
      el('dd', {}, el('div', { class: 'hitokoto' }, el('span', { class: 'ja', lang: 'ja' }, p.hitokoto.ja), el('span', { class: 'ko' }, p.hitokoto.ko))),
    );
    facts.append(dl);
    const details = el('details', my.items.length ? {} : { open: '' }, el('summary', {}, el('h3', {}, el('span', { class: 'emoji' }, '📘'), '図鑑', el('span', { class: 'n' }, '기본 정보'))), facts);
    out.push(el('section', { class: 'sec sec--facts' }, details));

    // prev / next
    const prev = prefById.get(p.id === 1 ? 47 : p.id - 1)!;
    const next = prefById.get(p.id === 47 ? 1 : p.id + 1)!;
    const prevBtn = el('button', { type: 'button', class: 'prev' }, el('small', {}, '← 前'), el('span', { lang: 'ja' }, prev.name.ja));
    const nextBtn = el('button', { type: 'button', class: 'next' }, el('small', {}, '次 →'), el('span', { lang: 'ja' }, next.name.ja));
    prevBtn.addEventListener('click', () => cb.onSelectPrefecture(prev.slug));
    nextBtn.addEventListener('click', () => cb.onSelectPrefecture(next.slug));
    out.push(el('nav', { class: 'ph__nav', 'aria-label': '이전/다음 현' }, prevBtn, nextBtn));
    return out;
  }

  function friendCard(m: Mascot, prefShort: string): HTMLElement {
    const has = cb.isMascotFound(m.id);
    const art = el('div', { class: 'friends__art', 'aria-hidden': 'true' });
    art.innerHTML = mascotVisualHtml(m);
    const b = el(
      'button',
      { type: 'button', class: `friends__card${has ? ' is-found' : ''}${m.kind === 'extra' ? ' is-extra' : ''}${m.secret ? ' is-secret' : ''}`, title: has ? m.name.ja : `${prefShort}에 누가 살까?` },
      art,
      el('span', { class: 'friends__name', lang: 'ja' }, has ? m.name.ja : '？？？'),
      el('small', {}, has ? (m.secret ? '숨은 친구' : m.kind === 'extra' ? '비공식' : '공식') : prefShort),
    );
    b.addEventListener('click', () => cb.onRevealMascot(m.id));
    return b;
  }

  function mascotCard(m: Mascot): HTMLElement {
    const art = el('div', { class: 'mascot-card__art', 'aria-hidden': 'true' });
    art.innerHTML = mascotVisualHtml(m);
    const link = el('a', { class: 'mascot-card__link', href: m.url ?? mascotSearchUrl(m), target: '_blank', rel: 'noopener noreferrer' }, m.url ? '공식 페이지 ↗' : '검색해서 보기 ↗');
    return el(
      'div',
      { class: 'mascot-card' },
      art,
      el(
        'div',
        { class: 'mascot-card__body' },
        el('b', { lang: 'ja' }, m.name.ja, el('span', { class: 'mascot-card__kana' }, ` ${m.name.kana}`)),
        el('small', {}, `${m.name.ko} · ${m.org}${m.secret ? ' · 숨은 친구' : m.kind === 'extra' ? ' · 비공식' : ''}`),
        el('small', { class: 'mascot-card__about', lang: 'ja' }, m.about.ja),
        el('small', { class: 'mascot-card__about' }, m.about.ko),
        el(
          'small',
          { class: 'mascot-card__meta' },
          m.art === 'likeness' ? '그림은 이 프로젝트가 그린 닮은꼴 (공식 아님) · ' : m.art === 'standin' ? `그림: ${m.credit ?? ''} (공식 그림 아님) · ` : `${m.credit ?? ''} · `,
          link,
        ),
      ),
    );
  }

  /** A 名物 / 観光 word: reading above, Korean below, and 📷 to look it up (searched with the prefecture's name). */
  function termChip(t: { ja: string; kana?: string; ko?: string }, where: string): HTMLElement {
    return el('span', { class: 'term' },
      el('span', { class: 'term__text' }, el('span', { class: 'term__ja', lang: 'ja' }, ruby(t.ja, t.kana)), t.ko ? el('span', { class: 'term__ko' }, t.ko) : null),
      photoSearch(`${t.ja} ${where}`));
  }

  function renderExtra(ex: NoteExtra, r: Region, open: boolean): HTMLElement {
    const d = el('details', { class: 'extra', ...(open ? { open: '' } : {}) }, el('summary', {}, el('span', { lang: 'ja' }, ex.title), ex.sub ? el('small', {}, ex.sub) : null));
    d.append(renderTree(ex.items, { color: r.color, ink: r.ink }));
    return d;
  }

  // ---------------------------------------------------------------- region
  function renderRegion(r: Region): HTMLElement[] {
    const out: HTMLElement[] = [];
    // a region inside a big one (中部 › 北陸) says so in the chip; its page then also carries my 中部 memo
    const g = groupOf(r);
    out.push(el('div', { class: 'ph' }, el('span', { class: 'chip--region', style: `--c:${r.color}` }, el('span', { lang: 'ja' }, g ? `${g.name.ja}地方 ›` : '地方'), el('small', {}, g ? g.name.ko : '지방'))));
    out.push(el('h2', { class: 'ph__name', lang: 'ja' }, r.name.ja, el('span', { class: 'ph__kana' }, r.name.kana)));
    out.push(el('p', { class: 'ph__alt' }, `${r.name.ko} · `, el('span', { class: 'romaji' }, r.name.en)));
    for (const rn of regionNotes(r)) {
      if (rn.memo) out.push(el('p', { class: 'ph__cap' }, el('span', { class: 'k' }, 'memo'), el('span', { lang: 'ja' }, rn.memo)));
      if (rn.items.length) {
        out.push(el('section', { class: 'sec' }, el('h3', {}, el('span', { class: 'emoji' }, '✎'), rn.id === r.id ? '지방 메모' : el('span', { lang: 'ja' }, `${rn.title} 메모`), rn.id === r.id ? null : el('span', { class: 'n' }, '내 마인드맵의 큰 지방 상자')), glossNote(rn.items), renderTree(rn.items, { color: r.color, ink: r.ink })));
      }
    }
    const extras = extrasForRegion(r.id);
    if (extras.length) {
      const sec = el('section', { class: 'sec sec--extras' }, el('h3', {}, el('span', { class: 'emoji' }, '🧷'), '함께 보기'));
      for (const ex of extras) sec.append(renderExtra(ex, r, true));
      out.push(sec);
    }

    const members = prefecturesIn(r.id);
    const chips = el('div', { class: 'member-chips' });
    for (const p of members) {
      const n = countBoxes(notesFor(p).items);
      const b = el('button', { type: 'button', style: `--c:${r.color}` }, el('span', { lang: 'ja' }, p.short.ja), n ? el('span', { class: 'dot', title: `메모 ${n}개` }) : null, el('small', {}, p.name.ko));
      b.addEventListener('click', () => cb.onSelectPrefecture(p.slug));
      chips.append(b);
    }
    out.push(el('section', { class: 'sec' }, el('h3', {}, el('span', { class: 'emoji' }, '🗾'), `${members.length}개 도도부현`, el('span', { class: 'n' }, '● = 메모 있음')), chips));

    const friends = members.flatMap((p) => mascotsOf(p).filter((m) => !m.secret || cb.isMascotFound(m.id)).map((m) => ({ m, p })));
    if (friends.length) {
      const row = el('div', { class: 'friends' });
      for (const { m, p } of friends) {
        const card = friendCard(m, p.short.ja);
        card.addEventListener('click', () => cb.onSelectPrefecture(p.slug), { capture: true });
        row.append(card);
      }
      const n = friends.filter(({ m }) => cb.isMascotFound(m.id)).length;
      out.push(el('section', { class: 'sec' }, el('h3', {}, el('span', { class: 'emoji' }, '✦'), '이 지방의 친구들', el('span', { class: 'n' }, `${n}/${friends.length}`)), row));
    }
    return out;
  }

  return { showPrefecture, showRegion, showMountains, refresh, close, isOpen: () => root.classList.contains('is-open'), current: () => current };
}

/** Content for the 메모장 modal: notes that belong to no particular place. */
export function renderGeneralMemo(): HTMLElement {
  const wrap = el('div', { class: 'memo-list' });
  wrap.append(el('h2', {}, '메모장', el('small', {}, '어디에도 안 붙는 메모들')));
  wrap.append(el('p', { class: 'lead' }, `출처: ${notes.meta.source} · ${notes.meta.updated}`));
  for (const ex of generalExtras()) {
    const d = el('details', { class: 'extra', open: '' }, el('summary', {}, el('span', { lang: 'ja' }, ex.title), ex.sub ? el('small', {}, ex.sub) : null));
    d.append(renderTree(ex.items, { color: '#F5EFE3', ink: '#a8998f' }));
    wrap.append(d);
  }
  return wrap;
}
