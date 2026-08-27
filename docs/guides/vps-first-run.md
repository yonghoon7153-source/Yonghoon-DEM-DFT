---
title: vps first run
created: 2026-08-27
updated: 2026-08-27
type: guide
tags: [tooling, network, vps, ssh, nginx]
sources: [docs/adr/0034-our-own-vps-in-front.md, docs/reviews/2026-08-27-codex-vps-result.md]
confidence: medium
explored: false
verificationStatus: unverified
---

# 우리 VPS 한 대 세우기 — 버릴 수 있는 것으로 먼저

`bml.bmlwork.kr` 을 늘 열려 있는 주소로 만드는 절차 (ADR 0034).
끝나면 이것들이 통째로 없어진다:

- 열 때마다 바뀌는 주소 → **안 바뀐다**
- `bmlonly` 와 IP 세 개 → 받는 쪽은 `bmlout https://bml.bmlwork.kr` **한 번**
- 주소를 카톡으로 다시 보내기 → 없다

## 읽기 전에 — 왜 임시 VPS 부터인가

`tools/vps-setup.sh` 는 **한 줄도 실제로 돌려 본 적이 없다.** 저장소를 고치는
컨테이너에 nginx·sshd·certbot 이 없어서다. Codex 적대 리뷰가 22건을 냈고 그중
8건이 "지금 만들면 설치가 인증서 앞에서 멎는다" 부류였다 — 고쳤지만, 고친 것을
확인한 방법은 **글자 세기**다 ([회답](../reviews/2026-08-27-codex-vps-reply.md)
의 표가 그것을 갈라 적어 두었다).

그래서 **버려도 되는 인스턴스에서 먼저 통과시킨다.** 여기서 뭔가 터지면 그
기계를 지우고 다시 만들면 되고, 실제 이름(`bml.bmlwork.kr`)은 아직 아무 데도
안 걸려 있다.

## 0. 만들기 (돈 안 나가는 쪽)

Oracle Cloud **Always Free** 의 AMD micro (1 GB) 로 충분하다. 이 일은
`ssh -R` 로 넘어온 TCP 를 nginx 가 받아 넘기는 것뿐이다.

- 이미지: **Ubuntu 22.04 또는 24.04**
- **public subnet** 에 두고 공인 IP 를 받는다
- SSH 키는 새로 만들어도 되고 쓰던 것을 넣어도 된다 (이건 관리용이다 —
  터널용 키는 나중에 따로 만든다)

> **"평생" 인 것은 요금이지 이 인스턴스가 아니다.** Oracle 은 7일 CPU·network
> 사용률이 기준 아래인 Always Free 인스턴스를 idle 로 보고 **회수할 수 있다.**
> 조용한 relay 는 그 후보가 되기 좋다. 이름(DNS)은 남지만 다시 만들 때까지
> 대문은 죽는다. 가짜 부하를 돌려 정책을 피하지는 않는다 — 대신 밖에서 죽은
> 것을 알 수 있게 해 두고, 다시 만드는 절차를 이 문서로 남긴다.

임시 VPS 라면 도메인이 필요하다 (인증서 때문에). `bmlwork.kr` 의 **다른**
이름을 하나 쓰면 된다 — 예를 들어 `test.bmlwork.kr` 을 임시 기계의 IP 로.
그러면 실제 이름은 끝까지 안 건드린다.

## 1. `--check` — 아무것도 바꾸기 전에

```bash
sudo bash vps-setup.sh --check test.bmlwork.kr
```

**Oracle 은 방화벽이 두 층이다.** 한쪽만 열면 조용히 timeout 나고, 그 timeout
은 certbot 실패로 보이지 방화벽 문제로 보이지 않는다.

1. **VCN → Security List 또는 NSG**: ingress 두 개.
   source `0.0.0.0/0` · TCP · **80** 과 **443**.
   **5003 은 열지 않는다** — `GatewayPorts` 가 잘못돼도 이 층이 막아야 한다.
2. **인스턴스 안의 iptables**: Oracle Ubuntu 이미지는 기본으로 막는다.
   기존 규칙을 지우지 말고 reject **앞에** 끼운다:
   ```bash
   sudo iptables -L INPUT --line-numbers      # REJECT 줄의 번호를 본다
   sudo iptables -I INPUT <그 번호> -p tcp --dport 80  -j ACCEPT
   sudo iptables -I INPUT <그 번호> -p tcp --dport 443 -j ACCEPT
   sudo netfilter-persistent save
   ```
   줄 번호는 이미지마다 다르다. 인터넷 예제의 "6번 줄" 을 그대로 베끼지 않는다.
   **UFW 로 고치지 않는다** — Oracle 이 이 이미지에서 권하지 않는다.

DNS 도 이때 맞춘다: A 레코드가 **이미** 이 기계를 가리켜야 한다
(Cloudflare 라면 **회색 구름** — 주황 구름은 올리는 파일을 100 MB 로 막는다).

## 2. 설치

```bash
sudo bash vps-setup.sh test.bmlwork.kr you@hanyang.ac.kr
```

끝까지 가야 한다 (certbot 포함). 중간에 멎으면 그 메시지가 곧 다음 할 일이다.
이미 설정이 있으면 **덮지 않고 멈춘다** — 정말 바꾸려면 `BML_REPLACE=1`.

## 3. 세운 것이 진짜 섰나 — 기계가 센다

```bash
sudo bash vps-setup.sh --verify test.bmlwork.kr
```

사람이 열 줄을 손으로 치면 **빠뜨린 줄과 통과한 줄이 화면에서 같아 보인다.**
그래서 기계가 센다. 여기서 보는 것:

| 무엇 | 왜 |
|---|---|
| `nginx -t` | 지금 도는 설정과 디스크의 설정이 갈라져 있으면 재부팅에서 진다 |
| `is-enabled` · `is-active` | 지금 떠 있는 것과 다음에도 뜨는 것은 다르다 |
| `sshd -T` 의 실효 `gatewayports no` | 파일 한 곳만 봐서는 모른다 — include·Match 가 값을 뒤집는다 |
| `5003` 리스너가 `127.0.0.1` **하나** | `0.0.0.0`·`[::]` 은 nginx 를 우회하는 구멍, `[::1]` 만도 실패 (공개 주소가 502) |
| 인증서 + 갱신 타이머 | 90일 뒤에 조용히 죽는 것을 막는다 |
| `nginx -T` 에 `520m` · `request_buffering off` · `75s` · `listen 443` | certbot 이 443 블록을 새로 쓰므로, **실효 설정**에 실렸는지는 파일 하나로 모른다 |
| 전용 계정에 셸이 없고 키에 `permitlisten` | 키가 새도 forwarding 하나로 끝나야 한다 |

**`?` 는 통과가 아니다.** "못 쟀다" 이고, 그때는 왜 못 쟀는지부터 본다.

## 4. 랩 PC 의 키를 올린다

설치가 끝나면 화면이 정확한 줄을 적어 준다. 요점은 **제한을 그대로 붙이는
것**이다:

```
restrict,port-forwarding,permitlisten="127.0.0.1:5003" ssh-ed25519 AAAA... 랩PC
```

`restrict` 가 셸·PTY·agent·X11 을 다 끄고, `permitlisten` 이 열 수 있는
포트를 하나로 묶는다. 이 줄에서 앞부분을 빼면 그 키는 **VPS 에 로그인할 수
있는 키**가 된다.

## 5. 밖에서 5003 이 막혔나

```bash
nc -vz <VPS 의 IP> 5003        # 실패해야 한다
```

**이 기계 안에서는 알 수 없는 검사다.** `--verify` 가 마지막에 이것을 남겨
두는 이유가 그것이다. 성공하면 두 번째 층(VCN)이 5003 을 열어 둔 것이다 —
그러면 nginx 도 TLS 도 우회된다.

## 6. 랩 PC 에서 열기

```bash
bml share vps bml-tunnel@<VPS 의 IP 또는 이름>
bml share domain test.bmlwork.kr
bml share
```

`✓ 열렸습니다 → https://test.bmlwork.kr (우리 도메인 · 이제 안 바뀝니다)` 여야
한다.

**200 만으로는 모자란다.** `bml` 이 `/api/health` 의 `instance` 를 로컬 것과
맞춰 본다 (Codex #8) — 손으로도 한 번:

```bash
curl -s https://test.bmlwork.kr/api/health   | grep -o '"instance":"[^"]*"'
curl -s http://127.0.0.1:5003/api/health     | grep -o '"instance":"[^"]*"'
```

같아야 한다. 다르면 그 주소는 **다른 워크벤치**다 (DNS 가 옛 기계를 가리키거나,
저쪽 5003 을 옛 터널이 잡고 있다).

## 7. 랩 PC 를 재우거나 랜을 뽑는다

뽑았다 꽂고 **90초 안에** 저절로 돌아와야 한다.

- 랩 PC 가 깨어 있는데 망만 끊긴 경우: 랩 쪽 `ServerAliveInterval=30` ·
  `ServerAliveCountMax=3` 이 약 90초 뒤 ssh 를 끝내고 감독자가 다시 붙는다.
- **PC 자체가 잠들면 랩 쪽 타이머도 멈춘다.** 그때는 VPS 쪽
  `ClientAliveInterval 30` · `ClientAliveCountMax 3` 이 옛 listener 를
  정리해 준다 — 그것이 없으면 깨어난 ssh 가 "포트가 이미 잡혔다" 로 계속 죽는다.

## 8. `bml stop` 이 정말 닫나

```bash
bml stop                                   # 랩 PC
ss -H -ltn 'sport = :5003'                 # VPS — 사라져야 한다
```

랩 PC 에 ssh 도 감독자도 안 남아야 한다. 남으면 5초마다 다시 붙으므로
**닫았다고 말한 뒤에 고정 주소가 조용히 다시 열린다.**

## 9. VPS 재부팅

```bash
sudo reboot
# 올라온 뒤
sudo bash vps-setup.sh --verify test.bmlwork.kr
```

대문이 저절로 서야 한다. 그 다음 랩 PC 에서 `bml share` 한 번.

## 10. 인증서 갱신

```bash
sudo certbot renew --dry-run
```

이게 실패하면 **90일 뒤에 조용히 죽는다** — 그때는 아무도 왜인지 모른다.

---

## 열 단계를 다 통과하면

그때 실제 이름을 건다: `bml.bmlwork.kr` 의 A 레코드를 이 기계로 (회색 구름),
`sudo bash vps-setup.sh bml.bmlwork.kr <메일>` 을 다시 돌리고,
랩 PC 에서 `bml share domain bml.bmlwork.kr`.

그리고 임시 이름(`test.bmlwork.kr`)의 A 레코드는 지운다 — 남겨 두면 다음에
누가 그 주소를 열어 보고 우리 데이터를 본다.

## 안 되면

- **certbot 이 멎는다** → 1번(두 층)으로 돌아간다. 80 이 밖에서 안 열리면
  HTTP-01 이 못 온다.
- **공개 주소가 502** → 저쪽 리스너를 본다 (`ss -H -ltn 'sport = :5003'`).
  `[::1]` 만 잡혀 있으면 nginx 가 보는 `127.0.0.1` 은 비어 있다.
- **`bml share` 가 "우리 서버가 아닙니다"** → DNS 가 아직 옛 기계이거나 저쪽
  5003 을 옛 터널이 잡고 있다. 화면이 셋 중 무엇인지 적어 준다.
- **아무것도 안 되고 이유를 모르겠다** → 이 길을 접어도 된다.
  localhost.run 갈래와 Cloudflare 갈래를 지우지 않았다 (ADR 0034 의 '대가').
  `bml share now` 로 랜덤 주소 한 번이면 오늘 할 일은 된다.

## 함께 보기

- [[bml-command]] — `bml share` · `bml share vps` · `bmlout` 이 각각 무엇인지
- [[central-server]] — 한 대를 중추 서버로 두는 이유와 백업
