---
source_url: https://github.com/REIL-UConn/Multi-Objective-Optimization-for-Lithium-Ion-Battery-Degradation-Diagnostics
ingested: 2026-10-03
sha256: 427325be907de8cc4b50a16ec9c12f12da2ca0be2097e84dd8c3bc8435d2bd6f
---

수집 목적: 경쟁 · 비교 도구 + 실험 아이디어 (일일 브리핑 ② · ④ 축) — 브리핑 (2026-10-02 조사분) 이 "알려진 제작 조건으로 LLI/LAM 추정 검증" 후보로 든 REIL-UConn 저장소에서 **참값 (설계값) 표가 어디에 어떤 꼴로 있는가**, 피팅 변수 · 목적 함수 · 건강 매개변수 계산이 무엇인가를 원문으로 남긴다. 실행은 하지 않았다 (읽기만). 사용자 지시 2026-10-03 "관련해서도 확인을 해보고 사용가능한지 판단을 해보고".

---

# REIL-UConn 다목적 피팅 저장소 — 참값 표 · 목적 함수 원문 (2026-10-03 · 읽기만)

## 받은 것

- 공개 저장소 `https://github.com/REIL-UConn/Multi-Objective-Optimization-for-Lithium-Ion-Battery-Degradation-Diagnostics` 를 `git clone --depth 1` (얕은 복제 · 저장소 밖 `/home/user/REIL-UConn/moo`). 끝 커밋 (`git log -1` 원문): `1188c371e5836df4a7e5f5acf336a34ffd4027e6 2026-07-12 23:24:04 -0400 Update README to include dataset link and citation`.
- 노트북 실행 0 · `results/*.pkl` 는 **열지 않았다** (pickle 역직렬화 = 임의 코드 실행 — 남의 파일은 버리는 환경에서도 열지 않는다). 디지털 커먼즈 자료 페이지는 받지 않았다.
- 라이선스: 아래 코드 발췌는 MIT (원문 아래) — 저작권 표기를 함께 싣는다.

### 추적 파일 · 크기 · sha256 (`git ls-files` 순)

| 파일 | 바이트 | sha256 |
|---|---|---|
| `Benchmarking_LFP_final.ipynb` | 4,134,001 | `388f2a6f101abf42ef8c7c1c627b7046e8bf900b913d22f83435b39eb81a9e29` |
| `LFP_Data.xlsx` | 10,841,377 | `fd50e09542be7adb2270963d65a6e7b5ccae1473a512f68462c2dd419d620ee1` |
| `LICENSE` | 1,067 | `0c95990daf792fe897f5ca90262d9d682c1b3e9c705a257ecf591e031c1f4786` |
| `README.md` | 4,188 | `1eaf4a09133c529cb60ca8d3caa3b488384eb0dc1356732d5c7cd2cd35c2cb72` |
| `results/LFP_Combined_Panel_SelectedCells_R1.pdf` | 53,927 | `ebf2ffd864682461109aa8a0a469959e2da004dae75952f632ff4b300b85cf2b` |
| `results/LFP_Health_Parameters_V2_R1.pdf` | 48,652 | `93918406d686db5de82362f637071eef524c6baa7b41e93d3267305439cfb6ca` |
| `results/LFP_Models_R1.pkl` | 514,030 | `e66ef8d530a497d7727f7386550576c14c82437fa617865162169d0bad1c9e2f` |
| `results/LFP_Objective_Stacks_byCell_horizontal_maxScaled_R1.pdf` | 49,523 | `96756191ad7923737cbfe6ca87d7a88af046d050575f9b03fb1e43ea534f71a4` |
| `results/LFP_QV_DVDQ_Comparison_Main_Text_R1.pdf` | 66,910 | `4f7268de2dea8f2f1c815b38a87a63f61860f8b26f8c5fb04a3250ec599b8251` |
| `results/LFP_QV_DVDQ_Comparison_R1.pdf` | 152,764 | `9d91585a15aca94ae70ec6ad7348fb7f52e33ea27857cea401dc1b796f3908c2` |
| `results/LFP_Results_R1.pkl` | 4,935,385 | `e5c0795336fe7b762a6b946863abb91972721ebd067d5842d314c0845cd1a2f2` |
| `results/LFP_hps_R1.pkl` | 69,725 | `2bbbdb63b405fa93602a4240d326ceca13f169fcc727256377dacb1cb0ea6214` |
| `util_LFP.py` | 33,754 | `3c19e45ef8a64ce67cda1f623551e758d4c0f67086bbae02b978428d78de1c76` |

## 노트북 `Benchmarking_LFP_final.ipynb` — 셀 원문 (번호는 0 부터)

### 셀 3 — 목적 함수 조합 여섯

```python
# Six cases for the single- and multi-objective optimization
case_selection = {0:[1],
                  1:[0,1],
                  2:[2,3],
                  3:[0,1,2],
                  4:[0,1,3],
                  5:[0,1,2,3],}
```

### 셀 4 — 반쪽전지 전극 질량 (명목값)

```python
# Calculate the mass of half cell electrodes, based on nominal values

# LFP mass loading: 13.5 mg/cm2
# Graphite mass loading: 5.77 mg/cm2
# Electrode diameter: 1.2 cm

area = 0.25 * np.pi * 1.2**2  # cm^2
LFP_mass_12 = 13.5 *  area  # mg
Gr_mass_12 = 5.77 * area  # mg

# Mass factors for normalization to % mass remaining
LFP_mass_factor = 20.16
Gr_mass_factor = 11.4
```

### 셀 8 — 시트 · 셀 이름표 (11 셀)

```python
# Create a dictionary to hold the data for each case
LFP_Models = {case: [] for case in case_selection.keys()}


# list of sheets and list of cell ID for each sheet
sheets = ['15-LFP 16-Gr Full-cell @ C_20',
          '15-LFP 16-Gr SOC-10',
          '15-LFP 16-Gr SOC-20',
          '12-LFP 16-Gr SOC-100',
          '15-LFP 12-Gr Full-cell @ C_20',
          'Full cell after FM SOC 0',
          'Full cell after FM SOC 10',
          '15-LFP 12-Gr SOC-10',
          '15-LFP 12-Gr SOC-20',
          '12-LFP 12-Gr SOC-10',
          '12-LFP 12-Gr SOC-20',
          ]

cell_idx = [1,0,0,0,0,0,1,1,1,0,0]

step_idx = [6,6,6,7,6,0,0,6,6,6,6]

selections = ['Fresh',
            'LLI-1',
            'LLI-2',
            'LAM$_\mathrm{PE}$-1',
            'LAM$_\mathrm{NE}$-1',
            'LAM$_\mathrm{PE,LLI}$-1',
            'LAM$_\mathrm{PE,LLI}$-2',
            'LAM$_\mathrm{NE,LLI}$-1',
            'LAM$_\mathrm{NE,LLI}$-2',
            'All mode-1',
            'All mode-2',]


for i, sheet in enumerate(sheets):
    data_dict = visualize_LFP_data(data_file=data_file,
                                   sheet_name=sheet,
                                      step_idx=step_idx[i],
                                      visualize=False)
    data_extract=extract_battery_data(data=data_dict,
                                                   idx=cell_idx[i],
                                                   )
    for case in LFP_Models.keys():
        LFP_Models[case].append(data_extract)

    
```

### 셀 9 — 건강 매개변수 참값 (`theoretical`)

```python
# Theoretical values of HPs
theoretical = [[1,1,1],
                        [1,1,0.9],
                        [1,1,0.8],
                        [0.64,1,1],
                        [1,0.56,1],
                        [0.64,1,0.64],
                        [0.64,1,0.58],
                        [1,0.56,0.9],
                        [1,0.56,0.8],
                        [0.64,0.56,0.58],
                        [0.64,0.56,0.51],
                        ]
                        
```

## `util_LFP.py` 발췌 원문

### 157–236 줄 — `objective_fun` (목적 함수 넷)

```python
def objective_fun(x, Model, halfcell):

    Q_exp = Model['Q_exp_interp']
    dVdQ_exp = Model['dVdQ_exp_interp']
    V_exp = Model['V_exp_interp']
    
    # Load half-cell data
    q_PE_hc = halfcell[0]
    V_PE_hc = halfcell[1]
    q_NE_hc = halfcell[2]
    V_NE_hc = halfcell[3]
    
    # Extract parameters
    m_P, m_N, d_P, d_N = x
    
    # Get half-cell VQ and dVdQ curves (function to be implemented separately)
    Q_PE_hc_ad, Q_NE_hc_ad, dVdQ_PE_hc, dVdQ_NE_hc, VPE_hc_sim, VNE_hc_sim, dQdV_PE_hc, dQdV_NE_hc = dVdQ_hc(
        V_PE_hc, q_PE_hc, V_NE_hc, q_NE_hc, m_P, m_N, d_P, d_N, interp_len=500
    )
    
    # Find indices where Q is closest to zero
    Q0P_ID = np.argmin(np.abs(Q_PE_hc_ad))
    Q0N_ID = np.argmin(np.abs(Q_NE_hc_ad))
    QmaxP_ID = np.argmax(Q_PE_hc_ad)
    QmaxN_ID = np.argmax(Q_NE_hc_ad)
    
    # Interpolate using experimental data
    VPE_interp = interp1d(Q_PE_hc_ad[Q0P_ID:QmaxP_ID], VPE_hc_sim[Q0P_ID:QmaxP_ID], fill_value='extrapolate')
    VNE_interp = interp1d(Q_NE_hc_ad[Q0N_ID:QmaxN_ID], VNE_hc_sim[Q0N_ID:QmaxN_ID], fill_value=(1.5,0.01), bounds_error=False)
    
    VPE_sim = VPE_interp(Q_exp)
    VNE_sim = VNE_interp(Q_exp)
    Vf_sim = VPE_sim - VNE_sim
    Model['Vf_sim'] = Vf_sim
    
    # Capacity estimation
    Q_sim = np.linspace(0, Q_PE_hc_ad[QmaxP_ID], 250)
    VPE_sim_4Cap = VPE_interp(Q_sim)
    VNE_sim_4Cap = VNE_interp(Q_sim)
    Vf_sim_4Cap = VPE_sim_4Cap - VNE_sim_4Cap
    
    Vexp_max, Vexp_min = 3.6, 2
    
    Vmin_ID = np.argmin(np.abs(Vf_sim_4Cap - Vexp_min))
    Vmax_ID = np.argmin(np.abs(Vf_sim_4Cap - Vexp_max))
    
    Model['Q_sim'] = Q_sim[Vmin_ID:Vmax_ID]
    Model['Vf_sim_4Cap'] = Vf_sim_4Cap[Vmin_ID:Vmax_ID]
    Model['Q_sim_max'] = np.max(Model['Q_sim'])
    
    # Calculate dV/dQ
    unique_Q, unique_indices = np.unique(Q_exp, return_index=True)
    dVdQ_sim = np.diff(Vf_sim[unique_indices]) / np.diff(unique_Q)
    dVdQ_sim = np.append(dVdQ_sim, dVdQ_sim[-1])
    Model['dVdQ_sim'] = dVdQ_sim
    
    # Compute errors
    # QV end-point error
    f1 = (np.mean((np.max(Vf_sim) - np.max(V_exp)) ** 2)) + np.sqrt(np.mean((np.min(Vf_sim) - np.min(V_exp)) ** 2))/2
    # QV curve error
    f2 = np.mean((Vf_sim - V_exp) ** 2)
    # dVdQ peak error (identify the two peaks)
    try:
        # First peak location
        peak_loc_exp = find_peaks(dVdQ_exp,distance=20,prominence=0.05)[0][0] # Returns a scalar value
        peak_loc_sim = find_peaks(dVdQ_sim,distance=20,prominence=0.05)[0][0] # Returns a scalar value

        f3 = np.mean((Q_exp[peak_loc_sim] - Q_exp[peak_loc_exp]) ** 2) # peak location error
        # peak magnitude error of a range of 16 points, also only look at the peak region of experiment
        f3 += np.mean((dVdQ_sim[peak_loc_exp-8:peak_loc_exp+8] - 
                               dVdQ_exp[peak_loc_exp-8:peak_loc_exp+8])**2) 
    except:
        f3 = 1
    
    # dVdQ curve error
    # Only consider the range where experimental dV/dQ is above a threshold to avoid noise-dominated regions
    dVdQ_clean_range = dVdQ_exp < 0.4 # Adjust threshold as needed
    f4 = np.mean((dVdQ_sim[dVdQ_clean_range] - dVdQ_exp[dVdQ_clean_range]) ** 2)

    return np.array([f1, f2, f3, f4])
```

### 703–729 줄 — `extract_health_parameter` (m_P · m_N · LII)

```python
def extract_health_parameter(nsga_result,halfcell):
    '''
    Extracts health parameters from the optimization result.

    Args:
        nsga_result: The result of the NSGA optimization.
        halfcell: The half-cell data used in the optimization.

    Returns:
        health_params: A numpy array containing the three health parameters.
    '''
    # Extract the half-cell parameters from the optimization result
    X = nsga_result.X

    # Calculate the maximum PE capacity
    q_PE_hc = halfcell[0].flatten()
    max_q = np.max(q_PE_hc)
    Q_max = X[:, 0] * max_q

    # Calculate the LII
    d_P = X[:, 2]
    d_N = X[:, 3]
    LII = (Q_max - (d_P - d_N))/max_q

    # Output the health parameters
    health_params = np.concatenate((X[:,:2], LII.reshape(-1, 1)), axis=1)
    return health_params
```

### `LICENSE` 원문

```
MIT License

Copyright (c) 2026 REIL-UConn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

(해석은 raw 가 아니라 위키 페이지 `entities/isu-uconn-lfp-gr-emulated-degradation.md` 에 둔다.)
