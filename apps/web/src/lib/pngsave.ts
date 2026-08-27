/** 그림을 파일로 — 화면 해상도가 아니라 **인쇄 해상도**로.
 *
 *  화면 캡처로는 논문·발표에 못 쓴다.  브라우저 창의 그래프는 CSS 픽셀로
 *  600×320 쯤이고, 그것을 슬라이드에 붙여 키우면 글자부터 뭉개진다.  그래서
 *  캡처가 아니라 **다시 그린다**: 같은 옵션으로 3 배 크기의 캔버스에 새로
 *  그리고, 글꼴·선 굵기·눈금까지 같은 배로 키운다.  결과는 확대해도 선이
 *  선이고 글자가 글자다.
 *
 *  여기 있는 것은 그리는 쪽이 아니라 **담는 쪽**이다: 다 그린 캔버스를 받아
 *  제목·범례·꼬리말을 붙이고 파일로 내린다.  실제로 다시 그리는 일은
 *  `Plot`(uPlot) 과 `Plot3D`(직접 그리기) 가 각자 한다 — 그 둘은 그리는
 *  방법이 아예 다르고, 공통으로 뽑아 봐야 양쪽 다 어색해진다.
 */

/** 몇 배로 그릴까.  3 배면 600 px 그래프가 1800 px 이 되고, A4 한 단
 *  (약 8 cm) 에 넣었을 때 570 dpi 다 — 인쇄에 충분하고 파일은 아직 작다. */
export const PNG_SCALE = 3

/** uPlot 축 기본값 중 **배수를 곱해 줘야 하는 것들** (CSS 픽셀).
 *
 *  저장이 그림을 세 배로 그릴 때 여기를 안 키우면 눈금이 세 배로 촘촘해진다.
 *  `space` 는 "눈금 사이 최소 픽셀" 이라 (uPlot 1.6.32, `xAxisOpts.space = 50`,
 *  `yAxisOpts.space = 30`), 캔버스만 1800 px 이 되면 uPlot 은 "여기 눈금
 *  서른여섯 개가 들어가겠네" 로 읽는다.  글꼴은 같이 세 배라 그 서른여섯 개가
 *  서로 겹친다 — 실제로 GITT 그림의 가로 눈금이 `0.0250.050.075…` 로 붙어
 *  나왔다.
 *
 *  `size` 는 눈금 글자가 앉는 띠의 두께다.  이것도 안 키우면 33 px 글자가
 *  50 px 띠에 축 이름과 겹쳐 앉는다.
 */
export const AXIS_PX = {
  /** 가로 눈금 사이 최소 간격 (uPlot 기본값). */
  xSpace: 50,
  /** 가로 눈금 글자 띠의 두께 (uPlot 기본값). */
  xSize: 50,
  /** 세로 눈금 사이 최소 간격 (uPlot 기본값). */
  ySpace: 30,
  /** 세로 눈금 글자 띠 — 여기는 우리 값이다 (긴 수가 잘리지 않게 기본보다 넓다). */
  ySize: 58,
} as const

/** 저장한 그림의 눈금을 화면보다 **얼마나 성기게** 할까.
 *
 *  배수만 맞추면 저장한 그림이 화면과 똑같은 눈금 수를 갖는데, 그것도 종이에는
 *  촘촘하다.  화면은 커서를 올려 값을 읽을 수 있어서 눈금이 많아도 손해가 없지만
 *  종이에는 커서가 없다 — 사이클 추세를 저장했더니 가로가 `1 2 3 … 43` 이었다.
 *  읽는 사람이 원하는 것은 `10 20 30 40` 이다.
 *
 *  **가로와 세로가 다른 수인 이유**: 가로 눈금 글자는 나란히 누워 서로 부딪히고
 *  (`0.0250.050.075…` 로 붙어 나온 것이 그것이다), 세로 글자는 위아래로 쌓여
 *  부딪히지 않는다.  세로는 그냥 많을 뿐이라 덜 걷어내면 된다.
 *
 *  실측으로 골랐다 (진짜 크롬에서 uPlot 이 고른 눈금을 셋).  세로도 2 로 하면
 *  충방전 프로파일의 전압 축이 `3, 4` **두 칸**으로 무너진다:
 *
 *      구간            화면      x2·y1.5        x2·y2
 *      사이클 1~43     8 / 7     4 / 4          4 / 4
 *      0~225 mAh/g    10 / 5     5 / 5          5 / **2**
 *      0~1.5 mAh/cm²   8 / 4     4 / 4          4 / 4
 */
export const PNG_TICK_ROOM = { x: 2, y: 1.5 } as const

/** 그 값들을 배수만큼 키운 것.
 *
 *  `room` 은 눈금을 성기게 하는 몫이다 — 눈금 **간격**에만 곱하고 글자 띠
 *  두께에는 안 곱한다 (띠는 글자가 앉는 자리라 글꼴 배수만 따라간다).
 *  화면은 `{x: 1, y: 1}` 이라 예전 그대로다.
 */
export function axisPx(
  scale: number, room: { x: number; y: number } = { x: 1, y: 1 },
): Record<keyof typeof AXIS_PX, number> {
  return {
    xSpace: AXIS_PX.xSpace * scale * room.x,
    xSize: AXIS_PX.xSize * scale,
    ySpace: AXIS_PX.ySpace * scale * room.y,
    ySize: AXIS_PX.ySize * scale,
  }
}

export interface PngLegendItem {
  label: string
  color: string
  /** 점선으로 그린 곡선.  범례 조각도 점선이라야 그림과 맞는다. */
  dash?: boolean
}

export interface PngFrame {
  /** 다 그린 그래프.  이 캔버스의 **장치 픽셀** 크기가 결과의 기준이다. */
  plot: HTMLCanvasElement
  /** 장치 픽셀 / CSS 픽셀.  글자 크기를 여기에 맞춰 키운다. */
  ratio: number
  title?: string
  /** 제목 아래 한 줄 — 단위 기준, 이격 폭 같은 "이 그림을 읽는 법". */
  caption?: string
  legend?: PngLegendItem[]
  background: string
  text: string
  faint: string
}

/** 제목·범례를 붙여 한 장으로 만든다.
 *
 *  범례를 굳이 다시 그리는 이유: uPlot 의 범례는 캔버스가 아니라 DOM 이라
 *  캔버스에 안 담긴다.  그래프만 저장하면 열한 개 곡선이 색만 남고 이름이
 *  사라지는데, 그러면 그림 한 장으로는 아무것도 못 읽는다.
 */
export function composePng(frame: PngFrame): HTMLCanvasElement {
  const { plot, ratio } = frame
  const pad = Math.round(16 * ratio)
  const titleSize = Math.round(15 * ratio)
  const captionSize = Math.round(11 * ratio)
  const legendSize = Math.round(11 * ratio)
  const rowGap = Math.round(7 * ratio)
  const swatch = Math.round(16 * ratio)

  const width = plot.width
  const inner = width - pad * 2

  // 범례를 먼저 줄로 나눈다 — 몇 줄인지 알아야 캔버스 높이가 정해진다.
  const measure = document.createElement('canvas').getContext('2d')
  if (!measure) {
    // **조용히 넘어가지 않는다.**  글자 폭을 못 재면 제목도 범례도 자리를
    // 못 잡는다.  그 상태로 그림만 내보내면 "저장됨" 인데 이름이 없는 파일이
    // 나온다 (Codex 그림 리뷰 #11).
    throw new Error('글자 폭을 잴 수 없어 제목·범례를 그리지 못했습니다')
  }
  const rows: PngLegendItem[][] = []
  if (frame.legend?.length) {
    measure.font = `${legendSize}px Pretendard, system-ui, sans-serif`
    let row: PngLegendItem[] = []
    let at = 0
    for (const item of frame.legend) {
      const chip = swatch + Math.round(6 * ratio) + measure.measureText(item.label).width
      const step = chip + Math.round(14 * ratio)
      if (row.length && at + chip > inner) {
        rows.push(row)
        row = []
        at = 0
      }
      row.push(item)
      at += step
    }
    if (row.length) rows.push(row)
  }

  // **꼬리말을 감는다.**  한 줄로 그리면 폭을 넘은 만큼이 그냥 잘렸다 —
  // 그리고 잘리는 끝자락이 하필 `세로 눈금은 값이 아닙니다` 처럼 가장 남아야
  // 할 말이었다 (Codex 그림 리뷰 #5).  뜻 단위(` · `)로 먼저 끊고, 그래도
  // 넘치면 어절로 끊는다.
  measure.font = `${captionSize}px Pretendard, system-ui, sans-serif`
  const captionLines = frame.caption
    ? wrapText(measure, frame.caption, inner) : []
  const headHeight = frame.title
    ? titleSize + Math.round(6 * ratio)
      + (captionLines.length
        ? captionLines.length * (captionSize + Math.round(3 * ratio))
          + Math.round(1 * ratio)
        : 0)
    : 0
  const legendHeight = rows.length
    ? rows.length * legendSize + (rows.length - 1) * rowGap + Math.round(10 * ratio)
    : 0
  const height = pad + headHeight + plot.height + legendHeight + pad

  const out = document.createElement('canvas')
  out.width = width
  out.height = height
  const ctx = out.getContext('2d')
  if (!ctx) {
    // 그림만 돌려주면 제목·꼬리말·범례가 조용히 사라진 채 "저장됨" 이 된다.
    throw new Error('그림을 합칠 캔버스를 만들지 못했습니다')
  }

  // **배경을 칠한다.**  투명 PNG 를 어두운 슬라이드에 붙이면 검은 글씨가
  // 사라진다 — 그림이 없어진 것처럼 보이고 원인이 안 보인다.
  ctx.fillStyle = frame.background
  ctx.fillRect(0, 0, width, height)

  let y = pad
  if (frame.title) {
    ctx.fillStyle = frame.text
    ctx.font = `600 ${titleSize}px Pretendard, system-ui, sans-serif`
    ctx.textBaseline = 'top'
    ctx.fillText(frame.title, pad, y)
    y += titleSize + Math.round(6 * ratio)
    if (captionLines.length) {
      ctx.fillStyle = frame.faint
      ctx.font = `${captionSize}px Pretendard, system-ui, sans-serif`
      for (const line of captionLines) {
        ctx.fillText(line, pad, y)
        y += captionSize + Math.round(3 * ratio)
      }
      y += Math.round(1 * ratio)
    }
  }

  ctx.drawImage(plot, 0, y)
  y += plot.height + (rows.length ? Math.round(10 * ratio) : 0)

  {
    ctx.font = `${legendSize}px Pretendard, system-ui, sans-serif`
    ctx.textBaseline = 'top'
    for (const row of rows) {
      let at = pad
      for (const item of row) {
        ctx.strokeStyle = item.color
        ctx.lineWidth = Math.max(1, Math.round(2 * ratio))
        ctx.setLineDash(item.dash ? [Math.round(4 * ratio), Math.round(3 * ratio)] : [])
        ctx.beginPath()
        ctx.moveTo(at, y + legendSize / 2)
        ctx.lineTo(at + swatch, y + legendSize / 2)
        ctx.stroke()
        ctx.setLineDash([])
        ctx.fillStyle = frame.text
        ctx.fillText(item.label, at + swatch + Math.round(6 * ratio), y)
        at += swatch + Math.round(6 * ratio)
          + ctx.measureText(item.label).width + Math.round(14 * ratio)
      }
      y += legendSize + rowGap
    }
  }
  return out
}

/** 글자를 폭에 맞춰 여러 줄로.
 *
 *  먼저 뜻 단위(` · `)로 끊는다 — 캡션이 `이름 · 면적 · 이격` 이라 그 경계가
 *  사람이 읽는 경계와 같다.  한 조각이 그래도 넘치면 어절로 끊고, 어절
 *  하나가 넘으면 그 줄은 그대로 둔다 (글자 단위로 자르면 단위 기호가 갈린다).
 */
export function wrapText(
  ctx: CanvasRenderingContext2D, text: string, limit: number,
): string[] {
  if (!text) return []
  if (ctx.measureText(text).width <= limit) return [text]
  const lines: string[] = []
  let line = ''
  const flush = () => { if (line) { lines.push(line); line = '' } }
  const push = (piece: string, join: string) => {
    const next = line ? line + join + piece : piece
    if (line && ctx.measureText(next).width > limit) {
      flush()
      line = piece
      return
    }
    line = next
  }
  for (const chunk of text.split(' · ')) {
    if (ctx.measureText(chunk).width <= limit) {
      push(chunk, ' · ')
      continue
    }
    // 조각 하나가 한 줄을 넘는다 — 어절로 더 끊는다.
    flush()
    for (const word of chunk.split(/\s+/)) push(word, ' ')
    flush()
  }
  flush()
  return lines
}

/** 파일 이름에 못 쓰는 글자를 없앤다.  한글은 남긴다 — 셀 이름이 한글이다. */
export function safeFileName(text: string): string {
  return (text || 'plot')
    .replace(/[\\/:*?"<>|]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, 80) || 'plot'
}

/** 캔버스를 PNG 로 내린다.
 *
 *  `toBlob` 을 쓴다 (`toDataURL` 이 아니라): 3 배 그림은 수 MB 이고, data URI
 *  는 그 전체를 문자열로 만들었다가 다시 디코딩한다 — 큰 그림에서 탭이 몇 초
 *  멈춘다.  Blob URL 은 복사가 없다.
 */
export function downloadCanvas(
  canvas: HTMLCanvasElement, name: string,
): Promise<void> {
  // **콜백이 아니라 Promise 다.**  한 번의 저장은 단추의 `saving` 상태·재진입
  // 막기·blob 굽기·URL 만들기·링크 누르기·오류 표시가 **한 생명주기**다.
  // 콜백으로 두면 `finally` 가 굽기 전에 돌아 `saving` 이 먼저 풀리고, 저장을
  // 두 번 누르면 늦게 온 첫 실패가 이미 성공한 두 번째를 실패로 덮는다.
  // 콜백 안에서 난 예외도 바깥 `try` 가 못 잡는다 (Codex 그림 리뷰 #10).
  return new Promise<void>((resolve, reject) => {
    const finish = (url: string, revoke: boolean) => {
      try {
        const link = document.createElement('a')
        link.href = url
        link.download = `${safeFileName(name)}.png`
        document.body.appendChild(link)
        link.click()
        link.remove()
        if (revoke) setTimeout(() => URL.revokeObjectURL(url), 10_000)
        resolve()
      } catch (cause) {
        reject(cause instanceof Error ? cause : new Error(String(cause)))
      }
    }
    if (typeof canvas.toBlob === 'function') {
      canvas.toBlob((blob) => {
        if (!blob) {
          // 브라우저가 캔버스를 PNG 로 못 굽는 경우다 — 대개 너무 커서다.
          reject(new Error('브라우저가 이 크기의 그림을 만들지 못했습니다'))
          return
        }
        let url: string
        try {
          url = URL.createObjectURL(blob)
        } catch (cause) {
          reject(cause instanceof Error ? cause : new Error(String(cause)))
          return
        }
        finish(url, true)
      }, 'image/png')
      return
    }
    try {
      finish(canvas.toDataURL('image/png'), false)
    } catch (cause) {
      reject(cause instanceof Error ? cause : new Error(String(cause)))
    }
  })
}

/** `11px ...` 같은 CSS 글꼴 문자열의 크기만 배로. */
export function scaleFont(font: string, scale: number): string {
  return font.replace(/(\d+(?:\.\d+)?)px/, (_all, size: string) =>
    `${Math.round(Number(size) * scale * 100) / 100}px`)
}

/** SVG 로 그린 그림을 캔버스로 — 배를 키워서.
 *
 *  SVG 는 벡터라 **키워도 안 뭉갠다**: 3 배 캔버스에 그리면 3 배 해상도의
 *  그림이 그대로 나온다 (uPlot 처럼 다시 그릴 필요가 없다).  대신 함정이
 *  하나 있다 — `<img>` 로 불러들인 SVG 는 **문서와 완전히 분리된 세계**라,
 *  `var(--line)` 도 클래스(`.plot3d-tick`)도 안 산다.  화면에서는 멀쩡한
 *  그림이 저장하면 선이 검게, 글자가 기본 크기로 나오는 이유가 그것이다.
 *
 *  그래서 복제본을 만들고 **살아 있는 원본에서 계산된 값을 그대로 베껴**
 *  속성으로 박는다.  두 트리는 구조가 같으므로 나란히 걷는다.
 */
export async function svgToCanvas(
  svg: SVGSVGElement, scale: number, background: string,
): Promise<HTMLCanvasElement | null> {
  const rect = svg.getBoundingClientRect()
  const width = Math.max(1, Math.round(rect.width || svg.clientWidth || 900))
  const height = Math.max(1, Math.round(rect.height || svg.clientHeight || 520))

  const clone = svg.cloneNode(true) as SVGSVGElement
  const live = svg.querySelectorAll('*')
  const copy = clone.querySelectorAll('*')
  const carry = ['fill', 'stroke', 'stroke-width', 'stroke-dasharray',
                 'font-family', 'font-size', 'font-weight', 'opacity']
  for (let i = 0; i < live.length && i < copy.length; i += 1) {
    const from = window.getComputedStyle(live[i] as Element)
    const to = copy[i] as Element
    for (const key of carry) {
      const value = from.getPropertyValue(key)
      // `none` 은 지워야 할 값이 아니라 **뜻이 있는 값**이다 (선 없는 채움).
      if (value) to.setAttribute(key, value)
    }
    to.removeAttribute('class')
  }
  clone.setAttribute('width', String(width * scale))
  clone.setAttribute('height', String(height * scale))
  if (!clone.getAttribute('viewBox')) {
    clone.setAttribute('viewBox', `0 0 ${width} ${height}`)
  }
  clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg')

  const markup = new XMLSerializer().serializeToString(clone)
  const uri = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(markup)}`
  const image = new Image()
  image.src = uri
  await new Promise<void>((resolve, reject) => {
    if (typeof image.decode === 'function') {
      image.decode().then(() => resolve(), reject)
      return
    }
    image.onload = () => resolve()
    image.onerror = () => reject(new Error('SVG 를 그림으로 못 바꿨습니다'))
  })

  const canvas = document.createElement('canvas')
  canvas.width = width * scale
  canvas.height = height * scale
  const ctx = canvas.getContext('2d')
  if (!ctx) return null
  ctx.fillStyle = background
  ctx.fillRect(0, 0, canvas.width, canvas.height)
  ctx.drawImage(image, 0, 0, canvas.width, canvas.height)
  return canvas
}
