function [xu, ym] = averageDuplicates(x, y)
%AVERAGEDUPLICATES  합성 대역품 — model.py 의 average_duplicates 와 같은 규약.
%   같은 x 를 하나로 접고 y 는 평균. **정렬된** unique 를 쓴다.
    x = x(:); y = y(:);
    [xu, ~, ic] = unique(x);
    ysum = accumarray(ic, y);
    ycnt = accumarray(ic, ones(size(y)));
    ym = ysum ./ ycnt;
end
