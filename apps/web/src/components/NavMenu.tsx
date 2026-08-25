/** 측정 종류로 묶은 상단 메뉴.
 *
 *  섹션이 셋이 되면서 링크를 한 줄로 늘어놓을 수 없게 됐다 — '비교' 는 충방전
 *  안의 화면이고 'DRT' 는 다른 측정인데, 나란히 서면 같은 층위로 읽힌다.
 *  섹션 이름만 보이고 그 안은 눌러서 편다.
 *
 *  키보드로도 되어야 한다.  Escape 로 닫고, 밖을 누르면 닫히고, 링크를 고르면
 *  닫힌다 — 마지막 것이 없으면 화면이 바뀐 뒤에도 메뉴가 떠 있어서 새 화면의
 *  절반을 가린다.
 */

import { useEffect, useId, useRef, useState } from 'react'
import { NavLink, useLocation } from 'react-router-dom'

export interface NavLinkSpec {
  to: string
  label: string
  /** 아직 없는 화면.  숨기지 않고 눌리지 않게 둔다 — 무엇이 올지 보인다. */
  soon?: boolean
}

export interface NavSection {
  label: string
  links: NavLinkSpec[]
}

export function NavMenu({ section }: { section: NavSection }) {
  const [open, setOpen] = useState(false)
  const wrapRef = useRef<HTMLDivElement>(null)
  const location = useLocation()
  const id = useId()

  const active = section.links.some(
    (link) => !link.soon && isUnder(location.pathname, link.to),
  )

  useEffect(() => {
    if (!open) return undefined
    const onDown = (event: MouseEvent) => {
      if (!wrapRef.current?.contains(event.target as Node)) setOpen(false)
    }
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setOpen(false)
    }
    document.addEventListener('mousedown', onDown)
    document.addEventListener('keydown', onKey)
    return () => {
      document.removeEventListener('mousedown', onDown)
      document.removeEventListener('keydown', onKey)
    }
  }, [open])

  return (
    <div className="nav-menu" ref={wrapRef}>
      <button
        type="button"
        className={active ? 'active' : ''}
        aria-expanded={open}
        aria-controls={id}
        aria-haspopup="true"
        onClick={() => setOpen((value) => !value)}
      >
        {section.label}
        <span className="chevron" aria-hidden="true">
          ▾
        </span>
      </button>
      {open ? (
        <div className="nav-drop" id={id} role="menu">
          {section.links.map((link) =>
            link.soon ? (
              <span key={link.to} className="soon" role="menuitem" aria-disabled="true">
                {link.label}
                <span className="tiny faint"> 준비 중</span>
              </span>
            ) : (
              <NavLink
                key={link.to}
                to={link.to}
                role="menuitem"
                className={({ isActive }) => (isActive ? 'active' : '')}
                onClick={() => setOpen(false)}
              >
                {link.label}
              </NavLink>
            ),
          )}
        </div>
      ) : null}
    </div>
  )
}

/** `/eis/12` 는 `/eis` 아래다.  `/samples` 가 `/sample` 을 삼키지는 않는다. */
export function isUnder(pathname: string, to: string): boolean {
  return pathname === to || pathname.startsWith(`${to}/`)
}
