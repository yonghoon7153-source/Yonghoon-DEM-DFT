function out = fit_cycles_driver(cfg)
% fit_cycles_driver - 규진팀 파이프라인(electrode_balancing_blend 등)을 **그대로** 사이클별로 돌려
% 11 열 결과표 + 설정/입력 identity sidecar 를 쓴다.
%
% 결정 실험 (reviews/BML_R1_RESPONSE.md §9): 핸드오프가 "제거 완료" 라고 적은 rng(0) 전역 오염 없이
% 다시 돌리면 결과표의 값 반복(a_PE 가 사이클마다 비트 동일 · a_NE 파일 내부 상수)이 사라지는가.
% 이 드라이버는 원본 함수를 **수정하지 않는다**. 하는 일은 넷:
%   (1) 파이프라인 .m 파일에 `rng(` 고정이 남아 있지 않은지 검사 (남아 있으면 돌리지 않는다)
%   (2) 사이클마다 main_blend_final.m 과 같은 호출 (같은 initial5/lb5/ub5/fit_params/diff_params)
%   (3) 수출 공식(main_blend_final.m:137-151)으로 11 열 계산 — 규진팀 result_L_*.xlsx 와 같은 열
%   (4) 입력 sha256 · 코드 sha256 · 설정 · MATLAB/툴박스 버전을 `<결과>.settings.json` 에 —
%       `python3 scripts/check_rails.py <결과.xlsx>` 가 이 sidecar 를 읽어 3 층(기록된 제약) 검사를 한다.
%
%   cfg.pipeline_dir   규진팀 .m 폴더 (electrode_balancing_blend · build_blend_functions · fit_gamma_si ·
%                      electrode_ocv · extractMyData · averageDuplicates · differential)
%   cfg.data_root      'data/literature/' 가 있는 폴더
%   cfg.half_cell_file 기준(pristine) 반쪽전지 xlsx (PE_capacity/PE_voltage/NE_capacity/NE_voltage)
%   cfg.full_cell_file 풀셀 사이클 워크북 — '<cycle>_capacity' / '<cycle>_voltage' 열 (extractMyData 규약).
%                      cycle 0 이 기준행이어야 한다 (항등식의 분모)
%   cfg.cycles         [] 이면 헤더의 숫자 접두어 전부 (오름차순)
%   cfg.si_source      'Li' 등 — data/literature/Si_OCP_sources/<name>.csv
%   cfg.label          결과 파일 라벨 (예: 'L_ref1')
%   cfg.out_dir        결과 폴더
%   cfg.plotting       기본 "none"
%
% 사용:
%   cfg = struct('pipeline_dir','C:\...\degradation mode', 'data_root','C:\...\degradation mode', ...
%                'half_cell_file','...\data\half_cell\GITT\pristine.xlsx', ...
%                'full_cell_file','...\L_ref1_cycles.xlsx', 'cycles',[], 'si_source','Li', ...
%                'label','L_ref1', 'out_dir','results_refit');
%   out = fit_cycles_driver(cfg);
%
% ⚠ MATLAB + Global Optimization Toolbox(MultiStart) 가 필요하다. Octave 에서는 구문만 검사한다
%   (matlab/tests/run_all.sh 1 단계).

    t_start = datestr(now, 'yyyy-mm-ddTHH:MM:SS');
    req = {'pipeline_dir','data_root','half_cell_file','full_cell_file','si_source','label','out_dir'};
    for k = 1:numel(req)
        if ~isfield(cfg, req{k}) || isempty(cfg.(req{k}))
            error('fit_cycles_driver:cfg', 'cfg.%s 가 없다', req{k});
        end
    end
    if ~isfield(cfg, 'cycles'),   cfg.cycles = [];      end
    if ~isfield(cfg, 'plotting'), cfg.plotting = "none"; end

    % ── (1) rng 고정 검사 — 파이프라인 파일 전부 ──────────────────────────────────────────────
    pipeline_files = {'electrode_balancing_blend.m', 'build_blend_functions.m', 'fit_gamma_si.m', ...
                      'electrode_ocv.m', 'extractMyData.m', 'averageDuplicates.m', 'differential.m'};
    code = struct();
    for k = 1:numel(pipeline_files)
        f = fullfile(cfg.pipeline_dir, pipeline_files{k});
        if ~exist(f, 'file')
            error('fit_cycles_driver:pipeline', '파이프라인 파일이 없다: %s', f);
        end
        txt = fileread(f);
        hit = regexp(txt, '(?<![\w.])rng\s*\(', 'once');
        if ~isempty(hit)
            error('fit_cycles_driver:rng', ['%s 에 rng( 고정이 남아 있다 — 핸드오프 §"폐기한 방향" 1번의 버그다. ' ...
                  '돌리지 않는다 (지우고 다시)'], pipeline_files{k});
        end
        code.(matlab.lang.makeValidName(pipeline_files{k})) = struct('path', f, 'sha256', sha256_of_file(f));
    end
    addpath(cfg.pipeline_dir);
    rs = rng;                                       % 읽기만 — 고정하지 않는다
    toolbox = struct('multistart', exist('MultiStart', 'class') == 8, ...
                     'fmincon', exist('fmincon', 'file') > 0, ...
                     'gads_license', license('test', 'GADS_Toolbox') == 1);
    if ~toolbox.multistart || ~toolbox.fmincon
        error('fit_cycles_driver:toolbox', 'MultiStart/fmincon 이 없다 (Global Optimization Toolbox 필요)');
    end

    % ── (2) 설정 — main_blend_final.m:45-64 그대로 ─────────────────────────────────────────────
    initial5 = [1.08, -0.04, 1.05, -0.03, 0.25];
    ub5      = [1.4,   0,     1.4,  0.1,  0.50];
    lb5      = [1.0,  -0.5,   1.0, -0.5,  0.00];
    fitting_method = "combined";
    diff_params = struct('window', 11, 'poly_order', 3);
    fit_params  = struct('peak_weight', 7, 'sigma_ratio', 0.03, 'use_peak_weight', true, ...
                         'weight_pe_peaks', false, 'w_pocv', 1.0, 'w_dvdq', 1.0, 'w_dqdv', 0.0);

    lit_dir = fullfile(cfg.data_root, 'data', 'literature');
    gr_file = fullfile(lit_dir, 'Si_Gr_literature_OCP.xlsx');
    si_file = fullfile(lit_dir, 'Si_OCP_sources', [cfg.si_source '.csv']);
    lit_gr = readtable(gr_file);
    Gr_capacity_lit = lit_gr.Gr_capacity(~isnan(lit_gr.Gr_capacity));
    Gr_voltage_lit  = lit_gr.Gr_voltage(~isnan(lit_gr.Gr_voltage));
    si_df = readtable(si_file);
    Si_capacity_lit = si_df.normalizedCapacity;
    Si_voltage_lit  = si_df.voltage;
    lit_si_gr = struct('Si_capacity', Si_capacity_lit, 'Si_voltage', Si_voltage_lit, ...
                       'Gr_capacity', Gr_capacity_lit, 'Gr_voltage', Gr_voltage_lit);

    [hc_dir, hc_name, hc_ext] = fileparts(cfg.half_cell_file);
    hc_dir = [hc_dir filesep]; hc_file = [hc_name hc_ext];
    result_ocv = electrode_ocv(hc_dir, hc_file, diff_params);

    % Track B: 기준 반쪽전지의 raw NE 로 gamma_Si 초기값 (main_blend_final.m 과 같은 코드)
    dataTable_hc = readtable(cfg.half_cell_file);
    [NE_capacity_raw, NE_voltage_raw] = extractMyData(dataTable_hc, 'NE');
    [NE_capacity_raw, NE_voltage_raw] = averageDuplicates(NE_capacity_raw, NE_voltage_raw);
    if NE_voltage_raw(end) > NE_voltage_raw(1)
        NE_capacity_norm = 1 - NE_capacity_raw / NE_capacity_raw(end);
    else
        NE_capacity_norm = NE_capacity_raw / NE_capacity_raw(end);
    end
    gfit = fit_gamma_si(NE_capacity_norm, NE_voltage_raw, Si_capacity_lit, Si_voltage_lit, ...
                        Gr_capacity_lit, Gr_voltage_lit, 'gamma_range', [lb5(5), ub5(5)], ...
                        'use_dv', true, 'plot_flag', false);
    initial5(5) = gfit.gamma_Si_fit;

    % ── 사이클 목록 — 헤더의 '<n>_capacity' 접두어 ────────────────────────────────────────────
    [fc_dir, fc_name, fc_ext] = fileparts(cfg.full_cell_file);
    fc_dir = [fc_dir filesep]; fc_file = [fc_name fc_ext];
    T = readtable(cfg.full_cell_file, 'VariableNamingRule', 'preserve');
    names = T.Properties.VariableNames;
    cyc = [];
    for k = 1:numel(names)
        tok = regexp(names{k}, '^(\d+)_capacity$', 'tokens', 'once');
        if ~isempty(tok), cyc(end+1) = str2double(tok{1}); end %#ok<AGROW>
    end
    cyc = sort(unique(cyc));
    if ~isempty(cfg.cycles)
        missing = setdiff(cfg.cycles, cyc);
        if ~isempty(missing)
            error('fit_cycles_driver:cycles', '요청한 cycle 이 워크북에 없다: %s', mat2str(missing));
        end
        cyc = sort(unique(cfg.cycles));
    end
    if isempty(cyc) || cyc(1) ~= 0
        error('fit_cycles_driver:cycles', 'cycle 0 (기준행) 이 없다 — 항등식의 분모가 없다');
    end

    % ── 사이클마다 원본 호출 ───────────────────────────────────────────────────────────────────
    n = numel(cyc);
    a_PE = zeros(n,1); b_PE = a_PE; a_NE = a_PE; b_NE = a_PE; gamma_Si = a_PE; C_cell = a_PE;
    rmse_pocv = a_PE; rmse_dvdq = a_PE; rmse_dqdv = a_PE; elapsed_s = a_PE;
    for i = 1:n
        fprintf('\n========== %s cycle %d ==========\n', cfg.label, cyc(i));
        t0 = tic;
        r = electrode_balancing_blend(result_ocv, lit_si_gr, fc_dir, fc_file, cyc(i), ...
                                      initial5, lb5, ub5, fitting_method, cfg.plotting, diff_params, fit_params);
        elapsed_s(i) = toc(t0);
        a_PE(i) = r.a_PE; b_PE(i) = r.b_PE; a_NE(i) = r.a_NE; b_NE(i) = r.b_NE;
        gamma_Si(i) = r.gamma_Si; C_cell(i) = r.c_cell;
        rmse_pocv(i) = r.rmse_pocv; rmse_dvdq(i) = r.rmse_dvdq; rmse_dqdv(i) = r.rmse_dqdv;
    end

    % ── (3) 수출 공식 — main_blend_final.m:137-151 그대로 ─────────────────────────────────────
    x_cell = C_cell / C_cell(1);
    c_lit  = C_cell .* (a_PE + b_PE - b_NE);
    LAM_PE = (a_PE(1)*C_cell(1) - a_PE.*C_cell) / (a_PE(1)*C_cell(1));
    LAM_NE = (a_NE(1)*C_cell(1) - a_NE.*C_cell) / (a_NE(1)*C_cell(1));
    LLI    = (c_lit(1) - c_lit) / c_lit(1);
    cycle  = cyc(:);
    result = table(cycle, C_cell, x_cell, a_PE, b_PE, a_NE, b_NE, c_lit, LAM_PE, LAM_NE, LLI, ...
                   gamma_Si, rmse_pocv, rmse_dvdq, rmse_dqdv, elapsed_s);

    if ~exist(cfg.out_dir, 'dir'), mkdir(cfg.out_dir); end
    stem = sprintf('result_%s_%s', cfg.label, cfg.si_source);
    xlsx = fullfile(cfg.out_dir, [stem '.xlsx']);
    csvf = fullfile(cfg.out_dir, [stem '.csv']);
    writetable(result, xlsx);
    writetable(result, csvf);

    % ── (4) sidecar — check_rails.py 가 <xlsx>.settings.json 을 읽는다 ─────────────────────────
    v = ver('MATLAB');
    sc = struct();
    sc.label = cfg.label; sc.si_source = cfg.si_source; sc.cycles = cyc(:)';
    sc.lb = lb5; sc.ub = ub5; sc.initial = initial5; sc.free = {'a_PE','b_PE','a_NE','b_NE','gamma_Si'};
    sc.n_multistart = 20; sc.n_multistart_pre = 10;     % electrode_balancing_blend.m: run(ms_pre,…,10) · run(ms,…,20)
    sc.fitting_method = char(fitting_method); sc.fit_params = fit_params; sc.diff_params = diff_params;
    sc.gamma_init_trackB = initial5(5);
    sc.rng_guard = 'clean (pipeline 7 files, no rng( call)'; sc.rng_type = rs.Type;
    sc.matlab = struct('version', version, 'release', v.Release, 'toolbox', toolbox);
    sc.inputs = struct('half_cell', struct('path', cfg.half_cell_file, 'sha256', sha256_of_file(cfg.half_cell_file)), ...
                       'full_cell', struct('path', cfg.full_cell_file, 'sha256', sha256_of_file(cfg.full_cell_file)), ...
                       'literature', struct('gr', struct('path', gr_file, 'sha256', sha256_of_file(gr_file)), ...
                                            'si', struct('path', si_file, 'sha256', sha256_of_file(si_file))));
    sc.pipeline_code = code;
    sc.driver = struct('path', mfilename('fullpath'), 'sha256', sha256_of_file([mfilename('fullpath') '.m']));
    sc.started = t_start; sc.finished = datestr(now, 'yyyy-mm-ddTHH:MM:SS');
    sc.host = getenv('COMPUTERNAME'); if isempty(sc.host), sc.host = getenv('HOSTNAME'); end
    sc.result_sha256 = struct('xlsx', sha256_of_file(xlsx), 'csv', sha256_of_file(csvf));
    fid = fopen([xlsx '.settings.json'], 'w');
    fwrite(fid, jsonencode(sc), 'char'); fclose(fid);
    fid = fopen([csvf '.settings.json'], 'w');
    fwrite(fid, jsonencode(sc), 'char'); fclose(fid);

    fprintf('\n결과: %s (+ .csv, .settings.json)\n', xlsx);
    fprintf('다음: python3 scripts/check_rails.py "%s"\n', xlsx);
    out = struct('result', result, 'sidecar', sc, 'xlsx', xlsx, 'csv', csvf);
end

function h = sha256_of_file(path)
% 파일 bytes 의 sha256 (java) — Python 쪽 provenance 와 같은 값
    fid = fopen(path, 'rb');
    if fid < 0, error('fit_cycles_driver:read', '읽지 못했다: %s', path); end
    bytes = fread(fid, inf, '*uint8'); fclose(fid);
    md = java.security.MessageDigest.getInstance('SHA-256');
    md.update(bytes);
    h = lower(reshape(dec2hex(typecast(md.digest(), 'uint8'), 2)', 1, []));
end
