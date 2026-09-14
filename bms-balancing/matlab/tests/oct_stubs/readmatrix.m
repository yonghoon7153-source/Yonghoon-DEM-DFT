function M = readmatrix(f, varargin)
%READMATRIX  **Octave 전용 테스트 대역품** — CSV 만, 'Range','A<n>' 만 지원.
%   MATLAB 내장함수를 흉내 내는 것이 아니라, 합성 CSV 를 읽어 dd_eval.m 의
%   배관(컬럼 인덱싱·NaN 제거)을 돌려 보기 위한 최소 구현이다.
    skip = 0;
    for k = 1:2:numel(varargin)
        if strcmpi(varargin{k}, 'Range')
            r = varargin{k+1};
            skip = str2double(r(2:end)) - 1;    % 'A3' -> 2줄 건너뜀
        end
    end
    M = dlmread(f, ',', skip, 0);
end
