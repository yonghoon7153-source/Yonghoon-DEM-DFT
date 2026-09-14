function d = differential(capacity, voltage, window, poly_order)
%DIFFERENTIAL  합성 대역품 — 필드 이름과 모양만 원본과 같게 만든 해석 함수.
%   pchip·sgolay 를 쓰지 않는다 (그 자리의 수치 일치는 이 테스트의 목표가
%   아니다 — `synth/README_SYNTH.md` 참고). 대신 window/poly_order 가 실제로
%   전달되는지 확인할 수 있게 결과에 섞어 넣는다.
    capacity = capacity(:); voltage = voltage(:);
    ok = isfinite(capacity) & isfinite(voltage);
    capacity = capacity(ok); voltage = voltage(ok);
    n = 500;
    k = window + 0.1 * poly_order;      % 인자가 도달했는지 결과로 확인

    c2 = linspace(min(capacity), max(capacity), n)';
    d.capacity_uniform2 = c2;
    d.voltage_uniform2  = 4.1 - 0.8 * c2;
    d.dvdq              = -0.8 + 0.3 * sin(k * c2);

    v1 = linspace(min(voltage), max(voltage), n)';
    d.voltage_uniform   = v1;
    d.capacity_uniform  = (v1 - min(v1)) / (max(v1) - min(v1));
    d.dqdv              = -1.25 + 0.4 * cos(k * v1);
end
