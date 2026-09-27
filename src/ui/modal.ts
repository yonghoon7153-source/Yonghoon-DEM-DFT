import { clear } from './dom';

export function createModal(root: HTMLElement) {
  const body = root.querySelector<HTMLElement>('#modal-body')!;
  let lastFocus: Element | null = null;

  function close() {
    if (root.hidden) return;
    root.hidden = true;
    clear(body);
    (lastFocus as HTMLElement | null)?.focus?.({ preventScroll: true });
  }
  /** `wide`: a page that needs room beside its main picture (the 23区 map and its ward cards). */
  function open(content: HTMLElement, opts: { wide?: boolean } = {}) {
    lastFocus = document.activeElement;
    clear(body);
    root.querySelector('.modal__card')?.classList.toggle('modal__card--wide', !!opts.wide);
    body.append(content);
    root.hidden = false;
    root.querySelector<HTMLButtonElement>('.modal__close')?.focus({ preventScroll: true });
    body.scrollTop = 0;
  }
  root.querySelectorAll('[data-close]').forEach((n) => n.addEventListener('click', close));
  return { open, close, isOpen: () => !root.hidden };
}
