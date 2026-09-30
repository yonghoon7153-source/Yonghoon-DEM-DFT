# 수신 검토기 작업 기록

받은 코드와 시험은 실행하지 않았다. 수신 측 자체 CSV 재계산기의 첫 실행은 수치 검사를 통과한 뒤, 선택 진단인 native Tfail 집계에서 첫 step의 빈 칸을 일반 step과 같은 열로 취급해 ValueError로 종료했다(도구 chunk dfe452). 로그 헤더와 0번 행을 대조한 뒤, 1번 이후 12열 행에만 Tfail/NLfail을 집계하고 첫 Tfail은 NOT_PRINTED로 두었다. 이 수정은 받은 파일이나 COMSOL 계산의 수정·재실행이 아니다.

초기 JSON 요약 조회에서도 PRESERVATION_BEFORE가 dict가 아니라 list인 점을 놓쳐 AttributeError로 종료했다(chunk960a30). 읽기 전용 표시 코드의 오류이며 원본이나 생산 판정에 영향이 없다.
