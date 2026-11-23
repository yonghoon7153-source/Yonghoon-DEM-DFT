import { fetchStudyDeck, parseConnection, type StudyConnection } from './study-sync';
import initialDeck from '../../data/word-cards.json';
import words from '../../data/words.json';
import { el } from './dom';
import { dailyCards, matchesCard, parseDeck, seoulStudyDay, shuffled, type StudyLanguage, type WordCard, type WordDeck } from './word-deck';

const DECK_KEY = 'nihonchizu.private-deck.v1';
const KNOWN_KEY = 'nihonchizu.known-cards.v1';

export function createWordCards() {
  const original = parseDeck(initialDeck);
  const known = new Set<string>();
  let marksWarning = '';
  try {
    const marks: unknown = JSON.parse(localStorage.getItem(KNOWN_KEY) || '[]');
    if (!Array.isArray(marks) || !marks.every((s) => typeof s === 'string')) throw new Error('Invalid marks');
    for (const mark of marks) known.add(mark);
  } catch { marksWarning = '이전 학습 표시를 읽지 못했어요. 새 표시는 이번 화면에서만 유지해요.'; }
  const conversation = createCardPanel(original, known, marksWarning);
  const records = createCardPanel(undefined, known, marksWarning);
  const sections = [conversation, records];
  const root = el('section', { class: 'study', 'aria-label': '단어 카드로 복습하기' });
  const tablist = el('div', { class: 'study__sections', role: 'tablist', 'aria-label': '학습 단어장' });
  const tabs = ['생활회화', '내 일본어 기록'].map((label, i) =>
    el('button', { type: 'button', role: 'tab', class: 'study__section-tab', id: `word-tab-${i}`, 'aria-controls': `word-panel-${i}` }, label));
  const panels = tabs.map((tab, i) => el('div', { role: 'tabpanel', id: `word-panel-${i}`, 'aria-labelledby': tab.id }));
  tablist.append(...tabs);
  root.append(tablist, ...panels);
  let active = -1;
  function open(i: number) {
    if (active === i) { sections[i]!.enter(); return; }
    if (active >= 0) { sections[active]!.pause(); panels[active]!.replaceChildren(); }
    active = i;
    tabs.forEach((tab, n) => {
      tab.setAttribute('aria-selected', String(n === i));
      tab.tabIndex = n === i ? 0 : -1;
      panels[n]!.hidden = n !== i;
    });
    panels[i]!.append(sections[i]!.root);
    sections[i]!.enter();
  }
  tabs.forEach((tab, i) => tab.addEventListener('click', () => open(i)));
  tablist.addEventListener('keydown', (event) => {
    let i = active;
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') i = 1 - active;
    else if (event.key === 'Home') i = 0;
    else if (event.key === 'End') i = 1;
    else return;
    event.preventDefault(); open(i); tabs[i]!.focus();
  });
  open(records.connected ? 1 : 0);
  const refreshActive = () => sections[active]!.refresh();
  function scheduleMidnight() {
    window.setTimeout(() => { refreshActive(); scheduleMidnight(); }, Math.max(1, seoulStudyDay().nextMidnight - Date.now()));
  }
  scheduleMidnight();
  window.setTimeout(refreshActive, 0);
  window.setInterval(refreshActive, 5 * 60 * 1000);
  window.addEventListener('focus', refreshActive);
  window.addEventListener('pageshow', refreshActive);
  window.addEventListener('hashchange', () => window.setTimeout(() => {
    if (root.isConnected && !root.closest('[hidden]')) sections[active]!.enter();
  }, 0));
  document.addEventListener('visibilitychange', refreshActive);
  return root;
}

function createCardPanel(original: WordDeck | undefined, known: Set<string>, marksWarning: string) {
  const isPublic = !!original;
  // An unconnected personal tab has no cards and opens its import prompt.
  const emptyDeck: WordDeck = { schemaVersion: 1, deckId: '', title: '', cards: [] };
  let deck = original ?? emptyDeck, language: StudyLanguage = 'ja', mode: 'cards' | 'list' = 'cards';
  let index = 0, flipped = false, onlyUnknown = false, order: WordCard[] = [];
  let storageWarning = marksWarning;
  let savedDeck: WordDeck | undefined;
  let connection: StudyConnection | undefined, revision = '';
  let request: AbortController | undefined, generation = 0, lastAttempt = 0;
  let importing = false;
  try {
    const saved = !isPublic && localStorage.getItem(DECK_KEY);
    if (saved) {
      const raw = JSON.parse(saved); savedDeck = parseDeck(raw); deck = savedDeck;
      // A broken connection must not discard a usable cached deck.
      try {
        if (raw.studyConnection) {
          const candidate = parseConnection(raw.studyConnection);
          if (candidate.deckId !== deck.deckId) throw new Error('Deck mismatch');
          connection = candidate;
          if (typeof raw.studyRevision === 'string' && /^[a-f0-9]{64}$/.test(raw.studyRevision)) revision = raw.studyRevision;
        }
      } catch { storageWarning = '단어장은 열었지만 자동 연결 정보를 읽지 못했어요. 연결 파일을 다시 불러와 주세요.'; }
    }
  } catch { storageWarning = '저장된 단어장을 읽지 못했어요. 연결 파일이나 단어장 파일을 다시 불러와 주세요.'; }

  const root = el('div', {});
  const name = el('h2', { class: 'study__title' });
  const subtitle = el('p', { class: 'study__subtitle' });
  const message = el('p', { class: 'study__message', role: 'status' }, storageWarning);
  const status = el('p', { class: 'sr-only', role: 'status', 'aria-live': 'polite', 'aria-atomic': 'true' });
  const button = (label: string, cls = 'study__button') => el('button', { type: 'button', class: cls }, label);
  const ja = button('日本語', 'study__tab'), en = button('English', 'study__tab');
  const today = button('오늘', 'study__tab'), all = button('전체', 'study__tab');
  const scopes = el('div', { class: 'study__tabs', role: 'group', 'aria-label': '복습할 단어 범위' }, today, all);
  const cardMode = button('카드', 'study__tab'), listMode = button('목록', 'study__tab');
  const tabs = el('div', { class: 'study__tabs', role: 'group', 'aria-label': '학습 언어' }, ja, en);
  const modes = el('div', { class: 'study__tabs', role: 'group', 'aria-label': '보기 방식' }, cardMode, listMode);
  const query = el('input', { class: 'study__search', type: 'search', placeholder: '단어·뜻 검색', 'aria-label': '단어 또는 뜻 검색', autocomplete: 'off' });
  const category = el('select', { class: 'study__select', 'aria-label': isPublic ? '상황별로 고르기' : '기록 분류로 고르기' });
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
  const connect = button('내 Notion 단어장 연결');
  const welcome = el('div', { class: 'study__connect' },
    el('h2', { class: 'study__connect-title' }, '오늘 복습할 일본어'),
    el('p', {}, '이 브라우저에서 오늘의 카드를 보려면 개인 연결 파일(study-connection.json)을 한 번 불러와 주세요.'),
    el('div', { class: 'study__connect-actions' }, connect,
      el('a', { class: 'study__text-button', href: words.today.reviewUrl, target: '_blank', rel: 'noopener noreferrer' }, 'Notion에서 오늘 목록 열기')));
  const forget = button('이 기기의 단어장 지우기', 'study__text-button');
  const syncMessage = el('p', { class: 'study__save-note', role: 'status' });
  const refresh = button('지금 새로 받기', 'study__text-button');
  const importPanel = el('details', { class: 'study__import' },
    el('summary', {}, '단어장 연결 관리'),
    el('p', {}, '채팅에서 받은 연결 파일이나 단어장 JSON을 골라 주세요. 연결 파일은 처음 한 번만 불러오면 돼요. 파일과 학습 표시는 이 브라우저에 보관해요.'),
    el('div', { class: 'study__import-actions' }, load, forget, refresh),
  );
  const studyView = el('div', {},
    el('div', { class: 'study__top' }, el('div', {}, name, subtitle), modes),
    el('div', { class: 'study__toolbar' }, scopes, tabs, mix),
    el('div', { class: 'study__filters' }, query, category, unknown),
    el('div', { class: 'study__meta' }, count, learned), progress,
    scene, navigation, ratings, detail, source, list, more,
    el('p', { id: 'study-shortcuts', class: 'study__shortcuts' }, '카드를 눌러 뒤집기 · 카드에서 ← → 이동 · Space로 뜻 보기'),
    el('p', { class: 'study__save-note' }, '학습 표시는 이 브라우저에 저장돼요. Notion 암기 기록은 바뀌지 않아요.'),
    syncMessage,
  );
  if (!isPublic) root.append(welcome, file);
  root.append(studyView);
  if (!isPublic) root.append(importPanel);
  root.append(message, status);

  const key = (c: WordCard) => `${deck.deckId}:${language}:${c.id}`;
  function persistKnown() {
    if (marksWarning) { message.textContent = marksWarning; return; }
    try { localStorage.setItem(KNOWN_KEY, JSON.stringify([...known])); }
    catch { message.textContent = '학습 표시는 이번 화면에서만 유지돼요. 브라우저 저장 공간을 확인해 주세요.'; }
  }
  let day = seoulStudyDay();
  let scope: 'today' | 'all' = isPublic || deck.today ? 'today' : 'all';
  let available: WordCard[] = [];
  let mixedIds: string[] | undefined;
  function preparePool() {
    const selectedCategory = category.value;
    available = scope === 'today' ? dailyCards(deck, language, day, isPublic) : deck.cards.filter((c) => c[language]);
    if (mixedIds) {
      const remaining = new Map(available.map((c) => [c.id, c]));
      const kept: WordCard[] = [];
      for (const id of mixedIds) {
        const c = remaining.get(id);
        if (c) { kept.push(c); remaining.delete(id); }
      }
      available = kept.concat([...remaining.values()]);
    }
    category.replaceChildren(el('option', { value: '' }, isPublic ? '모든 상황' : '모든 분류'),
      ...[...new Set(available.map((c) => c.category))].sort().map((c) => el('option', { value: c }, c)));
    if ([...category.options].some((o) => o.value === selectedCategory)) category.value = selectedCategory;
  }
  function select(preserve = false) {
    const currentId = preserve ? order[index]?.id : undefined;
    const previousIndex = index;
    order = available.filter((c) => matchesCard(c, query.value)
      && (!category.value || c.category === category.value) && (!onlyUnknown || !known.has(key(c))));
    const found = currentId ? order.findIndex((c) => c.id === currentId) : -1;
    index = preserve ? (found >= 0 ? found : Math.min(previousIndex, Math.max(0, order.length - 1))) : 0;
    flipped = false; listLimit = 40; render();
  }
  function render() {
    const c = order[index];
    const needsConnection = !isPublic && !savedDeck;
    welcome.hidden = !needsConnection;
    studyView.hidden = needsConnection;
    importPanel.hidden = needsConnection;
    if (needsConnection) return;
    name.textContent = isPublic ? '기본 생활 회화' : deck.title;
    const dateLabel = `${Number(day.key.slice(5, 7))}월 ${day.dayOfMonth}일`;
    subtitle.textContent = scope === 'today'
      ? `${dateLabel} · 한국 시간 · ${isPublic ? '기본 카드' : 'Notion 오늘'}`
      : isPublic || deck.today ? '전체 단어' : '전체 단어 · 이 파일에는 복습 날짜가 없어요.';
    scopes.hidden = !isPublic && !deck.today;
    today.setAttribute('aria-pressed', String(scope === 'today'));
    all.setAttribute('aria-pressed', String(scope === 'all'));
    [ja, en].forEach((b, i) => b.setAttribute('aria-pressed', String(language === (i ? 'en' : 'ja'))));
    [cardMode, listMode].forEach((b, i) => b.setAttribute('aria-pressed', String(mode === (i ? 'list' : 'cards'))));
    unknown.setAttribute('aria-pressed', String(onlyUnknown));
    learned.textContent = `익힌 표현 ${available.filter((v) => known.has(key(v))).length} / ${available.length}`;
    count.textContent = mode === 'list' ? `${order.length.toLocaleString()}개 표현` : `${c ? index + 1 : 0} / ${order.length}`;
    progress.max = Math.max(order.length, 1); progress.value = c ? index + 1 : 0;
    progress.hidden = mode !== 'cards';
    previous.disabled = !c || index === 0; next.disabled = !c || index === order.length - 1;
    flip.disabled = !c; mix.disabled = order.length < 2;
    ratings.hidden = !c || mode !== 'cards'; navigation.hidden = mode !== 'cards';
    list.hidden = mode !== 'list'; scene.hidden = mode !== 'cards';
    detail.hidden = !c || !flipped || mode !== 'cards'; source.hidden = !c?.notionUrl || mode !== 'cards';
    refresh.hidden = !connection;
    syncMessage.hidden = !connection;
    if (connection && !syncMessage.textContent) syncMessage.textContent = '매일 오전 9시에 정리한 단어장을 화면을 열어 둔 동안 5분마다 확인해요.';
    if (c?.notionUrl) source.href = c.notionUrl; else source.removeAttribute('href');
    const noDaily = scope === 'today' && !available.length;
    const empty = () => el('div', { class: 'study__empty' },
      el('h3', {}, noDaily ? `${dateLabel}에 복습할 표현이 없어요` : onlyUnknown ? '남은 낯선 단어가 없어요' : '찾는 표현이 아직 없어요'),
      resetFilters());
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
    b.addEventListener('click', () => { query.value = ''; category.value = ''; onlyUnknown = false; scope = 'all'; preparePool(); select(); });
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
    language = nextLanguage; preparePool(); select(true);
  }
  function changeScope(nextScope: typeof scope) {
    if (scope === nextScope) return;
    scope = nextScope; mixedIds = undefined; preparePool(); select();
  }
  today.addEventListener('click', () => changeScope('today'));
  all.addEventListener('click', () => changeScope('all'));
  ja.addEventListener('click', () => changeLanguage('ja'));
  en.addEventListener('click', () => changeLanguage('en'));
  cardMode.addEventListener('click', () => { mode = 'cards'; render(); });
  listMode.addEventListener('click', () => { mode = 'list'; render(); });
  card.addEventListener('click', turn); flip.addEventListener('click', turn);
  previous.addEventListener('click', () => move(-1)); next.addEventListener('click', () => move(1));
  again.addEventListener('click', () => mark(false)); gotIt.addEventListener('click', () => mark(true));
  query.addEventListener('input', () => select()); category.addEventListener('change', () => select());
  unknown.addEventListener('click', () => { onlyUnknown = !onlyUnknown; select(); });
  mix.addEventListener('click', () => { mixedIds = shuffled(deck.cards).map((c) => c.id); preparePool(); select(); status.textContent = '카드 순서를 섞었어요.'; });
  more.addEventListener('click', () => { listLimit += 40; render(); });
  root.addEventListener('keydown', (event) => {
    if (mode !== 'cards' || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || !(event.target instanceof HTMLElement)
      || event.target.matches('input, select, textarea') || event.target.isContentEditable) return;
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') { event.preventDefault(); move(event.key === 'ArrowLeft' ? -1 : 1); }
  });
  load.addEventListener('click', () => file.click());
  connect.addEventListener('click', () => file.click());
  function cancelRefresh() { generation++; request?.abort(); request = undefined; }
  function persistDeck() {
    if (!savedDeck) return;
    try {
      localStorage.setItem(DECK_KEY, JSON.stringify({ ...savedDeck, studyConnection: connection, studyRevision: revision }));
    } catch { message.textContent = '이번 화면에서는 사용할 수 있지만 저장 공간이 부족해요. 창을 닫은 뒤에는 연결 파일이나 단어장을 다시 불러와 주세요.'; }
  }
  function showDeck(nextDeck: WordDeck, preserve = false) {
    const sameDeck = preserve && deck.deckId === nextDeck.deckId;
    const resetReview = !sameDeck || Boolean(deck.today) !== Boolean(nextDeck.today);
    deck = nextDeck;
    if (resetReview) {
      resetPersonalReview();
      if (!sameDeck) mode = 'cards';
    }
    preparePool(); select(!resetReview);
  }
  function resetPersonalReview() {
    language = 'ja'; scope = deck.today ? 'today' : 'all';
    query.value = ''; category.value = ''; onlyUnknown = false; mixedIds = undefined;
  }
  function installDeck(imported: WordDeck, preserve: boolean) {
    const focusNewDeck = !savedDeck && root.isConnected &&
      (document.activeElement === document.body || document.activeElement === file || document.activeElement === connect);
    savedDeck = imported;
    showDeck(imported, preserve);
    if (focusNewDeck) (order.length ? card : ja).focus({ preventScroll: true });
  }
  async function receive(candidate: StudyConnection, connecting = false) {
    if (request) return;
    const token = generation, controller = new AbortController(); request = controller; lastAttempt = Date.now();
    const timeout = window.setTimeout(() => controller.abort(), 20000);
    syncMessage.textContent = '새 단어장을 확인하고 있어요…';
    try {
      const result = await fetchStudyDeck(candidate, controller.signal);
      if (token !== generation || (!connecting && connection !== candidate)) return;
      // Older clients cached the revision after stripping the daily index from the deck.
      const changed = connecting || result.revision !== revision || (!!result.deck.today && !deck.today);
      if (changed) {
        connection = candidate; revision = result.revision;
        installDeck(result.deck, !connecting);
        if (connecting) message.textContent = '자동 갱신을 연결했어요. 다음부터는 연결 파일을 다시 고르지 않아도 돼요.';
        persistDeck(); render();
      }
      syncMessage.textContent = `${new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })} 확인 · ${changed ? '새 단어장을 받았어요.' : '최신 단어장이에요.'} 화면을 열어 두면 5분마다 확인해요.`;
    } catch {
      if (token !== generation) return;
      const text = '새 단어장을 받지 못했어요. 기존 단어장과 학습 표시는 유지돼요. 잠시 후 다시 확인할게요.';
      syncMessage.textContent = text;
      if (connecting) message.textContent = '자동 연결을 확인하지 못했어요. 연결 파일과 인터넷 연결을 확인해 주세요. 기존 단어장은 그대로예요.';
    } finally {
      clearTimeout(timeout);
      if (request === controller) request = undefined;
    }
  }
  function maybeRefresh(force = false) {
    checkDay();
    if (importing || !connection || !root.isConnected || root.closest('[hidden]') || document.visibilityState !== 'visible') return;
    if (!force && Date.now() - lastAttempt < 5 * 60 * 1000) return;
    void receive(connection);
  }
  function checkDay() {
    const current = seoulStudyDay();
    if (current.key !== day.key) {
      day = current;
      if (scope === 'today') { mixedIds = undefined; preparePool(); select(); }
    }
  }
  refresh.addEventListener('click', () => maybeRefresh(true));
  file.addEventListener('change', async () => {
    const chosen = file.files?.[0]; if (!chosen) return;
    file.value = '';
    cancelRefresh(); const fileGeneration = generation;
    importing = true;
    message.textContent = '단어장 파일을 확인하고 있어요…';
    try {
      if (chosen.size > 8 * 1024 * 1024) throw new Error('8MB 이하의 단어장 파일을 선택해 주세요.');
      const raw: unknown = JSON.parse(await chosen.text());
      if (fileGeneration !== generation) return;
      if (raw && typeof raw === 'object' && 'kind' in raw && raw.kind === 'nihonchizu-study-connection') {
        const candidate = parseConnection(raw); await receive(candidate, true);
      } else {
        const imported = parseDeck(raw); connection = undefined; revision = ''; syncMessage.textContent = '';
        installDeck(imported, false); message.textContent = `${deck.cards.length.toLocaleString()}개 표현을 이 브라우저에 보관했어요.`;
        persistDeck(); render();
      }
    } catch (error) {
      if (fileGeneration === generation) message.textContent = error instanceof SyntaxError ? 'JSON 단어장 파일인지 확인해 주세요. 기존 단어장은 그대로예요.' : error instanceof Error ? error.message : '파일을 읽지 못했어요.';
    } finally {
      if (fileGeneration === generation) importing = false;
    }
  });
  forget.addEventListener('click', () => {
    try { localStorage.removeItem(DECK_KEY); }
    catch { message.textContent = '브라우저의 저장된 단어장을 지우지 못했어요. 브라우저 설정에서 이 사이트 데이터를 확인해 주세요.'; return; }
    cancelRefresh(); importing = false; connection = undefined; revision = ''; syncMessage.textContent = '';
    savedDeck = undefined; showDeck(emptyDeck); connect.focus();
    message.textContent = '이 기기의 단어장 사본을 지웠어요. Notion 원본과 학습 표시는 유지돼요.';
  });
  preparePool(); select();
  function pause() {
    if (importing) { importing = false; message.textContent = '불러오기를 멈췄어요. 이어서 연결하려면 파일을 다시 선택해 주세요.'; }
    if (request) { lastAttempt = 0; syncMessage.textContent = ''; }
    cancelRefresh();
  }
  function enter() {
    if (!isPublic && deck.today && (scope !== 'today' || language !== 'ja' || query.value || category.value || onlyUnknown)) {
      resetPersonalReview();
      preparePool(); select();
    }
    maybeRefresh();
  }
  return { root, connected: !!savedDeck, refresh: maybeRefresh, pause, enter };
}
