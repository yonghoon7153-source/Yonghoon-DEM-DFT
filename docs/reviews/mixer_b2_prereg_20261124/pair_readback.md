# B2 짝 방향의 로컬 산술

이 판독기는 C 반환의 검산·원 덤프 준비가 끝난 뒤에만 사용한다. 새 계산·제출은 없다. 이 등록 시점에는 C 결과를 읽은 건수가 0건이다.

1. 1저자에게 369734 반환물과 검증된 SHA256SUMS를 받는다. 승인된 C 배포 핀 92b185b70c12의 제출 영수증, Slurm 정상 종료, 러너 0, 234개 파일명, 현장 종료 시점 W9, 보고·전체 TAR 바이트, 원래 B2-C 덱과 실행 당시 seed를 확인한다. U 368758의 정상 반환은 docs/reviews/mixer_b2_flow_20261124/README.md §1에서 확인했다. C의 완전성과 W9를 확인할 수 없으면 짝 판독은 대기한다.
2. B2-U에 쓴 9파일 관측기와 동일한 E0 기준 덤프를 쓴다. 첫 번째 명령은 검증된 C 원 덤프에서 고정 관측기의 **전체 표준 출력**을 새 로컬 파일에 쓴다. 두 번째 명령은 그 표준 출력, 기존 U 관측 파일, 검증한 C의 원 return.json을 사용한다. 아래 변수에는 각각 검증한 현지 파일·폴더를 지정한다.

```bash
(
  set -eu -o noclobber
  py="$HOME/Yonghoon-DEM-DFT/venv/bin/python"
  "$py" -I -X utf8 -B "$FROZEN/scripts/mixer_precal_observe.py" \
    --case PRECAL_R1_B2_C --run "$C_NATIVE" --reference "$E0" > "$C_OBSERVER"
  "$py" -I -X utf8 -B "$READER/preregistered_pair.py" \
    "$U_OBSERVER" "$C_OBSERVER" "$C_RETURN/return.json" "$NEW_PAIR_JSON"
)
```

FROZEN은 B2-U 계산에 쓴 관측기 묶음, C_NATIVE는 정상 반환·원 덱·원 덤프·종료 로그를 갖춘 C 작업 사본, E0는 그때의 균일 정착 기준 폴더다. U_OBSERVER는 B2-U 원 관측 JSON으로 SHA256은 128d0c0dc67ead931dbc4a68ccf5c1508e7d02bcacc1db3f921010ba72dee2c2이다. C_RETURN은 검산한 C 반환 폴더다. C_OBSERVER, NEW_PAIR_JSON은 존재하지 않는 파일 경로, READER는 이 판독기가 있는 폴더다. 관측기의 의존 환경은 B2-U와 동일한 WSL Python·NumPy·SciPy를 쓴다.

100개 native 프레임 각각에서 실제 SE 개수로 순간 분율의 정수 분자를 복원한다. 100개가 완비되지 않거나 순서·시드·모듈·E0·원 덱·바이트 표지가 어긋나면 종료한다. 각 팔의 평균에 같은 프레임 가중치를 주고 정확한 유리수로 C−U를 산출한다. 결과는 %p 및 두 엄격 부등식의 참·거짓으로 기록한다. 0과 반대 부호는 둘 다 해당 방향 불일치다. 군집은 관측기 원 정의인 크기 2 이상, AM 접촉은 두 AM 종류의 합집합이다. C−U의 이 산술은 한 시드의 방향 비교이며 좌표 정밀도 등 다른 불확도는 기존 관측기의 결과를 따로 병기한다. W9의 진위·원본 보관 이력은 첫 단계의 자료로 별도 확인한다.
