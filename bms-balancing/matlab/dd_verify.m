function dd_verify(mode, varargin)
%DD_VERIFY  α·β 검증 드라이버 — 규진팀 코드를 **고치지 않고** 그대로 호출한다.
%
%   이 파일은 `electrode_balancing_blend.m` 와 같은 폴더(프로젝트 루트)에 둔다.
%   기존 함수(electrode_ocv · electrode_balancing_blend · build_blend_functions ·
%   extractMyData · averageDuplicates)를 그대로 부르므로, 여기서 나오는 값은
%   **그들 파이프라인의 값**이다.
%
%   왜 필요한가: Python 포팅(`bms-balancing/`)이 재는 축퇴가 진짜 그들 모델의
%   성질인지 확인하려면, **같은 것을 MATLAB 에서도 찍어 봐야** 한다. 포팅이
%   틀렸으면 그 위의 모든 숫자가 틀린다.
%
% 사용법
%   dd_verify('check')                % ★ 먼저 이것. 경로·툴박스·데이터를 몇 초 만에 확인
%   dd_verify('dump')                 % 여러 설정에서 적합 결과를 한 줄씩 출력
%   dd_verify('profile')              % γ_Si 를 고정하고 나머지 넷 재적합
%   dd_verify('scalenoise')           % 같은 설정을 5번 — 목적함수 scale 의 난수 영향
%
% 옵션 (이름-값)
%   'HalfCellDir'  기본 'data/half_cell/GITT/'
%   'FullCellFile' 기본 자동 탐색 (data/full_cell/large_cell_033C/*.xlsx 중 2행 헤더)
%   'SiSource'     기본 'Li'      ('Baggetto','Friedrich','Jiang','Kunz','Li','Lu','Sethuraman','Wetjen')
%   'State'        기본 '300_0009'
%   'RefState'     기본 'pristine'
%   'WDqdv'        기본 0          (1 이면 dQ/dV 항 포함)
%   'Gammas'       기본 0:0.025:0.5 (profile 모드)
%   'Out'          기본 ''         (비우면 화면만, 주면 그 CSV 로 저장)
%
% 출력은 **CSV 한 줄씩**이라 그대로 Python 쪽 표와 대조할 수 있다.

    if nargin < 1, mode = 'dump'; end

    p = inputParser;
    p.addParameter('HalfCellDir', 'data/half_cell/GITT/');
    p.addParameter('FullCellFile', '');
    p.addParameter('SiSource', 'Li');
    p.addParameter('State', '300_0009');
    p.addParameter('RefState', 'pristine');
    p.addParameter('WDqdv', 0);
    p.addParameter('Gammas', 0:0.025:0.5);
    p.addParameter('Out', '');
    p.parse(varargin{:});
    o = p.Results;

    % ── 공통 설정 — main_blend_final.m 과 **같은 값**을 쓴다 ──
    diff_params = struct('window', 11, 'poly_order', 3);

    % check 는 **아무것도 없어도** 돌아야 한다 — 없는 것을 알려 주는 게 일이다.
    if strcmpi(mode, 'check')
        local_check(o, diff_params);
        return
    end

    if isempty(o.FullCellFile)
        o.FullCellFile = local_find_fullcell();
    end

    fit_params  = struct('peak_weight', 7, 'sigma_ratio', 0.03, ...
                         'use_peak_weight', true, 'weight_pe_peaks', false, ...
                         'w_pocv', 1.0, 'w_dvdq', 1.0, 'w_dqdv', o.WDqdv);
    initial5 = [1.08, -0.04, 1.05, -0.03, 0.25];
    lb5      = [1.0,  -0.5,  1.0,  -0.5,  0.00];
    ub5      = [1.4,   0,    1.4,   0.1,  0.50];

    lit = local_load_lit(o.SiSource);

    switch lower(mode)
    case 'dump'
        rows = {};
        w  = o.WDqdv;                 % 한 번에 한 축만 — 두 축을 섞으면 뭐가 움직였는지 못 가른다
        fp = fit_params; fp.w_dqdv = w;
        fprintf('si_source,w_dqdv,a_PE,b_PE,a_NE,b_NE,gamma_Si,rmse_pocv,rmse_dvdq,LAM_PE_pct,LAM_NE_pct,LLI_pct,bounds\n');
        for si = {'Baggetto','Friedrich','Jiang','Kunz','Li','Lu','Sethuraman','Wetjen'}
            L = local_load_lit(si{1});
            rng(0, 'twister');    % ★ 발견 4 — 원본은 seed 가 없다. 비교하려면 고정해야 한다
            r0 = local_fit(o.RefState, o, L, initial5, lb5, ub5, diff_params, fp);
            rng(0, 'twister');
            r1 = local_fit(o.State,    o, L, initial5, lb5, ub5, diff_params, fp);
            m  = local_modes(r0, r1);
            rows{end+1} = local_row(si{1}, w, r1, m, lb5, ub5); %#ok<AGROW>
            fprintf('%s\n', rows{end});
        end
        local_save(o.Out, {'si_source,w_dqdv,a_PE,b_PE,a_NE,b_NE,gamma_Si,rmse_pocv,rmse_dvdq,LAM_PE_pct,LAM_NE_pct,LLI_pct,bounds'}, rows);

    case 'profile'
        % ⚠ 2026-09-10: 이 모드는 lbg(5)=ubg(5)=g 를 넘겨 γ 를 묶는데,
        %   electrode_balancing_blend.m 의 scale 표본이
        %       samples = lb + rand(50,5) .* (ub - lb)
        %   로 **넘겨받은 경계**를 쓴다 (원본 확인함). 그래서 γ 를 묶으면
        %   행마다 scale 이 달라지고 **행마다 다른 목적함수를 최소화**하게
        %   된다. 원 파이프라인(main_blend_final.m)은 고정-γ 프로파일을 하지
        %   않으므로 이건 그들 절차가 아니라 이 모드의 부작용이다.
        %   → 행끼리 목적함수 값을 비교하지 마라. 파라미터 추세만 읽어라.
        %   (그래서 이 모드는 rmse_pocv 만 찍는다 — 목적함수 비율은 안 찍는다.)
        fprintf(['[경고] profile 모드는 γ 를 경계로 묶으므로 행마다 목적함수의 ' ...
                 'scale 이 달라진다.\n        행끼리 목적함수 비교 금지 — ' ...
                 '파라미터 추세만 읽을 것.\n']);
        rng(0, 'twister');
        r0 = local_fit(o.RefState, o, lit, initial5, lb5, ub5, diff_params, fit_params);
        rows = {};
        fprintf('gamma_Si,a_PE,b_PE,a_NE,b_NE,rmse_pocv_mV,LAM_PE_pct,LAM_NE_pct,LLI_pct,bounds\n');
        for g = o.Gammas
            lbg = lb5; ubg = ub5; ini = initial5;
            lbg(5) = g; ubg(5) = g; ini(5) = g;      % γ 를 못 움직이게 묶는다
            rng(0, 'twister');
            r = local_fit(o.State, o, lit, ini, lbg, ubg, diff_params, fit_params);
            m = local_modes(r0, r);
            rows{end+1} = sprintf('%.4f,%.6f,%.6f,%.6f,%.6f,%.3f,%.4f,%.4f,%.4f,%s', ...
                g, r.a_PE, r.b_PE, r.a_NE, r.b_NE, 1000*r.rmse_pocv, ...
                m.LAM_PE*100, m.LAM_NE*100, m.LLI*100, ...
                local_bounds([r.a_PE r.b_PE r.a_NE r.b_NE], lb5(1:4), ub5(1:4))); %#ok<AGROW>
            fprintf('%s\n', rows{end});
        end
        local_save(o.Out, {'gamma_Si,a_PE,b_PE,a_NE,b_NE,rmse_pocv_mV,LAM_PE_pct,LAM_NE_pct,LLI_pct,bounds'}, rows);

    case 'scalenoise'
        % ★ 발견 4 를 눈으로 본다 — seed 만 바꿔 같은 적합을 5번
        rows = {};
        fprintf('seed,a_PE,b_PE,a_NE,b_NE,gamma_Si,rmse_pocv_mV\n');
        for s = 0:4
            rng(s, 'twister');
            r = local_fit(o.State, o, lit, initial5, lb5, ub5, diff_params, fit_params);
            rows{end+1} = sprintf('%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.3f', ...
                s, r.a_PE, r.b_PE, r.a_NE, r.b_NE, r.gamma_Si, 1000*r.rmse_pocv); %#ok<AGROW>
            fprintf('%s\n', rows{end});
        end
        local_save(o.Out, {'seed,a_PE,b_PE,a_NE,b_NE,gamma_Si,rmse_pocv_mV'}, rows);

    otherwise
        error('dd_verify: 모르는 mode "%s" (dump|profile|scalenoise)', mode);
    end
end

% ══════════════════════════════════════════════════════════════════════
function local_check(o, diff_params)
%LOCAL_CHECK  긴 적합을 돌리기 전에 몇 초 만에 확인한다.
%
%   여기서 나오는 [FAIL] 은 전부 **적합을 시작하면 몇십 분 뒤에 죽을 것**들이다.
%   하나도 안 죽이고 끝까지 센 다음 요약을 낸다 (첫 실패에서 멈추지 않는다).

    fails = 0; warns = 0;
    fprintf('\n=== dd_verify check ===\n현재 폴더: %s\n\n', pwd);

    % ① 그들 함수가 경로에 있는가
    need = {'electrode_balancing_blend','electrode_ocv','build_blend_functions', ...
            'differential','extractMyData','averageDuplicates'};
    for k = 1:numel(need)
        if isempty(which(need{k}))
            fprintf('[FAIL] 함수 없음: %s.m — 프로젝트 루트에서 실행하고 있나?\n', need{k});
            fails = fails + 1;
        else
            fprintf('[ ok ] %s.m\n', need{k});
        end
    end

    % ② 툴박스 — 없으면 적합 도중에 죽는다
    tb = {'fmincon','Optimization Toolbox'; ...
          'MultiStart','Global Optimization Toolbox'; ...
          'createOptimProblem','Global Optimization Toolbox'; ...
          'sgolayfilt','Signal Processing Toolbox'; ...
          'findpeaks','Signal Processing Toolbox'; ...
          'quantile','Statistics and Machine Learning Toolbox'};
    fprintf('\n');
    for k = 1:size(tb,1)
        w = which(tb{k,1});
        if isempty(w)
            fprintf('[FAIL] %-18s 없음 → %s 가 필요하다\n', tb{k,1}, tb{k,2});
            fails = fails + 1;
        elseif ~isempty(strfind(w, 'dd_shims'))
            % ⚠ 전 판은 which() 가 비었는지만 봤다. 그러면 dd_shims 의 대체
            %   구현을 **툴박스가 있다**고 잘못 보고한다. 어느 파일이 잡혔는지
            %   찍어야 그 착각이 안 생긴다.
            fprintf('[shim] %-18s ← %s\n', tb{k,1}, w);
            fprintf('       (MathWorks 구현이 아니다 — 우리 대체품이 잡혔다)\n');
            warns = warns + 1;
        else
            fprintf('[ ok ] %-18s (%s)\n', tb{k,1}, tb{k,2});
        end
    end

    % ③ 데이터 — 반쪽전지
    fprintf('\n');
    states = {'pristine','100','200','300_0009','300_0147'};
    for d = {'data/half_cell/GITT/','data/half_cell/step_005C/'}
        dirp = d{1};
        if ~isfolder(dirp)
            fprintf('[warn] 폴더 없음: %s (이 소스는 못 쓴다)\n', dirp);
            warns = warns + 1;
            continue
        end
        n_ok = 0;
        for s = states
            f = fullfile(dirp, local_halfcell_name(dirp, s{1}));
            if isfile(f), n_ok = n_ok + 1; end
        end
        fprintf('[ ok ] %s — 상태 파일 %d/5\n', dirp, n_ok);
    end

    % ④ 데이터 — 풀셀 워크북 (2행 헤더 레이아웃까지 확인)
    fprintf('\n');
    try
        f = o.FullCellFile;
        if isempty(f), f = local_find_fullcell(); end
        fprintf('[ ok ] 풀셀 워크북: %s\n', f);
        M = readmatrix(f, 'Range', 'A3');
        if size(M,2) < 10
            fprintf('[FAIL] 컬럼이 %d개다 — 상태 5개면 10개(용량·전압 쌍)여야 한다\n', size(M,2));
            fails = fails + 1;
        else
            for i = 1:5
                c = M(:, 2*i-1); c = c(~isnan(c));
                fprintf('        %-10s c_cell = %.3f\n', states{i}, max(c));
            end
        end
    catch ME
        fprintf('[FAIL] 풀셀 워크북: %s\n', ME.message);
        fails = fails + 1;
    end

    % ⑤ 데이터 — 문헌 곡선 8종
    fprintf('\n');
    sis = {'Baggetto','Friedrich','Jiang','Kunz','Li','Lu','Sethuraman','Wetjen'};
    miss = {};
    for k = 1:numel(sis)
        if ~isfile(fullfile('data','literature','Si_OCP_sources',[sis{k} '.csv']))
            miss{end+1} = sis{k}; %#ok<AGROW>
        end
    end
    if isempty(miss)
        fprintf('[ ok ] 문헌 Si OCP 8종 전부\n');
    else
        fprintf('[FAIL] 문헌 Si OCP 없음: %s\n', strjoin(miss, ', '));
        fails = fails + 1;
    end
    if isfile(fullfile('data','literature','Si_Gr_literature_OCP.xlsx'))
        fprintf('[ ok ] Si_Gr_literature_OCP.xlsx\n');
    else
        fprintf('[FAIL] Si_Gr_literature_OCP.xlsx 없음\n');
        fails = fails + 1;
    end

    % ⑥ 실제로 한 번 읽고 섞어 본다 (적합은 안 한다 — 몇 초면 끝난다)
    fprintf('\n');
    if fails == 0
        try
            t0 = tic;
            ro = electrode_ocv(o.HalfCellDir, local_halfcell_name(o.HalfCellDir, 'pristine'), diff_params);
            lit = local_load_lit(o.SiSource);
            [E_NE, ~] = build_blend_functions(lit.Si_capacity, lit.Si_voltage, ...
                                              lit.Gr_capacity, lit.Gr_voltage, diff_params);
            v = ro.E_PE(0.5) - E_NE(0.5, 0.25);
            fprintf('[ ok ] 배관 확인 — E_PE(0.5) − E_NE(0.5, γ=0.25) = %.4f V  (%.1f 초)\n', v, toc(t0));
            if v < 2.5 || v > 4.5
                fprintf('[warn] 그 값이 셀 전압 범위(2.5~4.5 V) 밖이다 — 방향 규약을 의심할 것\n');
                warns = warns + 1;
            end
        catch ME
            fprintf('[FAIL] 배관: %s\n', ME.message);
            fails = fails + 1;
        end
    else
        fprintf('[skip] 배관 확인 — 위 [FAIL] 부터 고칠 것\n');
    end

    fprintf('\n=== 결과: FAIL %d · warn %d ===\n', fails, warns);
    if fails == 0
        fprintf('돌려도 된다:\n');
        fprintf("  dd_verify('dump','State','300_0009','WDqdv',0,'Out','dd_dump_gitt_w0.csv')\n\n");
    else
        fprintf('위 [FAIL] 을 먼저 고칠 것. 지금 dump 를 돌리면 도중에 죽는다.\n');
        fprintf('툴박스가 없다면: 적합은 못 하지만 **목적함수 평가**는 된다 —\n');
        fprintf("  addpath('dd_shims','-end'); dd_eval()\n");
        fprintf('  (dd_shims 는 sgolayfilt·quantile 의 우리 대체 구현이다. MathWorks 것이 아니다.)\n\n');
    end
end

% ══════════════════════════════════════════════════════════════════════
function r = local_fit(state, o, lit, initial5, lb5, ub5, diff_params, fit_params)
    hc = local_halfcell_name(o.HalfCellDir, state);
    result_ocv = electrode_ocv(o.HalfCellDir, hc, diff_params);

    [c_full, v_full] = local_fullcell(o.FullCellFile, state);
    T = table(c_full, v_full, 'VariableNames', {'0_capacity','0_voltage'});
    tmp = sprintf('dd_verify_%s.xlsx', matlab.lang.makeValidName(state));
    writetable(T, fullfile(tempdir, tmp));

    r = electrode_balancing_blend(result_ocv, lit, tempdir, tmp, 0, ...
        initial5, lb5, ub5, "combined", "none", diff_params, fit_params);
end

function m = local_modes(r0, r)
    % main_blend_final.m 의 식 그대로
    m.LAM_PE = (r0.a_PE*r0.c_cell - r.a_PE*r.c_cell) / (r0.a_PE*r0.c_cell);
    m.LAM_NE = (r0.a_NE*r0.c_cell - r.a_NE*r.c_cell) / (r0.a_NE*r0.c_cell);
    c_lit_i  = (r0.a_PE + r0.b_PE - r0.b_NE) * r0.c_cell;
    c_lit    = (r.a_PE  + r.b_PE  - r.b_NE ) * r.c_cell;
    m.LLI    = (c_lit_i - c_lit) / c_lit_i;
end

function s = local_row(si, w, r, m, lb5, ub5)
    s = sprintf('%s,%g,%.6f,%.6f,%.6f,%.6f,%.6f,%.6g,%.6g,%.4f,%.4f,%.4f,%s', ...
        si, w, r.a_PE, r.b_PE, r.a_NE, r.b_NE, r.gamma_Si, ...
        r.rmse_pocv, r.rmse_dvdq, m.LAM_PE*100, m.LAM_NE*100, m.LLI*100, ...
        local_bounds([r.a_PE r.b_PE r.a_NE r.b_NE r.gamma_Si], lb5, ub5));
end

function s = local_bounds(p, lb, ub)
    names = {'a_PE','b_PE','a_NE','b_NE','gamma_Si'};
    hit = {};
    for i = 1:numel(p)
        if abs(p(i) - lb(i)) < 1e-6, hit{end+1} = [names{i} '=lb']; end %#ok<AGROW>
        if abs(p(i) - ub(i)) < 1e-6, hit{end+1} = [names{i} '=ub']; end %#ok<AGROW>
    end
    if isempty(hit), s = '-'; else, s = strjoin(hit, '|'); end
end

function name = local_halfcell_name(dirpath, state)
    if contains(dirpath, '005C')
        name = sprintf('%s_005C.xlsx', state);
    else
        name = sprintf('%s.xlsx', state);
    end
end

function f = local_find_fullcell()
    d = dir(fullfile('data','full_cell','large_cell_033C','*.xlsx'));
    keep = {};
    for k = 1:numel(d)
        if ~contains(d(k).name, 'pristine') && ~contains(d(k).name, '300cycle')
            keep{end+1} = fullfile(d(k).folder, d(k).name); %#ok<AGROW>
        end
    end
    if isempty(keep)
        error('dd_verify: data/full_cell/large_cell_033C 에서 상태별 워크북을 못 찾았다');
    end
    f = keep{1};
end

function [c, v] = local_fullcell(file, state)
    % 2행 헤더(1행=상태명, 2행=단위)에서 그 상태의 컬럼쌍
    order = {'pristine','100','200','300_0009','300_0147'};
    col = find(strcmp(order, state), 1);
    if isempty(col)
        error('dd_verify: 모르는 state "%s"', state);
    end
    M = readmatrix(file, 'Range', 'A3');
    c = M(:, 2*col-1);
    v = M(:, 2*col);
    ok = ~isnan(c) & ~isnan(v);
    c = c(ok); v = v(ok);
end

function lit = local_load_lit(si_source)
    lit_dir = fullfile('data','literature');
    g = readtable(fullfile(lit_dir, 'Si_Gr_literature_OCP.xlsx'));
    Gr_c = g.Gr_capacity(~isnan(g.Gr_capacity));
    Gr_v = g.Gr_voltage(~isnan(g.Gr_voltage));
    s = readtable(fullfile(lit_dir, 'Si_OCP_sources', [si_source '.csv']));
    lit = struct('Si_capacity', s.normalizedCapacity, 'Si_voltage', s.voltage, ...
                 'Gr_capacity', Gr_c, 'Gr_voltage', Gr_v);
end

function local_save(out, header, rows)
    if isempty(out), return; end
    fid = fopen(out, 'w');
    fprintf(fid, '%s\n', header{1});
    for k = 1:numel(rows)
        fprintf(fid, '%s\n', rows{k});
    end
    fclose(fid);
    fprintf('\nwrote %s\n', out);
end
