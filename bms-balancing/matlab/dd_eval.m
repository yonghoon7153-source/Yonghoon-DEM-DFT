function dd_eval(varargin)
%DD_EVAL  **적합 없이** 목적함수만 평가한다 — 툴박스 없는 기계용 포팅 대조.
%
%   왜 이것이 필요한가
%   ------------------
%   `dd_verify('dump')` 는 `fmincon`+`MultiStart` 가 있어야 돈다. 툴박스가
%   없으면 적합을 못 한다. 그런데 **포팅 대조에 정말 필요한 것은 적합이
%   아니라 모델이다.** 같은 파라미터 p 에서 MATLAB 과 Python 이 같은
%   RMSE 를 내는지가 핵심이고, 그건 최적화기 없이 잴 수 있다.
%
%   이 파일이 쓰는 것: `electrode_ocv` · `differential` ·
%   `build_blend_functions` (전부 규진팀 원본) + `dd_shims/` 의 대체 함수 셋
%   (`sgolayfilt` · `quantile` · `findpeaks`). 최적화기는 안 쓴다.
%
%   ⚠ 단 하나 예외: dQ/dV 두 열(`rmse_dqdv`·`rmse_dqdv_w`)이 쓰는
%     `compute_dqdv_rmse_blend`·`build_peak_weights_local` 은 그들
%     `electrode_balancing_blend.m` 의 **로컬 함수**라 밖에서 못 부른다.
%     그 둘만 아래 `local_rmse_dqdv`·`local_peak_weights` 로 **옮겨 적었다**.
%     그러므로 그 두 열의 일치는 「그들 코드 ↔ 우리 포팅」이 아니라
%     「우리 전사 ↔ 우리 포팅」이다. 자세한 것은 그 함수 머리말.
%
%   ⚠ `dd_shims/` 는 MathWorks 구현이 아니다. 그러므로 여기서 나온 값은
%     "MATLAB 의 답" 이 아니라 **"규진팀 모델 + 우리 대체 함수"** 의 답이다.
%     Python 포팅도 같은 정의를 쓰므로, 셋이 맞으면 세 구현이 일치하는 것이고
%     갈리면 그 자리가 발견이다.
%
% 사용법
%   addpath('dd_shims','-end')   % ← '-end' 로. 아래 이유를 볼 것
%   dd_eval()                    % 기본: pristine · GITT · Si=Li · w_dqdv=0
%   dd_eval('State','300_0009','SiSource','Kunz')
%
% 옵션
%   'HalfCellDir'  기본 'data/half_cell/GITT/'
%   'SiSource'     기본 'Li'
%   'State'        기본 'pristine'
%   'WDqdv'        기본 0        (열 계산에는 안 쓴다 — 앞머리에만 적힌다.
%                                 rmse 네 열은 항상 다 계산한다)
%   'PeakWeight'   기본 7        그들 fit_params.peak_weight
%   'SigmaRatio'   기본 0.03     그들 fit_params.sigma_ratio
%   'NModel'       기본 500      그들 x_model 격자점 수
%   'P'            평가할 파라미터 행렬 (n x 5). 비우면 아래 기본 격자
%   'Out'          CSV 경로
%
% 산출 CSV
%   앞머리에 `# 이름,값` 으로 **이분 앵커 16개**를 적고, 그 뒤에 파라미터
%   행이 온다. 갈렸을 때 어느 단계가 범인인지 좁히는 값들이라 화면뿐 아니라
%   파일에도 남긴다. 앵커 앞에 `# printed_format,%.17g` — rmse 열의 출력
%   형식 **선언**이 온다 (Codex R3-06: 비교기가 값의 길이로 정밀도를 추정하지
%   않게). 이 줄이 없는 옛 CSV 는 비교기가 "추정" 이라고 말한다.
%     c_cell · dv_lo/hi · dv_n · dq_lo/hi           — 적재와 분위수 창
%     dq_n · n_peaks · w_peak_sum · w_peak_max      — dQ/dV 창과 피크 가중
%     dq_nuniq_p1 · dq_nin_p1                       — 첫 행 p 에서 조용히
%                                                     버려진 점 수 (아래 참고)
%     E_PE(0.5) · E_NE(0.5,0.25) · dv_PE(0.5) · dv_NE(0.5,0.25)  — 곡선
%
%   그 CSV 하나를 Python 쪽에 그대로 먹이면 대조가 끝난다:
%       python -m bms_balancing.verify eval --state pristine --si-source Li \
%              --compare dd_eval_pristine_Li.csv
%   ⚠ 기본 파라미터 격자를 여기서 고치면 `verify.py` 의 `DD_EVAL_P` 도 같이
%     고쳐야 한다. 한쪽만 고치면 대조가 조용히 어긋난다.

    p = inputParser;
    p.addParameter('HalfCellDir', 'data/half_cell/GITT/');
    p.addParameter('SiSource', 'Li');
    p.addParameter('State', 'pristine');
    p.addParameter('WDqdv', 0);
    p.addParameter('P', []);
    p.addParameter('Out', '');
    p.addParameter('PeakWeight', 7);      % 그들 fit_params.peak_weight
    p.addParameter('SigmaRatio', 0.03);   % 그들 fit_params.sigma_ratio
    p.addParameter('NModel', 500);        % 그들 x_model 격자점 수
    p.parse(varargin{:});
    o = p.Results;

    if isempty(which('sgolayfilt'))
        error(['dd_eval: sgolayfilt 가 없다 — ' ...
               '`addpath(''dd_shims'',''-end'')` 를 먼저 하라']);
    end
    % ── 어느 구현이 잡혔는지 기록한다 (provenance) ──
    %   `-end` 로 올리면 MATLAB 의 진짜 함수가 이기고, 없는 것만 shim 으로
    %   메워진다. 그냥 `addpath('dd_shims')` 는 앞에 붙어서 **있는 툴박스
    %   함수까지 가린다** — 2026-09-10 실측: 이 기계에 진짜 quantile 이 있다.
    impl = @(f) local_impl_tag(f);
    if isempty(which('findpeaks'))
        error(['dd_eval: findpeaks 가 없다 — `addpath(''dd_shims'',''-end'')` ' ...
               '를 먼저 하라 (dQ/dV 열을 쓰려면 필요하다)']);
    end

    diff_params = struct('window', 11, 'poly_order', 3);

    % ── 그들 코드로 곡선을 만든다 ──
    hc = local_halfcell_name(o.HalfCellDir, o.State);
    ro = electrode_ocv(o.HalfCellDir, hc, diff_params);
    lit = local_load_lit(o.SiSource);
    [E_NE, dv_NE] = build_blend_functions(lit.Si_capacity, lit.Si_voltage, ...
                                          lit.Gr_capacity, lit.Gr_voltage, diff_params);

    % ── 풀셀 (electrode_balancing_blend.m 과 같은 전처리) ──
    [cap, vol] = local_fullcell(o.State);
    [cap, vol] = averageDuplicates(cap, vol);
    c_cell = cap(end);
    if vol(1) < vol(end)
        cap = cap / c_cell;
    else
        cap = 1 - cap / c_cell;
    end

    d = differential(cap, vol, diff_params.window, diff_params.poly_order);
    lo = quantile(d.capacity_uniform2, 0.15);
    hi = quantile(d.capacity_uniform2, 0.85);
    idx = (d.capacity_uniform2 >= lo) & (d.capacity_uniform2 <= hi);
    cap_dv = d.capacity_uniform2(idx);
    dv_dat = d.dvdq(idx);

    vlo = quantile(d.voltage_uniform, 0.05);
    vhi = quantile(d.voltage_uniform, 0.95);

    % ── dQ/dV 창 + 피크 가중 ──
    mv = (d.voltage_uniform >= vlo) & (d.voltage_uniform <= vhi);
    vol_dq_fit  = d.voltage_uniform(mv);
    dq_fit_data = d.dqdv(mv);
    [w_peak, pk_locs] = local_peak_weights(vol_dq_fit, dq_fit_data, ...
                                           o.PeakWeight, o.SigmaRatio);
    x_model = linspace(0, 1, o.NModel)';
    Ecell = @(q, x) ro.E_PE((x - q(2)) / q(1)) - E_NE((x - q(4)) / q(3), q(5));

    % ── 평가할 파라미터 ──
    P = o.P;
    if isempty(P)
        % 그들이 보고한 값(pristine·GITT·Li)과 그 주변, 그리고 γ 격자
        P = [1.077218 -0.022949 1.001342 0.000309 0.295099;
             1.076074 -0.022129 1.001279 0.000299 0.295298;
             1.181472 -0.141171 1.080759 -0.000775 0.239466;
             1.080000 -0.040000 1.050000 -0.030000 0.250000;
             1.100000 -0.050000 1.100000 -0.010000 0.100000;
             1.100000 -0.050000 1.100000 -0.010000 0.200000;
             1.100000 -0.050000 1.100000 -0.010000 0.300000;
             1.100000 -0.050000 1.100000 -0.010000 0.400000];
    end

    % ── 이분(bisection) 앵커 ──
    %   갈렸을 때 **어느 단계에서** 갈렸는지 좁히는 값들이다. CSV 앞머리에
    %   `# 이름,값` 으로 같이 적는다 — 화면에만 찍으면 사용자가 CSV 만
    %   보내 왔을 때 이분할 근거가 사라진다.
    [~, nuq1, nin1] = local_rmse_dqdv(Ecell, P(1, :), x_model, vol_dq_fit, ...
                                      dq_fit_data, w_peak, false, diff_params);
    anchors = { ...
        'c_cell',         c_cell; ...
        'dv_lo',          lo;     ...
        'dv_hi',          hi;     ...
        'dv_n',           sum(idx); ...
        'dq_lo',          vlo;    ...
        'dq_hi',          vhi;    ...
        'dq_n',           sum(mv); ...
        'n_peaks',        numel(pk_locs); ...
        'w_peak_sum',     sum(w_peak); ...
        'w_peak_max',     max(w_peak); ...
        'dq_nuniq_p1',    nuq1;   ...
        'dq_nin_p1',      nin1;   ...
        'E_PE_0p5',       ro.E_PE(0.5); ...
        'E_NE_0p5_0p25',  E_NE(0.5, 0.25); ...
        'dv_PE_0p5',      ro.dv_PE(0.5); ...
        'dv_NE_0p5_0p25', dv_NE(0.5, 0.25)};

    fprintf('\n=== dd_eval ===\n');
    fprintf('state=%s  halfcell=%s  Si=%s  w_dqdv=%g\n', o.State, o.HalfCellDir, o.SiSource, o.WDqdv);
    fprintf('sgolayfilt=%s  quantile=%s  findpeaks=%s\n', ...
            impl('sgolayfilt'), impl('quantile'), impl('findpeaks'));
    for k = 1:size(anchors, 1)
        fprintf('%-16s = %.17g\n', anchors{k, 1}, anchors{k, 2});
    end
    fprintf('\n');

    rows = {};
    hdr = 'a_PE,b_PE,a_NE,b_NE,gamma_Si,rmse_pocv,rmse_dvdq,rmse_dqdv,rmse_dqdv_w';
    RMSE_FMT = '%.17g';   % rmse 네 열의 출력 형식 — CSV 앞머리 `# printed_format` 에 그대로 적힌다
    fprintf('%s\n', hdr);
    for k = 1:size(P, 1)
        q = P(k, :);
        e_model  = Ecell(q, cap);
        r_pocv   = sqrt(mean((vol - e_model) .^ 2));
        dv_model = ro.dv_PE((cap_dv - q(2)) / q(1)) - dv_NE((cap_dv - q(4)) / q(3), q(5));
        r_dvdq   = sqrt(mean((dv_dat - dv_model) .^ 2));
        r_dqdv   = local_rmse_dqdv(Ecell, q, x_model, vol_dq_fit, dq_fit_data, ...
                                   w_peak, false, diff_params);
        r_dqdv_w = local_rmse_dqdv(Ecell, q, x_model, vol_dq_fit, dq_fit_data, ...
                                   w_peak, true,  diff_params);
        % ⚠ rmse 는 %.17g 로 적는다. 전 판은 %.10f 였는데, 그러면 절대
        %   양자화가 ±0.5e-10 이라 rmse≈0.0117 에서 그것만으로 상대 4.3e-9 다.
        %   그 자리수로 적힌 파일을 상대 1e-9 로 재면 **없는 불일치**가 나온다
        %   (2026-09-10 실측). 전정밀도로 적어야 대조가 그 아래로 내려간다.
        rows{end+1} = sprintf(['%.6f,%.6f,%.6f,%.6f,%.6f,' RMSE_FMT ',' RMSE_FMT ',' RMSE_FMT ',' RMSE_FMT], ...
            q(1), q(2), q(3), q(4), q(5), r_pocv, r_dvdq, r_dqdv, r_dqdv_w); %#ok<AGROW>
        fprintf('%s\n', rows{end});
    end

    if ~isempty(o.Out)
        fid = fopen(o.Out, 'w');
        fprintf(fid, '# dd_eval  state=%s  halfcell=%s  Si=%s  w_dqdv=%g\n', ...
                o.State, o.HalfCellDir, o.SiSource, o.WDqdv);
        % ⚠ 형식 선언 (Codex R3-06): 비교기가 값의 길이로 정밀도를 **추정**하지 않게
        %   rmse 열의 출력 형식을 파일이 직접 말한다. 아래 rows 의 sprintf 와 같아야 한다.
        fprintf(fid, '# printed_format,%s\n', RMSE_FMT);
        fprintf(fid, '# impl_sgolayfilt,%s\n', impl('sgolayfilt'));
        fprintf(fid, '# impl_quantile,%s\n', impl('quantile'));
        fprintf(fid, '# impl_findpeaks,%s\n', impl('findpeaks'));
        for k = 1:size(anchors, 1)
            fprintf(fid, '# %s,%.17g\n', anchors{k, 1}, anchors{k, 2});
        end
        fprintf(fid, '%s\n', hdr);
        for k = 1:numel(rows), fprintf(fid, '%s\n', rows{k}); end
        fclose(fid);
        fprintf('\nwrote %s\n', o.Out);
    end
end

% ══════════════════════════════════════════════════════════════════════
function tag = local_impl_tag(fname)
%LOCAL_IMPL_TAG  그 함수가 우리 shim 인지 MATLAB 것인지.
    w = which(fname);
    if isempty(w)
        tag = 'missing';
    elseif ~isempty(strfind(w, 'dd_shims'))
        tag = 'dd_shims';
    else
        tag = 'matlab';
    end
end

function [w, locs] = local_peak_weights(vol, dq, peak_weight, sigma_ratio)
%LOCAL_PEAK_WEIGHTS  규진팀 `build_peak_weights_local` 의 **전사본**.
%
%   ⚠ 출처 주의 — 여기가 이 파일에서 가장 약한 고리다.
%     `build_peak_weights_local` 과 `compute_dqdv_rmse_blend` 는 그들
%     `electrode_balancing_blend.m` 안의 **로컬 함수**라서 파일 밖에서 부를 수
%     없다. 그래서 dd_eval 은 그 둘만은 **불러 쓰지 못하고 옮겨 적었다**
%     (앞의 pOCV·dV/dQ 경로는 그들 `electrode_ocv`·`differential`·
%     `build_blend_functions` 를 그대로 호출한다).
%     그러므로 이 두 함수에 대해서는 대조가 「우리 Python 포팅 ↔ 우리 MATLAB
%     전사」이고, **「그들 코드 ↔ 우리 포팅」이 아니다.** 여기서 일치가 나와도
%     그것은 언어 간 구현 차이(1-based 인덱스·unique 규약·interp1·findpeaks)
%     가 없다는 뜻이지, 우리가 그들 식을 옳게 읽었다는 증명이 아니다.
%     ⇒ 규진팀에게 **이 두 함수를 눈으로 대조해 달라**고 부탁할 것.
    w = ones(size(dq));
    prom = 0.1 * (max(dq) - min(dq));
    [~, locs] = findpeaks(dq, 'MinPeakProminence', prom);
    if isempty(locs)
        return
    end
    sigma = sigma_ratio * (max(vol) - min(vol));
    for k = 1:numel(locs)
        w = w + (peak_weight - 1) * exp(-((vol - vol(locs(k))) .^ 2) / (2 * sigma ^ 2));
    end
end

function [r, nuniq, nin] = local_rmse_dqdv(Ecell, q, x_model, v_ref, dq_ref, w, weighted, dp)
%LOCAL_RMSE_DQDV  규진팀 `compute_dqdv_rmse_blend`(+가중판) 의 **전사본**.
%   출처 주의는 local_peak_weights 머리말과 같다.
%
%   이 경로에는 조용히 점을 버리는 자리가 둘 있어서 개수를 같이 돌려준다:
%     nuniq — `unique(v_smooth)` 뒤 남은 점. 모델 전압이 단조가 아니면 준다.
%     nin   — 보간 범위 안에 든 실측 격자점. 5 미만이면 원본이 1e6 을 낸다.
    v_model  = Ecell(q, x_model);
    v_smooth = sgolayfilt(v_model(:), dp.poly_order, dp.window);
    dq_model = gradient(x_model(:)) ./ gradient(v_smooth);
    [v_u, uid] = unique(v_smooth);
    dq_u  = dq_model(uid);
    nuniq = numel(v_u);
    idx   = (v_ref >= min(v_u)) & (v_ref <= max(v_u));
    nin   = sum(idx);
    if nin < 5
        r = 1e6;
        return
    end
    dq_i  = interp1(v_u, dq_u, v_ref(idx), 'linear');
    resid = dq_ref(idx) - dq_i;
    if weighted
        ww = w(idx);
        r  = sqrt(sum(ww .* resid .^ 2) / sum(ww));
    else
        r  = sqrt(mean(resid .^ 2));
    end
end

function name = local_halfcell_name(dirpath, state)
    if contains(dirpath, '005C')
        name = sprintf('%s_005C.xlsx', state);
    else
        name = sprintf('%s.xlsx', state);
    end
end

function [c, v] = local_fullcell(state)
    d = dir(fullfile('data','full_cell','large_cell_033C','*.xlsx'));
    f = '';
    for k = 1:numel(d)
        if ~contains(d(k).name, 'pristine') && ~contains(d(k).name, '300cycle')
            f = fullfile(d(k).folder, d(k).name); break
        end
    end
    if isempty(f), error('dd_eval: 풀셀 워크북을 못 찾았다'); end
    order = {'pristine','100','200','300_0009','300_0147'};
    col = find(strcmp(order, state), 1);
    if isempty(col), error('dd_eval: 모르는 state "%s"', state); end
    M = readmatrix(f, 'Range', 'A3');
    c = M(:, 2*col-1); v = M(:, 2*col);
    ok = ~isnan(c) & ~isnan(v);
    c = c(ok); v = v(ok);
end

function lit = local_load_lit(si_source)
    lit_dir = fullfile('data','literature');
    g = readtable(fullfile(lit_dir, 'Si_Gr_literature_OCP.xlsx'));
    s = readtable(fullfile(lit_dir, 'Si_OCP_sources', [si_source '.csv']));
    lit = struct('Si_capacity', s.normalizedCapacity, 'Si_voltage', s.voltage, ...
                 'Gr_capacity', g.Gr_capacity(~isnan(g.Gr_capacity)), ...
                 'Gr_voltage',  g.Gr_voltage(~isnan(g.Gr_voltage)));
end
