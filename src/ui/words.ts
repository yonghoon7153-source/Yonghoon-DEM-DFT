import words from '../../data/words.json';
import { el } from './dom';
import { createWordCards } from './word-cards';

// Cards are a reading view. Notion remains the source of the learning content.
export function createWordsPage() {
  const app = document.getElementById('app')!;
  const page = document.getElementById('words-page')!;
  const nav = document.getElementById('words-link')!;
  const mapContent = ['stage', 'panel', 'search', 'label-mode'].map((id) => document.getElementById(id)!);
  const home = location.pathname + location.search;
  // The existing header can wrap onto three rows on a narrow screen or with fallback fonts.
  const header = document.querySelector<HTMLElement>('.topbar')!;
  const headerSize = new ResizeObserver(() => {
    app.style.setProperty('--study-nav-top', `${Math.ceil(header.getBoundingClientRect().height) + 16}px`);
  });
  headerSize.observe(header);
  let returnHash = '';
  const back = el('a', { class: 'words__back', href: home }, '← 지도로 돌아가기');
  const title = el('h1', { id: 'words-title', tabindex: '-1' }, '오늘의 단어');
  const notebooks = el('div', { class: 'words__notebooks' });
  for (const note of words.notebooks) {
    notebooks.append(el('a', { class: 'words__notebook', href: note.url, target: '_blank', rel: 'noopener noreferrer' },
      el('span', { class: 'words__language', lang: note.lang }, note.label),
      el('span', {}, note.title),
      el('span', { class: 'words__arrow', 'aria-hidden': 'true' }, '↗'),
      el('span', { class: 'sr-only' }, ' (Notion, 새 탭)'),
    ));
  }
  const resources = el('ul', { class: 'words__resources' });
  for (const resource of words.resources) {
    resources.append(el('li', {}, el('a', {
      class: 'words__resource', href: resource.url, target: '_blank', rel: 'noopener noreferrer',
    },
      el('span', { class: 'words__resource-title' }, resource.title,
        el('span', { class: 'words__arrow', 'aria-hidden': 'true' }, '↗'),
      ),
      el('span', { class: 'words__resource-provider' }, resource.provider),
      el('span', { class: 'words__resource-description' }, resource.description),
      el('span', { class: 'sr-only' }, ' (새 탭)'),
    )));
  }
  page.append(el('div', { class: 'words' },
    back,
    el('header', { class: 'words__heading' },
      el('p', { class: 'words__eyebrow', lang: 'ja' }, '今日のことば'),
      title,
      el('p', { class: 'words__intro' }, '차곡차곡 모은 표현, 한 장씩 뒤집으며 익혀 봐요.'),
    ),
    createWordCards(),
    el('section', { class: 'words__note-link', 'aria-labelledby': 'words-note-title' },
      el('div', {}, el('p', { class: 'words__label' }, '나의 Notion 단어 노트'),
        el('h2', { id: 'words-note-title' }, words.today.title),
        el('p', { class: 'words__description' }, '전체 기록과 오늘 복습할 표현도 함께 살펴봐요.'),
      ),
      el('a', { class: 'words__open', href: words.today.url, target: '_blank', rel: 'noopener noreferrer' },
        'Notion에서 열기',
        el('span', { class: 'sr-only' }, ' (Notion, 새 탭)'),
      ),
    ),
    el('section', { class: 'words__related', 'aria-labelledby': 'words-related-title' },
      el('h2', { id: 'words-related-title' }, '함께 보는 회화 노트'), notebooks,
    ),
    el('section', { class: 'words__related', 'aria-labelledby': 'words-resources-title' },
      el('h2', { id: 'words-resources-title' }, '더 공부하고 싶다면'),
      el('p', { class: 'words__resource-intro' }, 'Codex 추천 · 상황별 회화와 단어의 쓰임을 확인하는 공식 학습 자료예요.'),
      resources,
    ),
  ));

  const isOpen = () => /^#\/?words$/.test(location.hash);
  nav.addEventListener('click', () => {
    if (!isOpen()) returnHash = location.hash;
  });
  function sync() {
    const open = isOpen();
    const wasOpen = !page.hidden;
    page.hidden = !open;
    app.classList.toggle('has-words', open);
    mapContent.forEach((node) => { node.inert = open; });
    if (open) {
      nav.setAttribute('aria-current', 'page');
      back.href = home + returnHash;
      document.title = '오늘의 단어 — にほんちず';
      if (!wasOpen) {
        page.scrollTop = 0;
        title.focus({ preventScroll: true });
      }
    } else {
      nav.removeAttribute('aria-current');
      document.title = 'にほんちず — 눌러 보는 일본 지도 🗾';
      if (wasOpen) nav.focus({ preventScroll: true });
    }
  }
  window.addEventListener('hashchange', sync);
  sync();
  return { isOpen };
}
