function T = readtable(f)
%READTABLE  **Octave 전용 테스트 대역품** — 헤더 한 줄짜리 CSV 를 struct 로.
%   `T.colname` 접근만 흉내 낸다 (dd_eval.m 이 쓰는 형태).
    fid = fopen(f, 'r');
    hdr = strtrim(fgetl(fid));
    fclose(fid);
    names = strsplit(hdr, ',');
    M = dlmread(f, ',', 1, 0);
    T = struct();
    for k = 1:numel(names)
        T.(strtrim(names{k})) = M(:, k);
    end
end
