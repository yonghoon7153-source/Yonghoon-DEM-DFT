---
title: vps rollout
created: 2026-09-13
updated: 2026-09-13
type: guide
tags: [tooling, workflow, network]
sources: [docs/adr/0034-our-own-vps-in-front.md, tools/vps-setup.sh, tools/bml]
confidence: high
explored: false
verificationStatus: unverified
---

# VPS 로드맵 — `bmlonly` 를 없애기까지

## 왜 이걸 하나

지금 굴레는 이렇다.

    터널이 끊긴다 → bml share → **주소가 바뀐다** → 기계마다 bmlout <새 주소>
    → 랩 DNS 가 그 이름을 못 풀어 준다 → bmlonly <주소> <IP> → 또 끊긴다

한 바퀴에 사람 셋이 붙는다. 그리고 이 굴레는 **닫히지 않는다** — localhost.run
으로 주소를 고정하는 것은 이미 안 되는 것으로 확인됐다. 같은 키로도 바뀌었다:
`653712d5fb509b` → `d1c47a7b4af191` → `928ae9cbe83d4e` (`tools/bml` 의
`write_tunnel_keepalive` 주석에 실측이 적혀 있다).

주소가 고정되면 **`bmlonly` · 중계기(ADR 0030) · IP 전달이 통째로 없어진다.**
다른 기계는 `bmlout https://bml.bmlwork.kr` 을 한 번만 치면 되고, 재부팅해도
그대로다 ([[bml-command]] 의 자리 두 개 — 랩 안은 [[central-server]] 그대로다). 그것이 이 로드맵의 전부다.

결정과 근거는 ADR 0034 (`docs/adr/0034-our-own-vps-in-front.md`) 에 있다. 이 문서는 **그것을 실제로
세우는 순서**다.

## 지금 어디까지 와 있나

코드는 **다 있다.** 이번에 새로 만들 것은 없다.

| 있는 것 | 어디 |
|---|---|
| VPS 설치본 (nginx · sshd · certbot · 방화벽) | `tools/vps-setup.sh` (428줄) |
| 열렸는지만 재는 모드 | `sudo bash vps-setup.sh --check <도메인>` |
| 랩 PC 쪽 연결 | `tools/bml` 의 `tunnel_via_vps` |
| 설정 두 줄 | `bml share vps <사용자@호스트>` · `bml share domain <이름>` |
| 끊기면 다시 붙는 감독자 | `write_tunnel_keepalive` (20번 연속 즉사면 멈춤) |
| "그 200 을 우리가 냈는가" | `confirm_tunnel` → `wrong_instance` (Codex #8) |
| 적대 리뷰 22건 | [2026-08-27-codex-vps-result](../reviews/2026-08-27-codex-vps-result.md) — `verified` |

**한 번도 못 돌려 본 것**: 이 저장소 컨테이너에 nginx·sshd·certbot 이 없다.
그래서 ADR 이 승격 조건을 걸어 뒀다 — *버릴 수 있는 VPS 에서 10단계를 통과하기
전에는 실제 이름을 걸지 않는다.*

## 로드맵

### 0단계 — 기계 한 대 (30분, 사람)

Oracle Cloud Always Free 의 **AMD micro (1 GB)**. 요금이 안 나오고 이 일에
충분하다. Ubuntu 22.04/24.04.

Oracle 콘솔에서 **보안 목록에 80·443 인그레스**를 연다. 그리고 인스턴스 안에서
`iptables` 도 열려 있어야 한다 — Oracle 이미지는 두 층 다 막아 두고, **한 층만
열고 넘어가면 certbot 이 인증서 발급에서 멎는다.** 그 두 층을 재는 것이
`--check` 다.

> 이 단계는 **버릴 기계**다. 실제 이름을 걸기 전에 여기서 다 깨 본다.

### 1단계 — 관문 10개 (1시간, 대부분 기계가 한다)

ADR 0034 의 "올리기 전에" 를 순서대로. 버릴 VPS 에 임시 이름
(`test.bmlwork.kr`) 을 걸고 돈다.

```bash
# 그 VPS 에서
sudo bash vps-setup.sh --check test.bmlwork.kr      # 1. 80·443 두 층
sudo bash vps-setup.sh test.bmlwork.kr <메일>        # 2. certbot 까지 끝까지
sudo sshd -T -C user=bml-tunnel,host=x,addr=127.0.0.1 | grep gatewayports
                                                     # 3. → gatewayports no
```

```bash
# 랩 PC 에서
ssh-copy-id <사용자>@<VPS>
bml share vps <사용자>@<VPS>
bml share domain test.bmlwork.kr
bml share stop && bml share                          # 6. 공개 주소가 200
```

```bash
# 다시 VPS 에서
ss -H -ltn 'sport = :5003'                           # 4. 127.0.0.1 하나뿐
# 밖에서
nc -vz <VPS-IP> 5003                                 # 5. 실패해야 정상
```

6번은 **200 만으로 통과가 아니다.** 손으로도 한 번 맞춰 본다:

```bash
curl -s https://test.bmlwork.kr/api/health | grep -o '"instance":"[^"]*"'
curl -s http://127.0.0.1:5003/api/health  | grep -o '"instance":"[^"]*"'
```

두 `instance` 가 **같아야** 한다. 다르면 그 주소는 다른 워크벤치다 (DNS 가 옛
기계를 가리키거나, 저쪽 5003 을 옛 터널이 잡고 있다). `bml` 이 이 검사를
이미 한다 — 손으로 한 번 더 보는 이유는 이 관문이 *그 검사 자체*를 통과시키는
자리이기 때문이다.

나머지 넷:

- **7.** 랩 PC 랜을 뽑았다 꽂는다 → **90초 안에 저절로** 돌아온다
- **8.** `bml stop` → 저쪽 `ss` 에서 5003 이 사라지고, 랩 PC 에 ssh 도 감독자도 안 남는다
- **9.** VPS 재부팅 → 대문이 저절로 선다
- **10.** `sudo certbot renew --dry-run`

**하나라도 걸리면 여기서 멈추고 고친다.** 그게 이 단계의 목적이다 — 실제
이름에 처음 겪는 문제를 걸지 않는 것.

### 2단계 — 진짜 이름 (20분)

관문을 다 통과했으면 그때 실제 인스턴스에 같은 절차를 돌리고
`bml.bmlwork.kr` 을 건다. Cloudflare DNS 는 **회색 구름(DNS only)** 이다 —
주황 구름은 올리는 파일을 100 MB 로 막고 우리 상한은 512 MB 다. 랩 안에서
되던 업로드가 밖에서만 413 으로 죽고, 그 413 은 우리가 낸 것이 아닌데 화면은
우리 탓처럼 보인다.

버릴 VPS 는 그다음에 지운다. **먼저 지우지 않는다** — 실제 쪽이 막히면 돌아갈
곳이 있어야 한다.

### 3단계 — 다른 기계들 (기계당 1분)

```bash
bml pull && bmlout https://bml.bmlwork.kr
```

한 번이면 끝이다. 이후 재부팅해도, 랩 PC 를 재시작해도 그대로다.

### 4단계 — 낡은 길을 걷어내지는 않는다

`bmlonly` · 중계기 · localhost.run 갈래는 **지우지 않는다.** VPS 를 잃거나
22 가 막히는 날 돌아갈 곳이 있어야 한다 (ADR 0034 "대가"). 다만 화면이 그것을
**먼저** 권하지는 않게 되고, 그게 실질적인 끝이다.

## 알고 시작할 것

- **"평생" 인 것은 요금이지 인스턴스가 아니다.** Oracle 은 7일 CPU·network
  사용률이 기준 아래인 Always Free 인스턴스를 idle 로 보고 **회수할 수 있다.**
  조용한 relay 는 딱 그 후보다. 이름(DNS)은 남지만 다시 만들 때까지 대문은
  죽는다. 그래서 **밖에서** 살아 있는지 보는 확인이 따로 필요하고, 다시 만드는
  절차를 적어 두어야 한다. 정책을 피하려고 가짜 부하를 돌리지는 않는다.
- **VPS 가 죽으면 밖에서 아무도 못 본다.** 랩 안(`bmlin`)은 그대로다.
- **기계 한 대를 돌봐야 한다.** 공짜라도 보안 갱신은 우리 몫이다.

## 막히면

관문에서 걸린 단계 번호와 그때 화면을 그대로 가져오면 된다. 8건이 "설치가
인증서 전에 멎는다" 부류였고 전부 고쳐 뒀지만, **이 저장소에서 한 번도 못
돌려 봤다** — 처음 실제로 도는 것이 그 VPS 다.
