import { NavLink, Navigate, Route, Routes } from 'react-router-dom'

import { FeedbackBell } from './components/FeedbackBell'
import { NavMenu, type NavSection } from './components/NavMenu'
import { UpdateBanner } from './components/UpdateBanner'
import { WhoAmI } from './components/WhoAmI'
import { Compare } from './pages/Compare'
import { Dashboard } from './pages/Dashboard'
import { Eis } from './pages/Eis'
import { EisCompare } from './pages/EisCompare'
import { EisDashboard } from './pages/EisDashboard'
import { EisLibrary } from './pages/EisLibrary'
import { EisUpload } from './pages/EisUpload'
import { Feedback } from './pages/Feedback'
import { GittCompare } from './pages/GittCompare'
import { GittDashboard } from './pages/GittDashboard'
import { GittDetail } from './pages/GittDetail'
import { GittLibrary } from './pages/GittLibrary'
import { GittUpload } from './pages/GittUpload'
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
    // 충방전과 **같은 네 화면**이다.  측정 종류가 다르다고 쓰는 방식까지
    // 다를 이유가 없다: 어느 섹션에서도 대시보드에서 시작해 라이브러리에서
    // 찾고 비교에서 겹쳐 보고 업로드로 넣는다.
    //
    // SOC 스캔이 링크에서 빠진 것은 없애서가 아니라 **올릴 때 정하는 것**이
    // 됐기 때문이다.  같은 `.mpr` 이고 같은 회로로 맞추므로 화면을 가를
    // 이유가 없고, 다른 것은 파일 하나가 스윕 하나냐 스물이냐 뿐이라
    // 라이브러리의 거르개 하나면 된다 (ADR 0022).
    label: 'EIS · DRT',
    links: [
      { to: '/eis', label: '대시보드' },
      { to: '/eis/library', label: '라이브러리' },
      { to: '/eis/compare', label: '비교' },
      { to: '/eis/upload', label: '업로드' },
    ],
  },
  {
    label: 'GITT',
    links: [
      { to: '/gitt', label: '대시보드' },
      { to: '/gitt/library', label: '라이브러리' },
      { to: '/gitt/compare', label: '비교' },
      { to: '/gitt/upload', label: '업로드' },
    ],
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
        {/* 오른쪽 위.  화면 어디에 있든 같은 자리에 있어야 "그때 적어 둬야지"
            가 실제로 적는 것으로 이어진다 — 메뉴 안에 넣으면 찾아 들어가야
            하고, 찾아 들어가야 하는 칸에는 아무도 안 적는다. */}
        <FeedbackBell />
        <WhoAmI />
      </header>

      <UpdateBanner />

      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/samples" element={<Library />} />
        <Route path="/samples/:id" element={<SampleDetail />} />
        <Route path="/compare" element={<Compare />} />
        <Route path="/eis" element={<EisDashboard />} />
        <Route path="/eis/library" element={<EisLibrary />} />
        <Route path="/eis/compare" element={<EisCompare />} />
        <Route path="/eis/upload" element={<EisUpload />} />
        {/* 스펙트럼 하나를 맞추는 화면은 그대로다 — 목록에서 들어온다.
            `/eis/spectra` 는 옛 `/eis` 를 대신한다: 즐겨찾기와 남이 준
            링크가 살아 있어야 한다. */}
        <Route path="/eis/spectra" element={<Eis />} />
        <Route path="/eis/:id" element={<SpectrumDetail />} />
        <Route path="/scans" element={<Scans />} />
        <Route path="/scans/:sha256" element={<ScanDetail />} />
        <Route path="/gitt" element={<GittDashboard />} />
        <Route path="/gitt/library" element={<GittLibrary />} />
        <Route path="/gitt/compare" element={<GittCompare />} />
        <Route path="/gitt/upload" element={<GittUpload />} />
        <Route path="/gitt/:id" element={<GittDetail />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/feedback" element={<Feedback />} />
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
