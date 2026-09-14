function t = contains(s, pat)
%CONTAINS  MATLAB R2016b+ 내장함수의 **Octave 전용** 대역품.
%
%   ⚠ 이 폴더(`tests/oct_stubs/`)는 **테스트에서만** 경로에 넣는다.
%     MATLAB 에는 `contains` 가 원래 있으므로 사용자 기계에는 절대 복사하지
%     않는다 (복사하면 내장함수를 가린다). `dd_shims/` 와 목적이 다르다:
%     dd_shims 는 사용자 기계에서 쓰라고 만든 것이고, 여기는 이 컨테이너에서
%     Octave 로 dd_eval.m 을 돌려 보려고 만든 것이다.
    t = ~isempty(strfind(s, pat));
end
