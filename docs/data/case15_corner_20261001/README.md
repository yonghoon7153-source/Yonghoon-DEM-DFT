# case15 (corner 팔 · FAM §12-3) DEM 원자료 (2026-10-01 첨부)

FAM 사전등록 `docs/reviews/fam_platen_prereg_20260812.md` §12-3 corner 팔 (`input_1mAh_100_15`) 의 t_DEM · f 를 원자료에서 재기 위해
1저자가 10-01 이 세션에 첨부한 다섯 파일.  **바이트 그대로** 보관한다 (덱 · 메시는 그대로 · 덤프 둘은 `gzip -9 -n`).
⚠ 이 폴더는 첨부된 바이트의 해시와 덱 내용만 증명한다 — 파일이 `input_1mAh_100_15` 런의 산출물이라는 것은 1저자 진술이다.

```
sha256 (원본)                                                      크기           파일
172953c78a07c4da16bd6b2bc6b02111c144f5ba257f800349193cc92de4dc60  6,579 B        input_case15.liggghts        (여기 있음)
2868f0898a9056375c74ea24f2be1d46cb5f06f2411b01c21fa77c96836c053b  349 B          mesh_v4_1710000.stl          (여기 있음)
f40f69eccd793ca96c7ba823914180e879b2c14c1c9a57f4c15af3393fce608f  8,821,311 B    atom_v4_1710000.liggghts     (atom_v4_1710000.liggghts.gz)
180140701ef4dfd34bbda6c236837d267502d35a0372824c8720d7d8731b1b4d  49,986,128 B   contact_v4_1710000.liggghts  (contact_v4_1710000.liggghts.gz · 첨부는 zip)
5944f830764ed0f9d9a588c7e5b47341b152b6310aa49715529f04ae6a174014  18,153,219 B   contact_v4_1710000.zip       (첨부 zip 자체 · 안에 파일 하나)
```

```
gunzip -c atom_v4_1710000.liggghts.gz | sha256sum      # f40f69ec…608f
gunzip -c contact_v4_1710000.liggghts.gz | sha256sum   # 18014070…1b4d
```

## 덱 · 덤프에서 읽은 사실 (해석 없음)

| 항목 | 값 | 근거 |
|---|---|---|
| 덱 끝 문구 | *"Case15: AM:SE=85:15, P:S=10:0, 1mAh/cm2"* | 덱 마지막 print |
| 반지름 (sim) | r_AM_P 6.0e-3 · r_AM_S 2.0e-3 · r_SE 0.5e-3 | 덱 20–22 행 |
| 목표 | `target_press 0.30` (덱 표기 그대로 · 누름 루프가 `current_press ≥ target_press` 에서 멈춘다) | 덱 19 · 149–152 행 |
| 누름 속도 | `move/mesh linear 0 0 -0.01` · 5000 step 루프 | 덱 145–152 행 |
| 단계 | PHASE 2 안정 (200,000 step) → PHASE 3 누름 (루프) → `unfix move_press` → PHASE 4 완화 (판 고정 · 100,000 step) | 덱 128–166 행 |
| contact 덤프 | PHASE 4 에서만 정의 (`dump dmp_contact … 10000`) ⇒ **step 1,710,000 ∈ PHASE 4 (판 고정 완화)** | 덱 160 행 |
| 덤프 step | 1,710,000 (atom · contact · mesh 같은 step) | 세 파일 머리 |
| 상자 | x · y = [0, 0.1) 주기 (`pp pp ff`) · z [−0.01, 1] | atom 머리 |
| 원자 수 · 접촉 행 | 65,970 · 182,995 | atom · contact 머리 |
| 판 메시 z | 0.0191455 (평평한 면) | mesh_v4_1710000.stl |

- ⬜ **마지막 덤프인가** (PHASE 4 100,000 step 의 끝인가 중간인가) 와 **원본 위치** 는 1저자 확인 대기 — 같은 폴더의 덤프 목록으로 정해진다.
- ⬜ corner 의 t_DEM · f 추출 = §12-3 계약대로 (다음 커밋).  파일명의 `v4` 는 첨부 때 붙은 이름 (덱의 덤프 이름은 `post_case15/{atom,contact,mesh}_*`).
