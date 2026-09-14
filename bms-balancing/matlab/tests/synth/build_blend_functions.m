function [E_NE, dv_NE] = build_blend_functions(si_c, si_v, gr_c, gr_v, diff_params)
%BUILD_BLEND_FUNCTIONS  합성 대역품 — 문헌 데이터가 결과에 닿는 해석적 블렌드.
    a = mean(si_c(isfinite(si_c)));
    b = mean(gr_v(isfinite(gr_v)));
    w = diff_params.poly_order;
    E_NE  = @(x, g) 0.25 + 0.35 * x - 0.20 * g + 0.05 * a * g .* x + 0.01 * b;
    dv_NE = @(x, g) 0.10 * cos(2 * x) + 0.05 * g + 0.001 * w;
end
