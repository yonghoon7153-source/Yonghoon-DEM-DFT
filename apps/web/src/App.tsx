import { NavLink, Navigate, Route, Routes } from 'react-router-dom'

import { Compare } from './pages/Compare'
import { Dashboard } from './pages/Dashboard'
import { Library } from './pages/Library'
import { SampleDetail } from './pages/SampleDetail'
import { Upload } from './pages/Upload'

const LINKS = [
  { to: '/dashboard', label: '대시보드' },
  { to: '/samples', label: '셀 라이브러리' },
  { to: '/compare', label: '비교' },
  { to: '/upload', label: '업로드' },
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
          {LINKS.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) => (isActive ? 'active' : '')}
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
        <span className="spacer" />
      </header>

      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/samples" element={<Library />} />
        <Route path="/samples/:id" element={<SampleDetail />} />
        <Route path="/compare" element={<Compare />} />
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
