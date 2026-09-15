"""Raw-file ingestion regression tests: encodings, CC/CV detection, manifests and the CLI contract."""
from pathlib import Path
from tempfile import TemporaryDirectory
import contextlib
import io
import json
import re
import sys
import unittest

PACKAGE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PACKAGE))
import numpy as np
import pandas as pd
from config import Config,DataError,config_dict
from demo import make_demo
from extract_capacity import (CYCLE_COLUMNS,EIS_COLUMNS,build_features,convert_mpt,find_cv_start,
                              load_raw,main,read_csv_any,read_cycle,read_table,validate_frame)

UNITS_ROW='s\ts\tindex\tindex\tAh\tV\tA'
REST=[0,0,1,10,0,3.7,0]

def small_config(**changes):
    values=dict(frequency_grid_hz=[.1,1.,10.,1000.,10000.,100000.],feature_sets=['single_1e3'],
                ridge_alphas=[.1,10.],logistic_cs=[.1,1.],inner_splits=2,use_ocv=False)
    values.update(changes)
    return Config(**values).validate()

def charge_rows(currents,voltages=None,step=20,start=1,scale=.5):
    capacities=list(np.cumsum(np.asarray(currents,dtype=float))*scale)
    voltages=voltages or [4.]*len(currents)
    return [[start+i,i,1,step,capacities[i],voltages[i],currents[i]] for i in range(len(currents))]

def write_cycle(path,rows,units_row=UNITS_ROW,trailing_tab=False,header='metadata'):
    text=f'{header}\n'+'\t'.join(CYCLE_COLUMNS)+'\n'+(f'{units_row}\n' if units_row else '')
    text+=''.join('\t'.join(map(str,row))+('\t' if trailing_tab else '')+'\n' for row in rows)
    path.write_text(text,encoding='utf-8')
    return path

def write_eis(path,frequencies,potentials=(3.7,),cycle_column=False,trailing_tab=False):
    columns=EIS_COLUMNS+['|Z|/Ohm','<Ewe>/V']+(['cycle number'] if cycle_column else [])
    lines=['EC-Lab ASCII FILE','\t'.join(columns)]
    for sweep,potential in enumerate(potentials):
        for f in frequencies:
            z=10+20/(1+1j*f/300)
            values=[f,z.real,-z.imag,abs(z),potential]+([sweep+1] if cycle_column else [])
            lines.append('\t'.join(f'{v:.12g}' for v in values)+('\t' if trailing_tab else ''))
    path.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return path

class ExtractCase(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory(prefix='extract_tests_')
        self.folder=Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def pair(self,cfg,cell=41,currents=(.01,.01,.005,.002)):
        cycle=self.folder/'cycle'; eis=self.folder/'eis'
        cycle.mkdir(exist_ok=True); eis.mkdir(exist_ok=True)
        write_cycle(cycle/f'cell{cell}.txt',[REST]+charge_rows(list(currents)))
        write_eis(eis/f'cell{cell}.mpt',cfg.frequency_grid_hz)
        return cycle,eis

class DetectionTests(ExtractCase):
    def test_f06_overshoot_noise_and_ramp_do_not_move_the_transition(self):
        cases={'overshoot':[.0102]+[.01]*7+[.006,.004,.002],
               'ripple':[.01,.0099,.0092,.0101,.01,.01,.0098,.01,.006,.004,.002],
               'ramp_up':[.004,.008,.01,.01,.01,.01,.01,.01,.006,.003,.001]}
        for label,currents in cases.items():
            with self.subTest(case=label):
                path=write_cycle(self.folder/f'cell41_{label}.txt',[REST]+charge_rows(currents))
                result,detail=read_cycle(path,small_config())
                self.assertEqual(detail['cv_first_below_index'],8)
                self.assertAlmostEqual(detail['cc_reference_current_a'],.01)
                self.assertGreater(result['cc_frac'],.6)

    def test_f06_single_sample_reference_is_what_used_to_fail(self):
        frame=pd.DataFrame({'current':[.0102]+[.01]*7+[.006,.004,.002]})
        self.assertEqual(find_cv_start(frame,.01,1,1),1)
        self.assertEqual(find_cv_start(frame),8)
        noisy=pd.DataFrame({'current':[.01,.0099,.0092,.0101,.01,.01,.0098,.01,.006,.004,.002]})
        self.assertEqual(find_cv_start(noisy,.01,1,1),2)
        self.assertEqual(find_cv_start(noisy),8)

    def test_f06_short_segment_keeps_the_documented_transition(self):
        result,detail=read_cycle(write_cycle(self.folder/'cell41.txt',[REST]+charge_rows([.01,.01,.005,.002])),
                                 small_config())
        self.assertEqual(detail['cv_first_below_index'],2)
        self.assertAlmostEqual(result['cap_cc'],.0125)

    def test_f06_implausible_cc_fraction_is_reported(self):
        path=write_cycle(self.folder/'cell41.txt',[REST]+charge_rows([.0102]+[.01]*11))
        result,detail=read_cycle(path,small_config(cc_reference_rows=1,cc_sustained_rows=1))
        self.assertLess(result['cc_frac'],.2)
        self.assertTrue(any('implausibly low' in message for message in detail['warnings']))
        plateau,detail=read_cycle(path,small_config())
        self.assertAlmostEqual(plateau['cc_frac'],1.)
        self.assertEqual(detail['warnings'],[])

    def test_f33_charge_continuing_in_the_next_step_is_flagged(self):
        rows=[REST]+charge_rows([.01,.01,.01],voltages=[4.,4.1,4.2])+ \
             charge_rows([.008,.004,.002],voltages=[4.2,4.2,4.2],step=21,start=4)
        result,detail=read_cycle(write_cycle(self.folder/'cell41.txt',rows),small_config())
        self.assertTrue(detail['next_segment_continues_charge'])
        self.assertTrue(any('separate Step No.' in message for message in detail['warnings']))
        self.assertAlmostEqual(result['cc_frac'],1.)

    def test_f33_discharge_after_charge_is_not_flagged(self):
        rows=[REST]+charge_rows([.01,.01,.005,.002])+[[9,0,1,30,.03,4.1,-.01]]
        _,detail=read_cycle(write_cycle(self.folder/'cell41.txt',rows),small_config())
        self.assertNotIn('next_segment_continues_charge',detail)
        self.assertEqual(detail['warnings'],[])

    def test_f63_boundary_zero_current_rows_stay_an_explicit_choice(self):
        path=write_cycle(self.folder/'cell41.txt',[REST]+charge_rows([0,.01,.01,.005,.002]))
        with self.assertRaisesRegex(DataError,'current sign/zero'):
            read_cycle(path,small_config())
        result,detail=read_cycle(path,small_config(trim_zero_current_boundary_rows=True))
        self.assertEqual(detail['segment_rows'],4)
        self.assertEqual(len(detail['boundary_zero_current_rows_removed']),1)
        self.assertAlmostEqual(result['cap'],.0135)
        self.assertEqual(detail['cv_first_below_index'],2)

class ReaderTests(ExtractCase):
    def test_f20_other_cycles_cannot_reject_a_complete_target_cycle(self):
        rows=[REST]+charge_rows([.01,.01,.005,.002])+[[0,0,2,40,'','',.01],[1,1,2,40,'',3.9,.01]]
        result,_=read_cycle(write_cycle(self.folder/'cell41.txt',rows),small_config())
        self.assertAlmostEqual(result['cap'],.0135)

    def test_f20_missing_value_inside_the_target_cycle_names_row_and_column(self):
        rows=[REST]+charge_rows([.01,.01,.005,.002])
        rows[2][4]=''
        with self.assertRaisesRegex(DataError,r"\|Q\|\(Ah\)="):
            read_cycle(write_cycle(self.folder/'cell41.txt',rows),small_config())

    def test_f55_units_and_locale_variants_are_named(self):
        rows=[REST]+charge_rows([.01,.01,.005,.002])
        with self.assertRaisesRegex(DataError,'units row'):
            read_cycle(write_cycle(self.folder/'cell41_units.txt',rows,units_row='s\ts\tindex\tindex\tmAh\tV\tmA'),
                       small_config())
        comma=[list(row) for row in rows]; comma[2][4]='0,015'
        with self.assertRaisesRegex(DataError,'decimal comma'):
            read_cycle(write_cycle(self.folder/'cell41_comma.txt',comma),small_config())
        clock=[list(row) for row in rows]; clock[2][0]='0:00:05'
        with self.assertRaisesRegex(DataError,'seconds'):
            read_cycle(write_cycle(self.folder/'cell41_clock.txt',clock),small_config())

    def test_f25_trailing_tabs_on_data_rows_keep_columns_aligned(self):
        cfg=small_config()
        spec,_=convert_mpt(write_eis(self.folder/'cell41.mpt',[1.,10.,100.],trailing_tab=True),cfg)
        np.testing.assert_allclose(spec['f'].to_numpy(),[1.,10.,100.])
        rows=[REST]+charge_rows([.01,.01,.005,.002])
        result,_=read_cycle(write_cycle(self.folder/'cell41.txt',rows,units_row=UNITS_ROW+'\t',
                                        trailing_tab=True),cfg)
        self.assertAlmostEqual(result['cap'],.0135)
        with self.assertRaisesRegex(DataError,'inconsistent tab-separated rows'):
            read_cycle(write_cycle(self.folder/'cell42.txt',rows,trailing_tab=True),cfg)

    def test_f32_cp1252_eclab_header_is_decoded(self):
        self.assertIn('cp1252',Config().encodings)
        table='\t'.join(EIS_COLUMNS)+'\n'+'\n'.join(f'{f}\t10\t-5' for f in [1.,10.,100.])+'\n'
        header='EC-Lab ASCII FILE\nElectrode surface area : 3.24 cm²\nTemperature : 25 °C\n'
        path=self.folder/'cell41.mpt'; path.write_bytes((header+table).encode('cp1252'))
        _,info=read_table(path,EIS_COLUMNS,small_config())
        self.assertEqual(info['encoding'],'cp1252')

    def test_f32_cp949_mojibake_in_an_eclab_header_is_flagged(self):
        table=('\t'.join(EIS_COLUMNS)+'\n'+'\n'.join(f'{f}\t10\t-5' for f in [1.,10.,100.])+'\n').encode('ascii')
        path=self.folder/'cell42.mpt'; path.write_bytes(b'EC-Lab ASCII FILE\nCs/\xb5F\n'+table)
        _,info=read_table(path,EIS_COLUMNS,small_config())
        self.assertEqual(info['encoding'],'cp949')
        self.assertTrue(any('Hangul' in message for message in info['warnings']))

    def test_f32_undecodable_file_names_the_remedy(self):
        path=self.folder/'cell43.mpt'; path.write_bytes(b'EC-Lab\n\x81\x30\n')
        with self.assertRaisesRegex(DataError,'cp1252'):
            read_table(path,EIS_COLUMNS,small_config(encodings=['utf-8-sig','cp949']))

class SpectrumTests(ExtractCase):
    def test_f19_stacked_sweeps_are_counted_and_selectable(self):
        cfg=small_config()
        path=write_eis(self.folder/'cell41.mpt',cfg.frequency_grid_hz,potentials=(3.7,3.9),cycle_column=True)
        spec,info=convert_mpt(path,cfg)
        self.assertEqual(info['eis_sweeps'],2)
        self.assertTrue(any('eis_sweep' in message for message in info['warnings']))
        with self.assertRaisesRegex(DataError,'eis_sweep'):
            build_features(spec,cfg)
        last,info=convert_mpt(path,small_config(eis_sweep='last'))
        self.assertEqual((info['selected_sweep'],info['raw_rows']),(1,len(cfg.frequency_grid_hz)))
        self.assertAlmostEqual(float(last['ocv'].median()),3.9)
        first,_=convert_mpt(path,small_config(eis_sweep='first'))
        self.assertAlmostEqual(float(first['ocv'].median()),3.7)
        features,_=build_features(last,cfg)
        self.assertTrue(np.isfinite(list(features.values())).all())
        with self.assertRaisesRegex(DataError,'outside the 2 sweeps'):
            convert_mpt(path,small_config(eis_sweep=5))

    def test_f19_sweeps_without_a_cycle_column_are_found_by_repeated_frequencies(self):
        cfg=small_config()
        path=write_eis(self.folder/'cell41.mpt',cfg.frequency_grid_hz,potentials=(3.7,3.9))
        _,info=convert_mpt(path,cfg)
        self.assertEqual(info['eis_sweeps'],2)
        self.assertEqual(info['sweep_ocv_median_v'],[3.7,3.9])

    def test_f19_mean_policy_refuses_to_average_different_states_only_when_configured(self):
        cfg=small_config()
        path=write_eis(self.folder/'cell41.mpt',cfg.frequency_grid_hz,potentials=(3.7,3.9))
        spec,_=convert_mpt(path,cfg)
        averaging=small_config(duplicate_frequency_policy='mean')
        result,_=build_features(spec,averaging)
        self.assertTrue(np.isfinite(list(result.values())).all())
        strict=small_config(duplicate_frequency_policy='mean',mean_max_ewe_spread_v=.005)
        with self.assertRaisesRegex(DataError,'not physical'):
            build_features(spec,strict)

    def test_f34_boundary_error_reports_the_relative_shortfall(self):
        cfg=small_config(frequency_grid_hz=[1.,10.,1000.])
        spec=pd.DataFrame({'f':[1.04,990.],'re':[4.,9.],'im':[0.,0.]})
        with self.assertRaisesRegex(DataError,'relative') as caught:
            build_features(spec,cfg)
        self.assertIn('clamp',str(caught.exception))

class FrameTests(ExtractCase):
    def test_f12_uppercase_feature_names_are_rejected_not_ignored(self):
        cfg=small_config(); data=make_demo(cfg,8).rename(columns={'mag@1000Hz':'Mag@1000Hz'})
        with self.assertRaisesRegex(DataError,'Use canonical feature name mag@1000Hz'):
            validate_frame(data,cfg,[])
        upper=make_demo(cfg,8).rename(columns={'re@1000Hz':'Re@1000Hz','im@1000Hz':'Im@1000Hz'})
        with self.assertRaisesRegex(DataError,'Use canonical feature name re@1000Hz'):
            validate_frame(upper,cfg,[])

    def test_f12_unused_columns_are_recorded(self):
        cfg=small_config(); data=make_demo(cfg,8); data['operator_note']='remeasured'
        events=[]; validate_frame(data,cfg,events)
        self.assertTrue(any(e.get('status')=='ignored_columns' and e['columns']==['operator_note'] for e in events))

    def test_f27_milliampere_hour_capacity_is_rejected(self):
        cfg=small_config(); data=make_demo(cfg,8); data['cap']*=1000
        with self.assertRaisesRegex(DataError,'cap must be in Ah'):
            validate_frame(data,cfg,[])

    def test_f27_capacity_above_the_design_value_is_flagged(self):
        cfg=small_config(); data=make_demo(cfg,8); data.loc[0,'cap']=2*cfg.design_capacity_ah
        events=[]; clean,_=validate_frame(data,cfg,events)
        self.assertEqual(len(clean),8)
        self.assertTrue(any(e.get('status')=='warning' and 'design_capacity_ah' in e['reason'] for e in events))

    def test_f56_full_exclusion_names_the_configured_range(self):
        cfg=small_config(cell_min=1,cell_max=5); data=make_demo(cfg,8)
        with self.assertRaisesRegex(DataError,re.escape('cell_min=1, cell_max=5')) as caught:
            validate_frame(data,cfg,[])
        self.assertIn('41..48',str(caught.exception))

class ManifestTests(ExtractCase):
    def test_f13_cp949_manifest_with_korean_text_is_read(self):
        cfg=small_config(); cycle,eis=self.pair(cfg)
        manifest=self.folder/'selection.csv'
        record=[{'cell_number':41,'cycle_file':'cell41.txt','eis_file':'cell41.mpt',
                 'batch_id':'1차','selection_reason':'재측정'}]
        manifest.write_bytes(pd.DataFrame(record).to_csv(index=False).encode('cp949'))
        events=[]
        frame=load_raw(cycle,eis,cfg,events,manifest)
        self.assertEqual(frame['batch_id'].tolist(),['1차'])
        self.assertTrue(any(e.get('status')=='selection_manifest' and e['encoding']=='cp949' for e in events))

    def test_f13_spreadsheets_and_undecodable_csv_name_the_remedy(self):
        cfg=small_config()
        book=self.folder/'selection.xlsx'; book.write_bytes(b'PK\x03\x04')
        with self.assertRaisesRegex(DataError,'CSV UTF-8'):
            read_csv_any(book,cfg)
        broken=self.folder/'selection.csv'; broken.write_bytes(b'cell_number\n\x81\x30\n')
        with self.assertRaisesRegex(DataError,'CSV UTF-8'):
            read_csv_any(broken,cfg)

    def test_f48_manifest_values_are_validated_as_input_errors(self):
        cfg=small_config(); cycle,eis=self.pair(cfg)
        base={'cell_number':'41','cycle_file':'cell41.txt','eis_file':'cell41.mpt'}
        def manifest(name,**changes):
            path=self.folder/name
            pd.DataFrame([{**base,**changes}]).to_csv(path,index=False)
            return path
        with self.assertRaisesRegex(DataError,'cycle_file is empty'):
            load_raw(cycle,eis,cfg,[],manifest('empty.csv',cycle_file=''))
        for value in ['','41.5','cell41']:
            with self.subTest(cell_number=value),self.assertRaisesRegex(DataError,'must be an integer'):
                load_raw(cycle,eis,cfg,[],manifest(f'bad_{value or "blank"}.csv',cell_number=value))
        frame=load_raw(cycle,eis,cfg,[],manifest('excel.csv',cell_number='41.0'))
        self.assertEqual(frame['cell_number'].tolist(),[41])

    def test_f41_excluded_cell_is_recorded_once(self):
        cfg=small_config(exclude_cells={'60':'predeclared measurement QC'})
        cycle,eis=self.pair(cfg)
        (cycle/'cell60.txt').write_text('invalid',encoding='utf-8')
        (eis/'cell60.mpt').write_text('invalid',encoding='utf-8')
        events=[]
        frame=load_raw(cycle,eis,cfg,events,None)
        self.assertEqual(frame['cell_number'].tolist(),[41])
        self.assertEqual(sum(1 for e in events if e.get('cell_number')==60 and e['status']=='excluded'),1)

    def test_f19_non_eis_technique_file_does_not_force_a_manifest(self):
        cfg=small_config(); cycle,eis=self.pair(cfg)
        (eis/'cell41_01_OCV.mpt').write_text('EC-Lab ASCII FILE\nmode\ttime/s\tEwe/V\n1\t0\t3.7\n',encoding='utf-8')
        events=[]
        frame=load_raw(cycle,eis,cfg,events,None)
        self.assertEqual(frame['cell_number'].tolist(),[41])
        self.assertTrue(any(e.get('status')=='skipped_non_eis_file' for e in events))

class ConfigTests(ExtractCase):
    def test_f38_non_text_codecs_and_malformed_exclusions_are_data_errors(self):
        with self.assertRaisesRegex(DataError,'not a text encoding'):
            small_config(encodings=['zlib'])
        with self.assertRaisesRegex(DataError,'Unknown text encoding'):
            small_config(encodings=['definitely-not-a-codec'])
        for keys in [{'cell60':'QC'},{'60.0':'QC'},{'060':'QC'},{'60':''}]:
            with self.subTest(exclude_cells=keys),self.assertRaisesRegex(DataError,'exclude_cells'):
                small_config(exclude_cells=keys)

    def test_f47_configuration_errors_name_the_key_and_value(self):
        expectations=[({'max_boundary_fraction':.2},'max_boundary_fraction=0.2'),
                      ({'cv_relative_drop':0.},'cv_relative_drop=0.0'),
                      ({'inner_splits':1},'inner_splits=1'),
                      ({'cell_min':99},'cell_min=99'),
                      ({'boundary_policy':'skip'},"boundary_policy='skip'"),
                      ({'use_ocv':'false'},"use_ocv='false'"),
                      ({'eis_sweep':'middle'},"eis_sweep='middle'"),
                      ({'cap_plausibility_factor':1.},'cap_plausibility_factor=1.0')]
        for setting,expected in expectations:
            with self.subTest(setting=setting),self.assertRaisesRegex(DataError,re.escape(expected)):
                small_config(**setting)

    def test_new_settings_keep_the_previous_reader_behaviour(self):
        cfg=Config().validate()
        self.assertEqual((cfg.eis_sweep,cfg.mean_max_ewe_spread_v,cfg.trim_zero_current_boundary_rows),
                         ('all',None,False))
        self.assertEqual((cfg.cc_reference_rows,cfg.cc_sustained_rows,cfg.cap_plausibility_factor),(5,3,10.))

class CommandTests(ExtractCase):
    def run_cli(self,arguments):
        stderr=io.StringIO()
        with contextlib.redirect_stderr(stderr),contextlib.redirect_stdout(io.StringIO()):
            try:
                code=main(arguments)
            except SystemExit as exit_code:
                code=exit_code.code
        return code,stderr.getvalue()

    def test_f08_configuration_errors_exit_two_with_an_audit(self):
        cfg=small_config(); _,eis=self.pair(cfg)
        output=self.folder/'prepared.csv'
        code,stderr=self.run_cli(['--eis-dir',str(eis),'--output',str(output),
                                  '--config',str(self.folder/'missing.json')])
        self.assertEqual(code,2)
        self.assertIn('Input error',stderr)
        self.assertFalse(output.exists())
        record=json.loads(output.with_suffix('.audit.json').read_text(encoding='utf-8'))
        self.assertEqual((record['status'],record['error_type']),('failed','FileNotFoundError'))

    def test_f08_malformed_configuration_json_exits_two(self):
        cfg=small_config(); _,eis=self.pair(cfg)
        config=self.folder/'config.json'; config.write_text('{"seed": }',encoding='utf-8')
        code,stderr=self.run_cli(['--eis-dir',str(eis),'--output',str(self.folder/'a.csv'),'--config',str(config)])
        self.assertEqual(code,2)
        self.assertIn('Input error',stderr)
        config.write_text(json.dumps({'exclude_cells':{'cell60':'QC'}}),encoding='utf-8')
        code,_=self.run_cli(['--eis-dir',str(eis),'--output',str(self.folder/'b.csv'),'--config',str(config)])
        self.assertEqual(code,2)

    def test_f40_failed_run_keeps_file_hashes_in_the_audit(self):
        cfg=small_config(); cycle,eis=self.pair(cfg)
        (eis/'cell41.mpt').write_text('invalid',encoding='utf-8')
        config=self.folder/'config.json'; config.write_text(json.dumps(config_dict(cfg)),encoding='utf-8')
        output=self.folder/'prepared.csv'
        code,stderr=self.run_cli(['--cycle-dir',str(cycle),'--eis-dir',str(eis),'--output',str(output),
                                  '--config',str(config)])
        self.assertEqual(code,2)
        self.assertIn('Cell 41',stderr)
        record=json.loads(output.with_suffix('.audit.json').read_text(encoding='utf-8'))
        self.assertEqual(record['status'],'failed')
        failed=[e for e in record['events'] if e.get('status')=='failed']
        self.assertEqual(len(failed[0]['eis_sha256']),64)
        self.assertEqual(record['config']['seed'],cfg.seed)

    def test_f40_successful_run_records_configuration_and_manifest(self):
        cfg=small_config(); cycle,eis=self.pair(cfg)
        manifest=self.folder/'selection.csv'
        pd.DataFrame([{'cell_number':41,'cycle_file':'cell41.txt','eis_file':'cell41.mpt'}]).to_csv(manifest,index=False)
        config=self.folder/'config.json'; config.write_text(json.dumps(config_dict(cfg)),encoding='utf-8')
        output=self.folder/'prepared.csv'
        code,_=self.run_cli(['--cycle-dir',str(cycle),'--eis-dir',str(eis),'--selection-manifest',str(manifest),
                             '--output',str(output),'--config',str(config)])
        self.assertEqual(code,0)
        record=json.loads(output.with_suffix('.audit.json').read_text(encoding='utf-8'))
        self.assertEqual((record['status'],record['cells']),('completed',1))
        self.assertEqual(len(record['selection_manifest']['sha256']),64)
        self.assertEqual(pd.read_csv(output)['cell_number'].tolist(),[41])

if __name__=='__main__':
    unittest.main(verbosity=2)
