import { NavLink, Navigate, Route, Routes } from 'react-router-dom'

import { NavMenu, type NavSection } from './components/NavMenu'
import { WhoAmI } from './components/WhoAmI'
import { Compare } from './pages/Compare'
import { Dashboard } from './pages/Dashboard'
import { Eis } from './pages/Eis'
import { Gitt } from './pages/Gitt'
import { GittDetail } from './pages/GittDetail'
import { Library } from './pages/Library'
import { SampleDetail } from './pages/SampleDetail'
import { ScanDetail } from './pages/ScanDetail'
import { Scans } from './pages/Scans'
import { SpectrumDetail } from './pages/SpectrumDetail'
import { Upload } from './pages/Upload'

/** 내비게이션은 **측정 종류**로 묶는다 (ADR 0019).
 *
 *  섹션이 셋이 되면서 링크를 한 줄로 늘어놓을 수 없게 됐다.  '비교' 는 충방전
 *  안의 화면이고 'DRT' 는 다른 측정인데, 한 줄에 나란히 서면 같은 층위로
 *  읽힌다.  섹션 이름만 두고 그 안은 눌러서 편다.
 *
 *  GITT 는 아직 화면이 없다.  메뉴에서 빼는 대신 눌리지 않게 두는 것은,
 *  무엇이 올지 보이는 편이 "그건 없어요" 를 두 번 말하는 것보다 낫기 때문이다. */
const SECTIONS: NavSection[] = [
  {
    label: '충방전 프로파일 · 사이클',
    links: [
      { to: '/dashboard', label: '대시보드' },
      { to: '/samples', label: '셀 라이브러리' },
      { to: '/compare', label: '비교' },
      { to: '/upload', label: '업로드' },
    ],
  },
  {
    // SOC 스캔이 스펙트럼 목록과 같은 섹션에 있는 이유: 같은 `.mpr` 이고 같은
    // 회로로 맞춘다.  다른 링크인 이유: 스캔은 파일 하나가 한 줄이고 x축이
    // SOC 다.  스펙트럼 목록에 풀어 놓으면 한 파일이 스무 줄을 먹는다 (ADR 0022).
    label: 'EIS · DRT',
    links: [
      { to: '/eis', label: '스펙트럼' },
      { to: '/scans', label: 'SOC 스캔' },
    ],
  },
  {
    label: 'GITT',
    links: [{ to: '/gitt', label: 'pseudo-OCV · 확산계수' }],
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
          {SECTIONS.map((section) => (
            <NavMenu key={section.label} section={section} />
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
        <Route path="/scans" element={<Scans />} />
        <Route path="/scans/:sha256" element={<ScanDetail />} />
        <Route path="/gitt" element={<Gitt />} />
        <Route path="/gitt/:id" element={<GittDetail />} />
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
