import { NavLink, Navigate, Route, Routes } from 'react-router-dom'

import { WhoAmI } from './components/WhoAmI'
import { Compare } from './pages/Compare'
import { Dashboard } from './pages/Dashboard'
import { Eis } from './pages/Eis'
import { Library } from './pages/Library'
import { SampleDetail } from './pages/SampleDetail'
import { SpectrumDetail } from './pages/SpectrumDetail'
import { Upload } from './pages/Upload'

/** 내비게이션은 **측정 종류**로 묶는다 (ADR 0019).
 *
 *  충방전은 `.wrd`, 임피던스는 `.mpr` 이고 축도 화면도 다르다.  한 줄에 나란히
 *  놓으면 '비교' 와 '스펙트럼' 이 같은 층위로 읽히는데, 하나는 충방전 안의
 *  화면이고 하나는 다른 측정 전체다.  GITT 도 여기 한 칸으로 들어온다. */
const SECTIONS: { label: string; links: { to: string; label: string }[] }[] = [
  {
    label: '충방전',
    links: [
      { to: '/dashboard', label: '대시보드' },
      { to: '/samples', label: '셀 라이브러리' },
      { to: '/compare', label: '비교' },
      { to: '/upload', label: '업로드' },
    ],
  },
  {
    label: 'EIS',
    links: [{ to: '/eis', label: '스펙트럼' }],
  },
]

export function App() {
  return (
    <div className="shell">
      <header className="topbar">
        <NavLink to="/dashboard" className="brand">
          <span className="dot" />
          Battery Lab Workbench
        </NavLink>
        <nav className="nav">
          {SECTIONS.map((section, index) => (
            <span className="nav-section" key={section.label}>
              {index > 0 ? <span className="nav-divider" aria-hidden="true" /> : null}
              <span className="nav-label">{section.label}</span>
              {section.links.map((link) => (
                <NavLink
                  key={link.to}
                  to={link.to}
                  className={({ isActive }) => (isActive ? 'active' : '')}
                >
                  {link.label}
                </NavLink>
              ))}
            </span>
          ))}
        </nav>
        <span className="spacer" />
        <WhoAmI />
      </header>

      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/samples" element={<Library />} />
        <Route path="/samples/:id" element={<SampleDetail />} />
        <Route path="/compare" element={<Compare />} />
        <Route path="/eis" element={<Eis />} />
        <Route path="/eis/:id" element={<SpectrumDetail />} />
        <Route path="/upload" element={<Upload />} />
        <Route
          path="*"
          element={
            <main className="page">
              <div className="empty">
                <div className="big">없는 페이지입니다</div>
                <NavLink to="/dashboard">대시보드로 돌아가기</NavLink>
              </div>
            </main>
          }
        />
      </Routes>
    </div>
  )
}
