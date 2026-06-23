# 서버에 COMSOL 6.4 설치 (헤드리스 리눅스 + GPU/cuDSS)

대상: NVIDIA GPU 리눅스 서버(예: RTX A6000), GUI 없음(SSH only).
목표: COMSOL 6.4 무인(silent) 설치 + GPU Compute Components(cuDSS) 포함.

> **전제:** COMSOL Access 계정 보유. COMSOL은 **공개 직링크가 없고** 다운로드가 로그인에
> 묶여 있다. 아래 1단계에서 "인증된 링크를 서버로 가져오는" 방법을 쓴다.

---

## 0. 사전 점검

```bash
df -h /opt           # 여유공간 확인. ISO ~15GB + 설치 수십GB → /opt 권장(루트 홈은 보통 작음)
nproc; free -h       # 코어/메모리
nvidia-smi           # GPU/드라이버 (cuDSS는 최신 NVIDIA 드라이버 필요, 보통 OK)
```

---

## 1. 설치 파일(전체 ISO) 받기

COMSOL 6.4 다운로드 페이지: `https://www.comsol.com/product-download/6.4`
→ 로그인 → **COMSOL 6.4** → **"Full product" (오프라인 ISO)** 선택.
(ISO는 크로스플랫폼이라 하나로 Linux 설치 가능. "Online Installer"는 헤드리스에 비권장.)

### 방법 A — 브라우저 링크를 서버에서 받기 (서버 회선이 빠를 때)

인증된 다운로드라 **단순 wget은 403**이 나기 쉽다. 브라우저 확장으로 "쿠키 포함 명령"을 떠서 옮긴다:

1. 로컬 브라우저에 **cliget**(Firefox) 또는 **CurlWget / Copy as cURL**(Chrome) 설치
2. COMSOL 다운로드 버튼 클릭 → 확장이 만들어준 `curl ...`(또는 `wget ...`) **명령 전체 복사**
   (또는 Chrome DevTools ▸ Network ▸ 다운로드 요청 우클릭 ▸ *Copy as cURL*)
3. 서버에 붙여넣고 파일명만 지정:
   ```bash
   cd /opt
   curl -L -o comsol64.iso "붙여넣은_URL"   # 또는 확장이 준 curl 명령 그대로 + `-o comsol64.iso`
   ```

### 방법 B — 로컬에 받아서 scp (가장 확실)

로컬(윈도우)에서 ISO 다운로드 후:
```powershell
scp "C:\경로\COMSOL_6.4_xxx.iso" root@121.78.116.27:/opt/comsol64.iso
```

다운로드 검증(체크섬 제공 시):
```bash
ls -lh /opt/comsol64.iso
# 페이지에 SHA256 있으면:  sha256sum /opt/comsol64.iso
```

---

## 2. ISO 마운트

```bash
mkdir -p /mnt/comsol
mount -o loop /opt/comsol64.iso /mnt/comsol
ls /mnt/comsol            # setup, setupconfig.ini 등이 보여야 함
```

---

## 3. 무인 설치 답안파일(setupconfig.ini) 준비

ISO 루트의 템플릿을 복사해서 편집한다. **이 템플릿은 모든 옵션이 주석으로 설명돼 있다.**

```bash
cp /mnt/comsol/setupconfig.ini /opt/setupconfig.ini
nano /opt/setupconfig.ini
```

최소로 바꿀 항목 세 개:
```ini
agree = 1                              # 라이선스 동의 (필수)
installdir = /usr/local/comsol64       # 설치 경로
license = 1718@라이선스서버            # ↓ 라이선스 종류에 맞게 (5단계 참고)
# license = /opt/license.dat           #   - 파일 방식이면 경로
# license = XXXXX-XXXXX-...            #   - passcode 방식이면 코드
```
나머지는 기본값으로 둬도 된다. 참고:
- **GPU Compute Components(cuDSS 포함)는 6.4 기본 선택**이라 따로 안 켜도 됨.
- "CUDA DNN Support"(대리모델 GPU 학습용)는 **기본 미선택** — 나중에 surrogate 학습까지 GPU로
  할 거면 그때 추가 설치.
- 클라이언트이므로 라이선스 매니저는 설치하지 않음(`licmanager`가 있으면 off/no).

---

## 4. 무인 설치 실행

```bash
/mnt/comsol/setup -s /opt/setupconfig.ini
```
- 로그는 보통 `~/.comsol` 또는 설치로그 파일에 남는다. 끝나면:
```bash
ls /usr/local/comsol64/bin/comsol            # 런처 존재 확인
```

> **X11 오류**(`cannot open display` 등)가 나면 가상 디스플레이로 감싼다:
> ```bash
> apt-get install -y xvfb         # (필요시)
> xvfb-run -a /mnt/comsol/setup -s /opt/setupconfig.ini
> ```

> **라이브러리 누락** 오류 시(예: libGL, libXrender) 흔한 의존성 설치:
> ```bash
> apt-get install -y libgl1 libglu1-mesa libxrender1 libxt6 libxext6 libxi6 libxtst6
> ```

---

## 5. 라이선스 설정 (FNL vs CPUL)

| 종류 | 설정 | 비고 |
|------|------|------|
| **FNL (플로팅 네트워크)** | `license = 포트@호스트` (기본 1718) | 서버가 라이선스 서버에 **네트워크로 닿아야** 함(방화벽/VPN). 윈도우에서 쓰던 그 서버 그대로. |
| **CPUL (CPU-locked)** | 이 서버 **hostid로 새 라이선스 발급** 필요 | 윈도우용을 복사 못 함. COMSOL Access에서 이 서버로 rehost/재발급. hostid: 아래. |

이미 설치했는데 라이선스만 바꾸려면(재설치 불필요):
```bash
# 환경변수로 지정 (가장 간단)
export LMCOMSOL_LICENSE_FILE=1718@라이선스서버
# 영구 적용:  echo 'export LMCOMSOL_LICENSE_FILE=1718@라이선스서버' >> ~/.bashrc
```
또는 `/usr/local/comsol64/license/license.dat` 로 라이선스 파일 배치.

CPUL용 hostid(서버 MAC 기반) 확인:
```bash
/usr/local/comsol64/license/glnxa64/lmutil lmhostid    # 설치 후
# 설치 전이면:  ip link    (eth0의 MAC을 COMSOL Access에 입력)
```

---

## 6. 설치 검증

```bash
/usr/local/comsol64/bin/comsol --version      # 6.4.x 출력되면 OK
```

파이프라인에 경로 등록 후 종합 점검:
```bash
cd ~/Yonghoon-DEM-DFT/comsol-gpu
sed -i 's#^COMSOL_BIN=.*#COMSOL_BIN=/usr/local/comsol64/bin/comsol#' config/server.env
bash scripts/check_env.sh
```
이때 **cuDSS 라이브러리**가 COMSOL 설치 폴더 안에서 잡혀야 한다:
```bash
find /usr/local/comsol64 -iname 'libcudss*' 2>/dev/null
```

GUI에서의 GPU 검증(원격 X 가능 시): `File ▸ Preferences ▸ Computing ▸ GPU Acceleration ▸ Verify CUDA Installation`.

---

## 7. 자주 나는 문제

| 증상 | 조치 |
|------|------|
| 다운로드 403/만료 | 브라우저 링크 재발급(세션 만료). cliget/Copy-as-cURL로 쿠키 포함 명령 사용, 또는 scp |
| `cannot open display` | `xvfb-run -a ./setup -s ...` |
| `libGL.so.1 not found` 등 | 위 6단계 의존성 apt 설치 |
| `comsol: command not found` | 풀경로 사용(`/usr/local/comsol64/bin/comsol`) 또는 PATH 추가 |
| 라이선스 오류(-15, -97 등) | FNL: 서버까지 네트워크/포트(1718, +데몬포트) 열렸는지. CPUL: hostid 일치 확인 |
| `/opt` 공간 부족 | 다른 파티션(`df -h`)에 ISO/installdir 지정 |

---

## 참고 출처
- [Installing COMSOL on Linux — KB 1086](https://www.comsol.com/support/knowledgebase/1086)
- [Running the COMSOL Installer — COMSOL 6.4 Docs](https://doc.comsol.com/6.4/doc/com.comsol.help.comsol/comsol_installation.02.012.html)
- [GPU Acceleration — COMSOL 6.4 Release Highlights](https://www.comsol.com/release/6.4/gpu-acceleration)
