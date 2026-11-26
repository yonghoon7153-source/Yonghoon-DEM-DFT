import catalog from '../../data/study-videos.json';
import { el } from './dom';

interface Episode { date: string; title: string; japaneseTitle: string; durationSeconds: number }
const episodes: Episode[] = [...catalog];
episodes.sort((a, b) => b.date.localeCompare(a.date));
const archiveHash = '#words/videos';
const dateFormat = new Intl.DateTimeFormat('ko-KR', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' });

function dateLabel(date: string) {
  return dateFormat.format(new Date(date + 'T00:00:00Z'));
}

function durationLabel(seconds: number) {
  const whole = Math.floor(seconds);
  return `${Math.floor(whole / 60)}:${String(whole % 60).padStart(2, '0')}`;
}

function media(date: string, file: string) {
  return `${import.meta.env.BASE_URL}study-videos/${date}/${file}`;
}

export function createStudyVideos() {
  const root = el('section', { class: 'video-archive', 'aria-label': '오늘의 영상' });
  const stage = el('div', { class: 'video-archive__stage' });
  const queue = el('ol', { class: 'video-archive__queue', 'aria-label': '날짜별 영상' });
  const playlist = el('nav', { class: 'video-archive__list', 'aria-label': '영상 목록' },
    el('div', { class: 'video-archive__list-heading' },
      el('h2', {}, '재생목록'), el('span', {}, `${episodes.length}편`)), queue);
  root.append(stage, playlist);
  const links = new Map<string, HTMLAnchorElement>();
  for (const ep of episodes) {
    const link = el('a', { class: 'video-archive__episode', href: `${archiveHash}/${ep.date}` },
      el('span', { class: 'video-archive__thumb' },
        el('img', { src: media(ep.date, 'poster.webp'), alt: '', loading: 'lazy', decoding: 'async' }),
        el('span', { class: 'video-archive__length' }, durationLabel(ep.durationSeconds))),
      el('span', { class: 'video-archive__episode-info' },
        el('time', { datetime: ep.date }, dateLabel(ep.date)), el('strong', {}, ep.title)));
    links.set(ep.date, link);
    queue.append(el('li', {}, link));
  }
  let active: string | undefined;
  let player: HTMLVideoElement | undefined;

  function pause() { player?.pause(); }
  function show(date?: string) {
    const ep = date ? episodes.find((entry) => entry.date === date) : episodes[0];
    if (ep && ep.date === active) return;
    pause();
    player = undefined;
    active = ep?.date;
    for (const [key, link] of links) {
      if (key === active) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    }
    if (!ep) {
      stage.replaceChildren(el('div', { class: 'video-archive__empty' },
        el('p', {}, date ? '이 날짜에 등록된 영상이 없어요.' : '아직 등록된 영상이 없어요.'),
        episodes.length && date ? el('a', { href: archiveHash }, '최근 영상 보기') : null));
      return;
    }
    const movie = media(ep.date, 'lesson.mp4');
    player = el('video', { class: 'video-archive__player', controls: '', playsinline: '', preload: 'metadata',
      poster: media(ep.date, 'poster.webp'), 'aria-label': ep.title },
      el('source', { src: movie, type: 'video/mp4' }));
    const fallback = el('p', { class: 'video-archive__error', role: 'status', hidden: '' },
      '영상을 재생하기 어려워요. ', el('a', { href: movie }, 'MP4 직접 열기'));
    const markError = () => { fallback.hidden = false; };
    player.addEventListener('error', markError);
    player.querySelector('source')!.addEventListener('error', markError);
    stage.replaceChildren(el('div', { class: 'video-archive__screen' }, player), fallback,
      el('time', { class: 'video-archive__date', datetime: ep.date }, dateLabel(ep.date)),
      el('h2', { class: 'video-archive__title' }, ep.title),
      el('p', { class: 'video-archive__ja', lang: 'ja' }, ep.japaneseTitle));
  }
  return { root, show, pause };
}
