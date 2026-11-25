#!/usr/bin/env bash
# =============================================================================
# orca_mpi_env.sh — 단일노드 ORCA 를 MPI 전송층 고장에서 살리는 설정. **정본 한 벌.**
#
#   . tools/sdcp/orca_mpi_env.sh      # source 하면 OMPI_MCA_btl 이 걸린다
#   bash tools/sdcp/orca_mpi_env.sh --selftest
#
# 왜 있나 (실측 셋, 전부 2시간 이상씩 태웠다)
#   · 2026-09-05  gs3 이 **같은 오류로 두 번** 죽었다 (02:45 · 14:16, 둘 다 nprocs 8):
#         [btl_tcp.c:559] recv(23) failed: Connection reset by peer (104)  × 수십 줄
#         ORCA finished by error termination in LEANSCF
#     한 대에서 도는데 OpenMPI 가 TCP BTL 로 통신하다 끊긴 것이다. 화학이 아니라 전송층이다.
#   · 2026-09-06  n=6 doped 가 **같은 자리**에서 죽었다 (LEANSCF · mpirun -np 8).
#     SCF 는 수렴까지 갔는데 거기서 끝났다. `OMPI_MCA_btl` 은 안 걸려 있었다.
#     처방은 하루 전에 이미 알고 있었는데 **새 러너가 그걸 안 물려받았다** —
#     그래서 지식을 스크립트에 흩어 두지 않고 여기 한 벌로 모은다.
#
# ⛔⛔ 판본을 감지해서 골라야 한다 (2026-09-05 두 번째 실측)
#   공유메모리 BTL 이름이 판본마다 다르다: OpenMPI ≤4.x = `vader` · ≥5.x = `sm`.
#   처음에 `self,vader,sm` 을 넣고 "없는 쪽은 무시된다" 고 적었는데 **틀렸다.**
#   kgy(OpenMPI 4.1.6)에서 즉사했다:
#       help-mpi-btl-sm.txt / btl sm is dead
#       mca_bml_base_open() failed --> Returned "Not found" (-13)
#       *** An error occurred in MPI_Init
#   없는 컴포넌트를 목록에 넣으면 OpenMPI 는 **무시하지 않고** 열려다 실패하고,
#   그러면 BTL 이 하나도 안 남아 MPI_Init 이 죽는다.
#
# ⛔ 이 파일이 **못 하는 것**
#   · 속도를 올리지 않는다. **생존**을 위한 설정이고 결과값을 바꾸지 않는다.
#   · MPI 고장을 전부 막지 않는다 — TCP BTL 계열만 막는다. 메모리·디스크로 죽는 것은 그대로다.
#   · 판본을 못 읽으면 **아무것도 강제하지 않는다** (기본 동작 유지). fail-open 이지만
#     여기서는 그게 맞다 — 잘못된 BTL 을 강제하면 위처럼 MPI_Init 에서 즉사한다.
#   · ORCA 를 실행하지 않는다. `%pal` 을 쓰면 ORCA 는 **전체 경로**로 불러야 한다는 것도
#     여기 책임이 아니다 (부르는 쪽에서 `$(command -v orca)`).
#
# 손으로 지정: `ORCA_MPI_BTL=self,vader` · 끄기: `ORCA_MPI_BTL=` (빈 값)
#   ⚠ 옛 이름 `STAGEA_MPI_BTL` 도 계속 받는다 (run_orca_stage_a.sh 문서·receipt 에 남아 있다).
# =============================================================================

btl_for_ompi(){   # $1 = "4.1.6" 등 · → 공유메모리 BTL 목록 (모르면 빈 문자열)
  case "${1%%.*}" in
    ""|*[!0-9]*) echo "" ;;                # 판독 실패 → 강제하지 않는다
    1|2|3|4)     echo "self,vader" ;;
    *)           echo "self,sm" ;;         # 5.x 이상
  esac
}

orca_mpi_env_apply(){   # → MPI_BTL_NOTE 를 채우고 OMPI_MCA_btl 을 export
  local ver use
  ver=$(mpirun --version 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
  use=${ORCA_MPI_BTL-${STAGEA_MPI_BTL-$(btl_for_ompi "$ver")}}
  [ -n "$use" ] && export OMPI_MCA_btl="$use"
  MPI_BTL_NOTE="${use:-<unset>} (OpenMPI ${ver:-미상})"
  export MPI_BTL_NOTE
}

# ⛔⛔ `${BASH_SOURCE[0]}` = `$0` 인지를 **반드시** 같이 본다 — source 된 스크립트는
#   호출자의 위치인자를 그대로 물려받는다. 이 가드 없이 `bash run_orca_stage_a.sh --selftest`
#   를 돌리면 여기가 `$1 = --selftest` 를 자기 것으로 읽고 **exit 0 으로 끝내서**
#   러너의 selftest 가 통째로 안 돌았다 (2026-09-07, 이 파일을 뽑아내자마자 실측).
#   "시험이 사라지는 것" 은 시험이 실패하는 것보다 나쁘다 — 초록으로 보이니까.
if [ "${BASH_SOURCE[0]}" = "$0" ] && [ "${1:-}" = "--selftest" ]; then
  ok=0; bad=0
  chk(){ if [ "$1" = "1" ]; then echo "  ⭕ $2"; ok=$((ok+1)); else echo "  ⛔ $2"; bad=$((bad+1)); fi; }
  chk "$([ "$(btl_for_ompi 4.1.6)" = "self,vader" ] && echo 1 || echo 0)" "4.x → self,vader (gabia·kgy 실물)"
  chk "$([ "$(btl_for_ompi 3.1.4)" = "self,vader" ] && echo 1 || echo 0)" "3.x → self,vader"
  chk "$([ "$(btl_for_ompi 5.0.2)" = "self,sm"   ] && echo 1 || echo 0)" "5.x → self,sm"
  chk "$([ -z "$(btl_for_ompi '')"      ] && echo 1 || echo 0)" \
      "⛔음성: 판본을 못 읽으면 **아무것도 강제하지 않는다** (틀린 BTL 강제가 더 나쁘다)"
  chk "$([ -z "$(btl_for_ompi 'x.y.z')" ] && echo 1 || echo 0)" "⛔음성: 숫자가 아니어도 강제하지 않는다"
  case "$(btl_for_ompi 4.1.6)" in *sm*) _h=1 ;; *) _h=0 ;; esac
  chk "$([ "$_h" = 0 ] && echo 1 || echo 0)" \
      '⛔음성: 4.x 목록에 sm 을 **섞지 않는다** (없는 컴포넌트를 넣으면 MPI_Init 즉사 — kgy 실물)'
  case "$(btl_for_ompi 5.0.2)" in *vader*) _h=1 ;; *) _h=0 ;; esac
  chk "$([ "$_h" = 0 ] && echo 1 || echo 0)" "⛔음성: 5.x 목록에 vader 를 섞지 않는다"
  ( ORCA_MPI_BTL="" ; orca_mpi_env_apply
    [ "${OMPI_MCA_btl:-<none>}" = "<none>" ] || exit 1 ) \
    && chk 1 "빈 값으로 끌 수 있다 (ORCA_MPI_BTL=)" || chk 0 "빈 값으로 끌 수 있다 (ORCA_MPI_BTL=)"
  ( ORCA_MPI_BTL="self,vader" ; orca_mpi_env_apply
    [ "$OMPI_MCA_btl" = "self,vader" ] || exit 1 ) \
    && chk 1 "손으로 지정한 값이 판본 감지를 이긴다" || chk 0 "손으로 지정한 값이 판본 감지를 이긴다"
  ( STAGEA_MPI_BTL="self,sm" ; orca_mpi_env_apply
    [ "$OMPI_MCA_btl" = "self,sm" ] || exit 1 ) \
    && chk 1 "옛 이름 STAGEA_MPI_BTL 도 계속 받는다" || chk 0 "옛 이름 STAGEA_MPI_BTL 도 계속 받는다"
  echo "  selftest: ⭕ $ok · ⛔ $bad"; [ "$bad" = 0 ] || exit 1; exit 0
fi
