import initialDeck from '../../data/word-cards.json';
import { el } from './dom';
import { matchesCard, parseDeck, shuffled, type StudyLanguage, type WordCard, type WordDeck } from './word-deck';

const DECK_KEY = 'nihonchizu.private-deck.v1';
const KNOWN_KEY = 'nihonchizu.known-cards.v1';

export function createWordCards() {
  const original = parseDeck(initialDeck);
  let deck = original, language: StudyLanguage = 'ja', mode: 'cards' | 'list' = 'cards';
  let index = 0, flipped = false, onlyUnknown = false, order: WordCard[] = [];
  let known = new Set<string>(), storageWarning = '', canPersistKnown = true;
  let savedDeck: WordDeck | undefined;
  try {
    const saved = localStorage.getItem(DECK_KEY);
    if (saved) { savedDeck = parseDeck(JSON.parse(saved)); deck = savedDeck; }
  } catch { storageWarning = '저장된 단어장을 읽지 못해 기본 단어장을 열었어요. 필요하면 파일을 다시 불러와 주세요.'; }
  try {
    const marks: unknown = JSON.parse(localStorage.getItem(KNOWN_KEY) || '[]');
    if (!Array.isArray(marks) || !marks.every((s) => typeof s === 'string')) throw new Error('Invalid marks');
    known = new Set(marks);
  } catch { canPersistKnown = false; storageWarning += ' 이전 학습 표시를 읽지 못했어요. 기존 저장값은 보존하고 새 표시는 이번 화면에서만 유지해요.'; }

  const root = el('section', { class: 'study', 'aria-label': '단어 카드로 복습하기' });
  const name = el('h2', { class: 'study__title' });
  const subtitle = el('p', { class: 'study__subtitle' });
  const message = el('p', { class: 'study__message', role: 'status' }, storageWarning);
  const status = el('p', { class: 'sr-only', role: 'status', 'aria-live': 'polite', 'aria-atomic': 'true' });
  const button = (label: string, cls = 'study__button') => el('button', { type: 'button', class: cls }, label);
  const ja = button('日本語', 'study__tab'), en = button('English', 'study__tab');
  const cardMode = button('카드', 'study__tab'), listMode = button('목록', 'study__tab');
  const tabs = el('div', { class: 'study__tabs', role: 'group', 'aria-label': '학습 언어' }, ja, en);
  const modes = el('div', { class: 'study__tabs', role: 'group', 'aria-label': '보기 방식' }, cardMode, listMode);
  const query = el('input', { class: 'study__search', type: 'search', placeholder: '단어·뜻 검색', 'aria-label': '단어 또는 뜻 검색', autocomplete: 'off' });
  const category = el('select', { class: 'study__select', 'aria-label': '상황별로 고르기' });
  const unknown = button('낯선 단어만', 'study__filter');
  const mix = button('섞기', 'study__button study__shuffle');
  const count = el('span', { class: 'study__count' });
  const learned = el('span', { class: 'study__learned' });
  const progress = el('progress', { class: 'study__progress', 'aria-label': '현재 카드 위치', max: '1', value: '0' });
  const scene = el('div', { class: 'study__scene' });
  const card = el('button', { type: 'button', class: 'study__card', 'aria-label': '카드 뒤집기', 'aria-describedby': 'study-shortcuts' });
  const previous = button('이전', 'study__button study__step');
  const next = button('다음', 'study__button study__step');
  const flip = button('뜻 보기', 'study__button study__flip');
  const again = button('다시 볼래요', 'study__rating study__rating--again');
  const gotIt = button('이제 알겠어요', 'study__rating study__rating--known');
  const ratings = el('div', { class: 'study__ratings' }, again, gotIt);
  const navigation = el('div', { class: 'study__navigation' }, previous, flip, next);
  const source = el('a', { class: 'study__source', target: '_blank', rel: 'noopener noreferrer' }, '이 단어 Notion에서 열기');
  const detail = el('div', { class: 'study__detail' });
  const list = el('div', { class: 'study__list', 'aria-label': '단어 목록' });
  const more = button('더 보기', 'study__button study__more');
  let listLimit = 40;
  const file = el('input', { type: 'file', accept: '.json,application/json', class: 'sr-only', tabindex: '-1', 'aria-label': '내 단어장 파일' });
  const load = button('내 단어장 불러오기', 'study__text-button');
  const basic = button('기본 단어장 보기', 'study__text-button');
  const forget = button('이 기기의 단어장 지우기', 'study__text-button');
  const importPanel = el('details', { class: 'study__import' },
    el('summary', {}, '내 단어장으로 공부하기'),
    el('p', {}, '채팅에서 받은 카드용 JSON 파일을 골라 주세요. 파일은 서버에 보내지 않고 이 브라우저에 보관해요.'),
    el('div', { class: 'study__import-actions' }, load, basic, forget, file),
  );
  root.append(
    el('div', { class: 'study__top' }, el('div', {}, el('p', { class: 'study__kicker' }, '한 장씩, 내 속도로'), name, subtitle), modes),
    el('div', { class: 'study__toolbar' }, tabs, mix),
    el('div', { class: 'study__filters' }, query, category, unknown),
    el('div', { class: 'study__meta' }, count, learned), progress,
    scene, navigation, ratings, detail, source, list, more,
    el('p', { id: 'study-shortcuts', class: 'study__shortcuts' }, '카드를 눌러 뒤집기 · 카드에서 ← → 이동 · Space로 뜻 보기'),
    el('p', { class: 'study__save-note' }, '학습 표시는 이 브라우저에 저장돼요. Notion 암기 기록은 바뀌지 않아요.'),
    importPanel, message, status,
  );

  const key = (c: WordCard) => `${deck.deckId}:${language}:${c.id}`;
  function persistKnown() {
    if (!canPersistKnown) { message.textContent = '기존 학습 표시를 읽지 못해 덮어쓰지 않았어요. 새 표시는 이번 화면에서만 유지돼요.'; return; }
    try { localStorage.setItem(KNOWN_KEY, JSON.stringify([...known])); }
    catch { message.textContent = '학습 표시는 이번 화면에서만 유지돼요. 브라우저 저장 공간을 확인해 주세요.'; }
  }
  function categories() {
    category.replaceChildren(el('option', { value: '' }, '모든 상황'),
      ...[...new Set(deck.cards.map((c) => c.category))].sort().map((c) => el('option', { value: c }, c)));
  }
  let sequence = [...deck.cards];
  function select(preserve = false) {
    const currentId = preserve ? order[index]?.id : undefined;
    const previousIndex = index;
    order = sequence.filter((c) => c[language] && matchesCard(c, query.value)
      && (!category.value || c.category === category.value) && (!onlyUnknown || !known.has(key(c))));
    const found = currentId ? order.findIndex((c) => c.id === currentId) : -1;
    index = preserve ? (found >= 0 ? found : Math.min(previousIndex, Math.max(0, order.length - 1))) : 0;
    flipped = false; listLimit = 40; render();
  }
  function render() {
    const c = order[index];
    name.textContent = deck.title;
    subtitle.textContent = deck === original ? '생활에서 꺼내 쓰는 일본어와 영어' : `내 단어장 · ${deck.cards.length.toLocaleString()}개 표현`;
    [ja, en].forEach((b, i) => b.setAttribute('aria-pressed', String(language === (i ? 'en' : 'ja'))));
    [cardMode, listMode].forEach((b, i) => b.setAttribute('aria-pressed', String(mode === (i ? 'list' : 'cards'))));
    unknown.setAttribute('aria-pressed', String(onlyUnknown));
    const available = deck.cards.filter((v) => v[language]);
    learned.textContent = `익힌 표현 ${available.filter((v) => known.has(key(v))).length} / ${available.length}`;
    count.textContent = mode === 'list' ? `${order.length.toLocaleString()}개 표현` : `${c ? index + 1 : 0} / ${order.length}`;
    progress.max = Math.max(order.length, 1); progress.value = c ? index + 1 : 0;
    progress.hidden = mode !== 'cards';
    previous.disabled = !c || index === 0; next.disabled = !c || index === order.length - 1;
    flip.disabled = !c; mix.disabled = order.length < 2;
    ratings.hidden = !c || mode !== 'cards'; navigation.hidden = mode !== 'cards';
    list.hidden = mode !== 'list'; scene.hidden = mode !== 'cards';
    detail.hidden = !c || !flipped || mode !== 'cards'; source.hidden = !c?.notionUrl || mode !== 'cards';
    basic.hidden = !savedDeck && deck === original;
    basic.textContent = deck === original ? '보관한 내 단어장 보기' : '기본 단어장 보기';
    if (c?.notionUrl) source.href = c.notionUrl; else source.removeAttribute('href');
    const empty = () => el('div', { class: 'study__empty' }, el('span', { 'aria-hidden': 'true' }, onlyUnknown ? '🌱' : '🔎'),
      el('h3', {}, onlyUnknown ? '남은 낯선 단어가 없어요' : '찾는 표현이 아직 없어요'),
      el('p', {}, '검색어나 상황을 바꾸거나 전체 단어를 다시 살펴보세요.'), resetFilters());
    if (mode === 'cards') {
      list.replaceChildren();
      if (!c) { scene.replaceChildren(empty()); detail.replaceChildren(); }
      else {
        if (!scene.contains(card)) scene.replaceChildren(card);
        card.dataset.face = flipped ? 'back' : 'front';
        card.setAttribute('aria-label', flipped ? `${c.ko}. ${c[language]}. 눌러서 표현으로 돌아가기` : `${c[language]}${language === 'ja' && c.reading !== c.ja ? `. 읽기: ${c.reading}` : ''}. 눌러서 뜻 보기`);
        card.replaceChildren(
          el('span', { class: 'study__tape', 'aria-hidden': 'true' }),
          el('span', { class: 'study__card-top' }, el('span', {}, c.category), el('span', {}, known.has(key(c)) ? '✓ 익힌 표현' : flipped ? '뜻 · 의미' : language === 'ja' ? '日本語' : 'English')),
          el('span', { class: 'study__expression', lang: flipped ? 'ko' : language }, flipped ? c.ko : c[language]),
          el('span', { class: 'study__reading', lang: flipped ? language : 'ja' }, flipped ? c[language] : language === 'ja' ? c.reading : ''),
          el('span', { class: 'study__card-hint' }, flipped ? '다시 누르면 표현이 보여요' : '떠올렸다면, 눌러서 뜻 확인'),
        );
        flip.textContent = flipped ? '표현 보기' : '뜻 보기';
        gotIt.textContent = known.has(key(c)) ? '✓ 익힌 표현' : '이제 알겠어요';
        const other = language === 'ja' ? c.en : c.ja;
        detail.replaceChildren(
          ...(other ? [el('p', { class: 'study__counterpart' }, el('span', {}, language === 'ja' ? 'English' : '日本語'), el('strong', { lang: language === 'ja' ? 'en' : 'ja' }, other))] : []),
          ...(c[language === 'ja' ? 'jaExample' : 'enExample'] ? [el('div', { class: 'study__example' },
            el('span', { class: 'study__example-label' }, c.exampleOrigin === 'authored' ? '이렇게 말해요 · 작성 예문' : '이렇게 말해요'),
            el('p', { lang: language }, c[language === 'ja' ? 'jaExample' : 'enExample']), el('p', { lang: 'ko' }, c.koExample))] : []),
        );
      }
    } else {
      const rows = order.slice(0, listLimit).map((v) => {
        const b = button('', 'study__row');
        b.append(el('span', { class: 'study__row-expression', lang: language }, v[language]), el('span', {}, v.ko),
          el('span', { class: 'study__row-mark' }, known.has(key(v)) ? '✓ 익힘' : '카드 보기'));
        b.addEventListener('click', () => { index = order.indexOf(v); mode = 'cards'; flipped = false; render(); card.focus(); });
        return b;
      });
      list.replaceChildren(...(rows.length ? rows : [empty()]));
    }
    more.hidden = mode !== 'list' || listLimit >= order.length;
  }
  function resetFilters() {
    const b = button('전체 단어 보기');
    b.addEventListener('click', () => { query.value = ''; category.value = ''; onlyUnknown = false; select(); });
    return b;
  }
  function move(offset: number) {
    if (index + offset < 0 || index + offset >= order.length) return;
    index += offset; flipped = false; render(); status.textContent = `${index + 1}번째 카드, ${order[index]![language]}`;
  }
  function turn() {
    const current = order[index]; if (!current) return;
    flipped = !flipped; render(); status.textContent = flipped ? current.ko : current[language];
  }
  function mark(value: boolean) {
    const c = order[index]; if (!c) return;
    value ? known.add(key(c)) : known.delete(key(c)); persistKnown();
    if (value && onlyUnknown) { order.splice(index, 1); index = Math.min(index, Math.max(0, order.length - 1)); flipped = false; render(); }
    else if (index < order.length - 1) move(1);
    else { flipped = false; render(); }
    status.textContent = !order.length ? '남은 낯선 단어가 없어요. 전체 단어 보기로 돌아갈 수 있어요.' : value ? '익힌 표현에 표시했어요.' : '다시 볼 표현에 남겼어요.';
    if (!order.length) scene.querySelector<HTMLButtonElement>('button')?.focus();
  }
  function changeLanguage(nextLanguage: StudyLanguage) {
    if (language === nextLanguage) return;
    language = nextLanguage; select(true);
  }
  ja.addEventListener('click', () => changeLanguage('ja'));
  en.addEventListener('click', () => changeLanguage('en'));
  cardMode.addEventListener('click', () => { mode = 'cards'; render(); });
  listMode.addEventListener('click', () => { mode = 'list'; render(); });
  card.addEventListener('click', turn); flip.addEventListener('click', turn);
  previous.addEventListener('click', () => move(-1)); next.addEventListener('click', () => move(1));
  again.addEventListener('click', () => mark(false)); gotIt.addEventListener('click', () => mark(true));
  query.addEventListener('input', () => select()); category.addEventListener('change', () => select());
  unknown.addEventListener('click', () => { onlyUnknown = !onlyUnknown; select(); });
  mix.addEventListener('click', () => { sequence = shuffled(sequence); select(); status.textContent = '카드 순서를 섞었어요.'; });
  more.addEventListener('click', () => { listLimit += 40; render(); });
  root.addEventListener('keydown', (event) => {
    if (mode !== 'cards' || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || !(event.target instanceof HTMLElement)
      || event.target.matches('input, select, textarea') || event.target.isContentEditable) return;
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') { event.preventDefault(); move(event.key === 'ArrowLeft' ? -1 : 1); }
  });
  load.addEventListener('click', () => file.click());
  file.addEventListener('change', async () => {
    const chosen = file.files?.[0]; if (!chosen) return;
    try {
      if (chosen.size > 8 * 1024 * 1024) throw new Error('8MB 이하의 단어장 파일을 선택해 주세요.');
      const imported = parseDeck(JSON.parse(await chosen.text()));
      deck = imported; sequence = [...deck.cards]; query.value = ''; onlyUnknown = false; categories(); select();
      try { localStorage.setItem(DECK_KEY, JSON.stringify(imported)); savedDeck = imported; render(); message.textContent = `${deck.cards.length.toLocaleString()}개 표현을 이 브라우저에 보관했어요.`; }
      catch { message.textContent = '단어장을 열었지만 저장 공간이 부족해요. 창을 닫은 뒤에는 파일을 다시 불러와 주세요.'; }
    } catch (error) { message.textContent = error instanceof SyntaxError ? 'JSON 단어장 파일인지 확인해 주세요. 기존 단어장은 그대로예요.' : error instanceof Error ? error.message : '파일을 읽지 못했어요.'; }
    file.value = '';
  });
  basic.addEventListener('click', () => { deck = deck === original && savedDeck ? savedDeck : original; sequence = [...deck.cards]; query.value = ''; onlyUnknown = false; categories(); select(); message.textContent = `${deck === original ? '기본' : '보관한 내'} 단어장을 열었어요. 단어장 파일과 학습 표시는 유지돼요.`; });
  forget.addEventListener('click', () => {
    try { localStorage.removeItem(DECK_KEY); }
    catch { message.textContent = '브라우저의 저장된 단어장을 지우지 못했어요. 브라우저 설정에서 이 사이트 데이터를 확인해 주세요.'; return; }
    savedDeck = undefined; deck = original; sequence = [...deck.cards]; query.value = ''; onlyUnknown = false; categories(); select();
    message.textContent = '이 기기의 단어장 사본을 지웠어요. Notion 원본과 학습 표시는 유지돼요.';
  });
  categories(); select();
  return root;
}
