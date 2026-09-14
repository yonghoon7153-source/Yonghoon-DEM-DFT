function r = electrode_ocv(dirpath, filename, diff_params)
%ELECTRODE_OCV  합성 대역품 — 반쪽전지 파일을 실제로 읽어(경로 배관 확인)
%   해석적 함수 핸들을 돌려준다.
    f = fullfile(dirpath, filename);
    if exist(f, 'file') ~= 2
        error('electrode_ocv(synth): 파일이 없다: %s', f);
    end
    T = readtable(f);
    s = mean(T.PE_capacity(isfinite(T.PE_capacity)));   % 파일 내용이 결과에 닿게
    w = diff_params.window;

    r.E_PE  = @(x) 3.90 - 0.70 * x + 0.02 * s * sin(2 * x);
    r.E_NE  = @(x) 0.25 + 0.35 * x;
    r.dv_PE = @(x) -0.70 + 0.05 * cos(w * x / 10);
    r.dv_NE = @(x) 0.10 - 0.02 * x;
end
