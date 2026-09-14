function [pks, locs] = findpeaks(x, varargin)
%FINDPEAKS  국소 최대점과 그 prominence 필터 — **기본 MATLAB 만으로 쓴 대체품**.
%
%   ⚠ MathWorks 의 Signal Processing Toolbox 함수가 아니다.
%     `dd_shims/` 를 경로에 넣었을 때만 쓰인다 (`addpath(...,'-end')`).
%     툴박스를 설치하면 진짜 함수가 이기고 이 파일은 안 쓰인다.
%
%   지원 범위 — 규진팀 코드가 쓰는 형태 하나뿐이다:
%       [~, locs] = findpeaks(dq, 'MinPeakProminence', thresh)
%   그 밖의 옵션('MinPeakHeight' 등)은 받으면 에러를 낸다. 조용히 무시하면
%   다른 답을 내고도 모르기 때문이다.
%
%   ── 정의 (MATLAB 문서·scipy 둘 다 같은 표준 정의) ──
%   어떤 봉우리의 prominence:
%     1. 그 봉우리 높이에서 좌·우로 수평선을 긋고, **더 높은 값**을 만나거나
%        신호 끝에 닿을 때까지 간다.
%     2. 그 두 구간 각각의 **최솟값**을 찾는다 (좌 base, 우 base).
%     3. prominence = 봉우리 높이 − max(좌 base, 우 base)
%
%   ── 평탄한 꼭대기 (plateau) ──
%   `scipy.signal.find_peaks` 와 같은 규약을 쓴다: 같은 값이 이어지는 꼭대기는
%   **가운데 인덱스** 하나를 봉우리로 삼는다. (MathWorks 구현은 평탄 꼭대기를
%   봉우리로 안 볼 수 있다 — 그 자리가 이 대체품과 진짜 함수의 알려진 차이다.)
%   우리 Python 포팅이 scipy 를 쓰므로 대조를 위해 scipy 쪽에 맞췄다.

    x = x(:);
    n = numel(x);

    % ── 옵션 ──
    min_prom = -Inf;
    k = 1;
    while k <= numel(varargin)
        name = varargin{k};
        if ~(ischar(name) || isstring(name))
            error('findpeaks(shim): 옵션 이름이 문자열이 아니다');
        end
        if k + 1 > numel(varargin)
            error('findpeaks(shim): 옵션 ''%s'' 에 값이 없다', char(name));
        end
        switch lower(char(name))
            case 'minpeakprominence'
                min_prom = double(varargin{k+1});
            otherwise
                error(['findpeaks(shim): 옵션 ''%s'' 은 지원하지 않는다. ' ...
                       '이 대체품은 규진팀 코드가 쓰는 ''MinPeakProminence'' ' ...
                       '하나만 구현했다 — 조용히 무시하면 다른 답을 낸다.'], ...
                       char(name));
        end
        k = k + 2;
    end

    pks = zeros(0, 1);
    locs = zeros(0, 1);
    if n < 3
        return
    end

    % ── ① 국소 최대점 (평탄 꼭대기는 가운데) ──
    cand = zeros(0, 1);
    i = 2;
    while i <= n - 1
        if x(i - 1) < x(i)
            j = i;                       % 평탄 구간의 오른쪽 끝을 찾는다
            while j < n && x(j + 1) == x(i)
                j = j + 1;
            end
            if j < n && x(j + 1) < x(i)
                cand(end+1, 1) = floor((i + j) / 2); %#ok<AGROW>
            end
            i = j + 1;
        else
            i = i + 1;
        end
    end
    if isempty(cand)
        return
    end

    % ── ② prominence ──
    prom = zeros(numel(cand), 1);
    for m = 1:numel(cand)
        p = cand(m);
        h = x(p);

        j = p;                            % 왼쪽: 더 높은 값을 만날 때까지
        left_min = h;
        while j >= 1 && x(j) <= h
            if x(j) < left_min, left_min = x(j); end
            j = j - 1;
        end

        j = p;                            % 오른쪽
        right_min = h;
        while j <= n && x(j) <= h
            if x(j) < right_min, right_min = x(j); end
            j = j + 1;
        end

        prom(m) = h - max(left_min, right_min);
    end

    keep = prom >= min_prom;
    locs = cand(keep);
    pks  = x(locs);
end
