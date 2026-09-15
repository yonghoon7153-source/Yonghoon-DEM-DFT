"""Value-level and mutation-resistant checks for the evaluation, prediction and reader paths."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import contextlib
import importlib.util
import io
import json
import sys
import unittest

PACKAGE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PACKAGE))
import joblib
import numpy as np
import pandas as pd
from openpyxl import load_workbook
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression,LogisticRegression,Ridge
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from config import Config,DataError,EvaluationError,VERSION,config_dict,digest,write_json
from demo import make_demo
from extract_capacity import CYCLE_COLUMNS,build_features,included,load_raw,read_cycle,validate_frame
from extract_capacity import main as extract_main
from export_for_origin import outcome,run,write_workbook
from export_for_origin import main as export_main
from predict import predict_frame
from predict import main as predict_main
from ridge_capacity import (FeatureSelector,band_columns,classification_metrics,fixed_baselines,
                            nested_evaluate,regression_metrics,select_model)

FITTERS=[StandardScaler,Ridge,LinearRegression,LogisticRegression,DummyRegressor,FeatureSelector,Pipeline]
INNER_METRIC_SCORING={'negative_MSE':'neg_mean_squared_error','negative_log_loss':'neg_log_loss'}

def small_config(**changes):
    values=dict(frequency_grid_hz=[.1,1.,10.,1000.,10000.,100000.],
                feature_sets=['single_1e3'],ridge_alphas=[.1,10.],logistic_cs=[.1,1.],
                inner_splits=2,use_ocv=False)
    values.update(changes)
    return Config(**values).validate()

def cycle_text(rows,metadata=('metadata',)):
    text=''.join(line+'\n' for line in metadata)+'\t'.join(CYCLE_COLUMNS)+'\n'+'s\ts\tindex\tindex\tAh\tV\tA\n'
    return text+''.join('\t'.join(map(str,row))+'\n' for row in rows)

def eis_file(path,cfg):
    rows=['freq/Hz\tRe(Z)/Ohm\t-Im(Z)/Ohm\t|Z|/Ohm\tPhase(Z)/deg\t<Ewe>/V']
    for f in cfg.frequency_grid_hz:
        z=10+20/(1+1j*f/300)
        rows.append(f'{f}\t{z.real}\t{-z.imag}\t{abs(z)}\t{np.angle(z,deg=True)}\t3.7')
    path.write_text('EC-Lab ASCII FILE\n'+'\n'.join(rows)+'\n',encoding='ascii')
    return path

def spectrum_columns(cfg,real,imaginary):
    columns={}
    for index,f in enumerate(cfg.frequency_grid_hz):
        a=real(index); b=imaginary(index)
        columns.update({f're@{f:g}Hz':a,f'im@{f:g}Hz':b,f'mag@{f:g}Hz':np.hypot(a,b),
                        f'phase@{f:g}Hz':np.degrees(np.arctan2(b,a))})
    return columns

def multivariate_frame(cfg,n=12,seed=11):
    """cap depends on one latent factor that every single column hides behind a large nuisance factor.

    Any two columns recorded at the same frequency cancel the nuisance, so a multi-column
    regularized fit must beat the single-feature baselines; no univariate model can.
    """
    rng=np.random.default_rng(seed)
    signal=rng.normal(0,1,n); nuisance=rng.normal(0,3,n)
    columns=spectrum_columns(cfg,lambda i:8+signal+(.4+.35*i)*nuisance+rng.normal(0,.05,n),
                             lambda i:-(3+signal-(.4+.35*i)*nuisance+rng.normal(0,.05,n)))
    return pd.DataFrame({'cell_number':np.arange(41,41+n),
                         'batch_id':[f'demo_batch_{i%3+1}' for i in range(n)],
                         'cap':.018+.0015*signal+rng.normal(0,.00005,n),
                         'cc_frac':.8+.02*rng.normal(0,1,n),'ocv':3.7+.002*rng.normal(0,1,n),**columns})

def null_frame(cfg,n=40,seed=5):
    """No relationship at all between features and targets; honest scores must sit at chance."""
    rng=np.random.default_rng(seed)
    columns=spectrum_columns(cfg,lambda i:10+rng.normal(0,1,n),lambda i:-(2+rng.normal(0,1,n)))
    frame=pd.DataFrame({'cell_number':np.arange(41,41+n),'cap':.018+.0015*rng.normal(0,1,n),**columns})
    frame['label']=rng.permutation(np.array([0,1]*(n//2)))
    return frame

def recording_search(record):
    """GridSearchCV that reports the splits and scoring it actually received, not the run's own trace."""
    class Recording(GridSearchCV):
        def fit(self,X,y=None,**kwargs):
            record.append({'search':self,'X':X,'cv':self.cv,'scoring':self.scoring})
            return super().fit(X,y,**kwargs)
    return Recording

def recorded_splits(entry):
    cv=entry['cv']
    return list(cv) if isinstance(cv,(list,tuple)) else list(cv.split(entry['X']))


class TemporaryCase(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory(prefix='ml_validation_')
        self.addCleanup(self.tmp.cleanup)
        self.folder=Path(self.tmp.name).resolve()


class SelectionTests(unittest.TestCase):
    def test_regularized_multifeature_model_is_selected_when_no_single_column_predicts(self):
        cfg=small_config(frequency_grid_hz=[1.,10.,1000.,10000.],feature_sets=['single_1e3','band_1e3_1e5','band_low','full'],
                         ridge_alphas=[.01,1.,100.],use_ocv=True,inner_splits=2)
        clean,features=validate_frame(multivariate_frame(cfg),cfg,[])
        pred,folds=nested_evaluate(clean[features],clean['cap'].to_numpy(),clean['cell_number'].to_numpy(),cfg)
        chosen=[fold['selected'] for fold in folds]
        self.assertTrue(any(s['estimator']=='Ridge' for s in chosen),[s['estimator'] for s in chosen])
        for s in chosen:
            if s['estimator']=='Ridge':
                self.assertIn(s['alpha'],cfg.ridge_alphas)
                self.assertGreater(len(s['features']),1)
        # The nested selection must also beat every fixed single-feature baseline on this fixture.
        nested=regression_metrics(clean['cap'].to_numpy(),pred)['Q2']
        for name,_,metrics in fixed_baselines(clean[features],clean['cap'].to_numpy(),clean['cell_number'].to_numpy(),cfg):
            self.assertGreater(nested,metrics['Q2'],name)

    def test_no_signal_data_scores_at_chance_instead_of_inventing_skill(self):
        cfg=small_config(frequency_grid_hz=[1.,10.,1000.],feature_sets=['band_low'],inner_splits=3,logistic_cs=[.01,.1])
        frame=null_frame(cfg)
        clean,features=validate_frame(frame,cfg,[])
        X=clean[features]; ids=clean['cell_number'].to_numpy()
        pred,_=nested_evaluate(X,clean['cap'].to_numpy(),ids,cfg)
        self.assertLessEqual(regression_metrics(clean['cap'].to_numpy(),pred)['Q2'],.1)
        y=frame.set_index('cell_number').loc[ids,'label'].to_numpy()
        prob,_=nested_evaluate(X,y,ids,cfg,kind='classification')
        auc=classification_metrics(y,(prob>=cfg.decision_threshold).astype(int),prob)['AUC_pooled_OOF']
        self.assertGreaterEqual(auc,.25)
        self.assertLessEqual(auc,.75)

    def test_classification_scores_rank_defective_cells_above_normal_ones(self):
        cfg=small_config(); clean,features=validate_frame(make_demo(cfg,8),cfg,[])
        y=(clean['cap'].to_numpy()<=cfg.threshold_ah).astype(int)
        prob,_=nested_evaluate(clean[features],y,clean['cell_number'].to_numpy(),cfg,kind='classification')
        # A score reported for the wrong class would still be finite and still sum to a full confusion matrix.
        self.assertGreater(prob[y==1].mean(),prob[y==0].mean())
        metrics=classification_metrics(y,(prob>=cfg.decision_threshold).astype(int),prob)
        self.assertGreaterEqual(metrics['AUC_pooled_OOF'],.9)
        self.assertGreaterEqual(metrics['TP']+metrics['TN'],7)

    def test_band_columns_map_each_name_to_an_explicit_frequency_set(self):
        cfg=small_config(frequency_grid_hz=[.1,1.,10.,1000.,10000.,100000.],
                         feature_sets=['single_1e3','band_1e3_1e5','band_low','full'])
        X=pd.DataFrame(spectrum_columns(cfg,lambda i:np.ones(3),lambda i:-np.ones(3)))
        X['ocv']=3.7
        bands=dict(band_columns(X,cfg))
        def frequencies(columns):
            return {float(c.split('@')[1][:-2]) for c in columns}
        self.assertEqual(frequencies(bands['single_1e3']),{1000.})
        self.assertEqual(frequencies(bands['band_1e3_1e5']),{1000.,10000.,100000.})
        self.assertEqual(frequencies(bands['band_low']),{.1,1.,10.})
        self.assertEqual(frequencies(bands['full']),{.1,1.,10.,1000.,10000.,100000.})
        for name,expected in [('single_1e3',4),('band_1e3_1e5',12),('band_low',12),('full',24)]:
            self.assertEqual(len(bands[name]),expected,name)
            self.assertNotIn('ocv',bands[name])
        cfg.use_ocv=True
        with_potential=dict(band_columns(X,cfg))
        self.assertEqual(set(with_potential),{'single_1e3','single_1e3_ocv','band_1e3_1e5','band_1e3_1e5_ocv',
                                              'band_low','band_low_ocv','full','full_ocv'})
        self.assertEqual(with_potential['full_ocv'][-1],'ocv')

    def test_grid_search_receives_the_declared_inner_folds_and_scoring(self):
        cfg=small_config(); clean,features=validate_frame(make_demo(cfg,8),cfg,[])
        X=clean[features]; ids=clean['cell_number'].to_numpy()
        for kind,y in [('regression',clean['cap'].to_numpy()),
                       ('classification',(clean['cap'].to_numpy()<=cfg.threshold_ah).astype(int))]:
            record=[]
            with patch('ridge_capacity.GridSearchCV',recording_search(record)):
                _,trace=select_model(X,y,ids,cfg,kind)
            self.assertEqual(len(record),1)
            self.assertEqual(record[0]['scoring'],INNER_METRIC_SCORING[trace['inner_metric']],kind)
            splits=recorded_splits(record[0])
            self.assertEqual(len(splits),len(trace['inner_folds']),kind)
            for (train,validation),reported in zip(splits,trace['inner_folds']):
                self.assertEqual(sorted(ids[train].tolist()),sorted(reported['train_cells']),kind)
                self.assertEqual(sorted(ids[validation].tolist()),sorted(reported['validation_cells']),kind)
            if kind=='regression':
                alphas={p['model__alpha'] for p in record[0]['search'].cv_results_['params'] if 'model__alpha' in p}
                self.assertEqual(alphas,set(cfg.ridge_alphas))

    def test_inner_splits_keep_interleaved_batches_apart_in_the_actual_search(self):
        cfg=small_config(outer_cv='leave_one_group_out')
        clean,features=validate_frame(make_demo(cfg,12),cfg,[])
        # Batches that run with cell order let a group-blind KFold imitate GroupKFold; interleaving removes that.
        groups=np.array([f'demo_batch_{i%3+1}' for i in range(len(clean))])
        X=clean[features]; by_row=pd.Series(groups,index=X.index)
        record=[]
        with patch('ridge_capacity.GridSearchCV',recording_search(record)):
            nested_evaluate(X,clean['cap'].to_numpy(),clean['cell_number'].to_numpy(),cfg,groups=groups)
        self.assertEqual(len(record),3)
        for entry in record:
            rows=entry['X'].index
            splits=recorded_splits(entry)
            self.assertTrue(splits)
            for train,validation in splits:
                left=set(by_row.loc[rows[train]]); right=set(by_row.loc[rows[validation]])
                self.assertFalse(left&right,(left,right))
                self.assertTrue(left and right)

    def test_fixed_baselines_never_use_the_target_of_the_cell_they_predict(self):
        cfg=small_config(); clean,features=validate_frame(make_demo(cfg,8),cfg,[])
        X=clean[features]; y=clean['cap'].to_numpy(); ids=clean['cell_number'].to_numpy()
        before={name:pred for name,pred,_ in fixed_baselines(X,y,ids,cfg)}
        changed=y.copy(); changed[0]=10.
        after={name:pred for name,pred,_ in fixed_baselines(X,changed,ids,cfg)}
        self.assertEqual(set(before),set(after))
        for name in before:
            self.assertAlmostEqual(before[name][0],after[name][0],places=12,msg=name)

    def test_evaluation_refuses_too_few_cells_and_too_few_groups(self):
        cfg=small_config(); clean,features=validate_frame(make_demo(cfg,8),cfg,[])
        X=clean[features]; y=clean['cap'].to_numpy(); ids=clean['cell_number'].to_numpy()
        with self.assertRaisesRegex(EvaluationError,'At least 4 independent cells'):
            nested_evaluate(X.iloc[:3],y[:3],ids[:3],cfg)
        grouped=small_config(outer_cv='leave_one_group_out')
        with self.assertRaisesRegex(EvaluationError,'at least 3 groups'):
            nested_evaluate(X,y,ids,grouped,groups=np.array(['b1']*4+['b2']*4))


class MetricTests(unittest.TestCase):
    def test_regression_metrics_match_hand_computation(self):
        result=regression_metrics([1.,2.,3.,4.],[1.5,2.5,2.5,3.5])
        # residual = [-.5,-.5,.5,.5]; SSE = 1; SST = 5; MAPE = mean(.5, .25, 1/6, .125)
        self.assertEqual(result['n_samples'],4)
        self.assertAlmostEqual(result['Q2'],.8)
        self.assertAlmostEqual(result['RMSE'],.5)
        self.assertAlmostEqual(result['MAE'],.5)
        self.assertAlmostEqual(result['MAPE_pct'],100*(.5+.25+.5/3+.125)/4)
        self.assertIsNone(regression_metrics([2.,2.],[1.,3.])['Q2'])

    def test_classification_metrics_match_hand_computation(self):
        y=[1,1,0,0,1,0]; pred=[1,0,0,0,1,1]; score=[.9,.4,.1,.2,.8,.6]
        result=classification_metrics(y,pred,score)
        self.assertEqual([result['TP'],result['FN'],result['FP'],result['TN']],[2,1,1,2])
        self.assertEqual(result['n_samples'],6)
        for key in ['sensitivity','specificity','precision','accuracy','F1']:
            self.assertAlmostEqual(result[key],2/3,msg=key)
        self.assertAlmostEqual(result['MCC'],1/3)
        # 8 of the 9 positive/negative score pairs are ordered correctly.
        self.assertAlmostEqual(result['AUC_pooled_OOF'],8/9)

    def test_outcome_names_every_true_and_predicted_combination(self):
        # The demo fixture is separable, so only a direct check reaches the FN and FP branches.
        self.assertEqual(outcome(np.array([1,1,0,0]),np.array([1,0,1,0])).tolist(),['TP','FN','FP','TN'])


class ReaderTests(TemporaryCase):
    def test_cp949_cycle_file_reads_like_its_utf8_twin(self):
        cfg=small_config(encodings=['utf-8-sig','cp949'])
        text=cycle_text([[0,0,1,10,0,3.7,0],[1,0,1,20,.001,3.8,.01],[2,1,1,20,.015,4.,.01],
                         [3,2,1,20,.018,4.2,.005],[4,3,1,20,.02,4.2,.002]],
                        metadata=('셀 41 충방전 기록','시험 온도 25도'))
        korean=self.folder/'cell41_cp949.txt'; utf8=self.folder/'cell41_utf8.txt'
        korean.write_bytes(text.encode('cp949')); utf8.write_bytes(text.encode('utf-8-sig'))
        with self.assertRaises(UnicodeDecodeError):
            korean.read_bytes().decode('utf-8-sig')
        fallback,info=read_cycle(korean,cfg)
        direct,reference=read_cycle(utf8,cfg)
        self.assertEqual(info['encoding'],'cp949')
        self.assertEqual(reference['encoding'],'utf-8-sig')
        self.assertEqual(fallback,direct)
        self.assertAlmostEqual(fallback['cap'],.02)

    def test_clamping_still_refuses_frequencies_far_outside_the_measured_support(self):
        cfg=small_config(frequency_grid_hz=[1.,10.,1000.],boundary_policy='clamp',max_boundary_fraction=.05)
        spec=pd.DataFrame({'f':[2.,500.],'re':[4.,9.],'im':[0.,0.]})
        with self.assertRaisesRegex(DataError,'exceed measured support'):
            build_features(spec,cfg)

    def test_ambiguous_raw_step_is_refused(self):
        cfg=small_config(target_raw_step=20,target_step_i=0)
        rows=[[0,0,1,10,0,3.7,0],[1,0,1,20,.001,3.8,.01],[2,1,1,30,.01,4.,.01],[3,2,1,20,.018,4.2,.005]]
        path=self.folder/'cell41.txt'; path.write_text(cycle_text(rows),encoding='ascii')
        with self.assertRaisesRegex(DataError,'multiple segments'):
            read_cycle(path,cfg)

    def test_cell_range_boundaries_are_inclusive(self):
        cfg=small_config(cell_min=41,cell_max=43); events=[]
        self.assertEqual([included(c,cfg,events) for c in [40,41,42,43,44]],[False,True,True,True,False])
        self.assertEqual([e['cell_number'] for e in events],[40,44])
        # The reason names the configured range so a user can see which key excluded the cell.
        self.assertTrue(all(e['reason'].startswith('outside configured cell range') for e in events))
        self.assertTrue(all('41..43' in e['reason'] for e in events))

    def test_cycle_file_without_its_eis_partner_is_named(self):
        cfg=small_config(); cycle=self.folder/'cycle'; eis=self.folder/'eis'; cycle.mkdir(); eis.mkdir()
        rows=[[0,0,1,10,0,3.7,0],[1,0,1,20,.001,3.8,.01],[2,1,1,20,.015,4.,.01],
              [3,2,1,20,.018,4.2,.005],[4,3,1,20,.02,4.2,.002]]
        for cell in [41,42]:
            (cycle/f'cell{cell}.txt').write_text(cycle_text(rows),encoding='ascii')
        eis_file(eis/'cell41.mpt',cfg)
        with self.assertRaisesRegex(DataError,'Unmatched cells'):
            load_raw(cycle,eis,cfg,[])

    def test_extract_cli_prepares_eis_only_features_then_refuses_to_overwrite(self):
        cfg=small_config(); eis=self.folder/'eis'; eis.mkdir()
        for cell in [41,42,43]:
            eis_file(eis/f'cell{cell}.mpt',cfg)
        config=self.folder/'config.json'; config.write_text(json.dumps(config_dict(cfg)),encoding='utf-8')
        out=self.folder/'prepared.csv'
        arguments=['--config',str(config),'--eis-dir',str(eis),'--output',str(out)]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(extract_main(arguments),0)
        frame=pd.read_csv(out)
        self.assertEqual(frame['cell_number'].tolist(),[41,42,43])
        self.assertNotIn('cap',frame)
        self.assertIn('mag@1000Hz',frame)
        self.assertTrue(json.loads(out.with_suffix('.audit.json').read_text(encoding='utf-8')))
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit) as raised:
            extract_main(arguments)
        self.assertEqual(raised.exception.code,2)


class ReportingTests(TemporaryCase):
    def test_capacity_exactly_at_the_threshold_counts_as_defective(self):
        cfg=small_config(); frame=make_demo(cfg,8)
        frame.loc[0,'cap']=cfg.threshold_ah
        out=self.folder/'run'; out.mkdir()
        self.assertEqual(run(frame,cfg,out,[],{'data_kind':'synthetic_demo'})['status'],'completed')
        oof=pd.read_csv(out/'oof_predictions.csv').set_index('cell_number')
        self.assertEqual(float(oof.loc[41,'measured_cap_Ah']),cfg.threshold_ah)
        self.assertEqual(int(oof.loc[41,'true_label']),1)
        # The threshold score must grow as predicted capacity falls, and agree with its own decision.
        np.testing.assert_array_equal((oof['score_capacity_threshold'].to_numpy()>=0).astype(int),
                                      oof['pred_capacity_threshold'].to_numpy())
        self.assertLess(float(np.corrcoef(oof['score_capacity_threshold'],oof['measured_cap_Ah'])[0,1]),0)

    def test_missing_optional_target_reports_partial_rather_than_completed(self):
        cfg=small_config(); frame=make_demo(cfg,8).drop(columns=['cc_frac'])
        out=self.folder/'run'; out.mkdir()
        result=run(frame,cfg,out,[],{'data_kind':'synthetic_demo'})
        self.assertEqual(result['status'],'partial')
        self.assertEqual(list(result['unavailable']),['cc_fraction'])
        metrics=json.loads((out/'metrics.json').read_text(encoding='utf-8'))
        self.assertIn('cc_fraction',metrics['unavailable'])
        summary=(out/'run_summary.md').read_text(encoding='utf-8')
        self.assertIn('## 계산하지 못한 항목',summary)
        # The line names the target and says why; the parenthetical distinguishes a target with no
        # metrics at all from one whose metrics exist but whose deployment model could not be fitted.
        self.assertRegex(summary,r'- cc_fraction[^\n]*: cc_frac column not provided')
        labels=pd.read_excel(out/'results_for_origin.xlsx',sheet_name='08_label_summary')
        self.assertIn('unavailable_cc_fraction',labels['item'].tolist())

    def test_successful_run_records_artifact_hashes_under_posix_keys(self):
        cfg=small_config(); frame=make_demo(cfg,8)
        csv=self.folder/'features.csv'; frame.to_csv(csv,index=False,encoding='utf-8-sig')
        config=self.folder/'config.json'; config.write_text(json.dumps(config_dict(cfg)),encoding='utf-8')
        out=self.folder/'run'
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(export_main(['--features',str(csv),'--config',str(config),
                                          '--synthetic-data','--output',str(out)]),0)
        self.assertEqual(json.loads((out/'run.json').read_text(encoding='utf-8'))['status'],'completed')
        hashes=json.loads((out/'artifact_hashes.json').read_text(encoding='utf-8'))
        self.assertIn('models/capacity.joblib',hashes)
        self.assertEqual([key for key in hashes if '\\' in key],[])
        for key,expected in hashes.items():
            self.assertEqual(digest(out.joinpath(*key.split('/'))),expected,key)

    def test_workbook_never_stores_exported_text_as_a_formula(self):
        table=pd.DataFrame({'note':['=SUM(A1)','-1','+cmd','@ref','plain'],'value':[1.,2.,3.,4.,5.]})
        path=self.folder/'guard.xlsx'
        write_workbook(path,{'01_guard':table})
        wb=load_workbook(path,read_only=True,data_only=False)
        self.assertFalse(any(cell.data_type=='f' for sheet in wb for row in sheet for cell in row))
        wb.close()


class ReleaseCheckTests(TemporaryCase):
    """tests/verify_release.py runs as a script; load it by path so its helpers stay testable."""
    def module(self):
        spec=importlib.util.spec_from_file_location('release_checks',PACKAGE/'tests'/'verify_release.py')
        loaded=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
        return loaded

    def test_checks_are_explicit_so_optimized_runs_cannot_skip_them(self):
        release=self.module()
        self.assertTrue(release.require(True,'always_true'))
        with self.assertRaisesRegex(RuntimeError,'Release check failed: deliberate'):
            release.require(False,'deliberate')

    def test_hashed_sources_exclude_local_virtualenvs_and_results(self):
        release=self.module()
        for relative in ['.venv/lib/numpy.py','results/stale_run.py','__pycache__/cached.py',
                         'demo.py','tests/verify_release.py','examples/generate_examples.py']:
            path=self.folder/relative
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text('',encoding='utf-8')
        self.assertEqual([key for key,_ in release.package_sources(self.folder)],
                         ['demo.py','examples/generate_examples.py','tests/verify_release.py'])

    def test_recorded_artifact_paths_are_read_back_whatever_separator_wrote_them(self):
        release=self.module()
        root=Path('/run')
        self.assertEqual(release.artifact_path(root,'models/capacity.joblib'),root/'models'/'capacity.joblib')
        self.assertEqual(release.artifact_path(root,'models\\capacity.joblib'),root/'models'/'capacity.joblib')
        self.assertEqual(release.artifact_path(root,'run.json'),root/'run.json')


class PredictionTests(TemporaryCase):
    def prepared(self,**changes):
        cfg=small_config(**changes)
        clean,features=validate_frame(make_demo(cfg,8),cfg,[])
        X=clean[features]; ids=clean['cell_number'].to_numpy()
        targets=[('capacity',clean['cap'].to_numpy(),'regression'),
                 ('cc_fraction',clean['cc_frac'].to_numpy(),'regression'),
                 ('logistic',(clean['cap'].to_numpy()<=cfg.threshold_ah).astype(int),'classification')]
        bundles={}
        for name,y,kind in targets:
            model,_=select_model(X,y,ids,cfg,kind)
            bundles[name]={'pipeline':model,'config':config_dict(cfg),'version':VERSION,'model_name':name,
                           'input_features':features,'training_cells':clean['cell_number'].tolist(),
                           'training_min':X.min().to_dict(),'training_max':X.max().to_dict(),
                           'data_kind':'synthetic_demo'}
        return cfg,clean,features,bundles

    def test_prediction_fits_no_estimator_of_any_kind(self):
        cfg,clean,features,bundles=self.prepared()
        new=clean.drop(columns=['cap','cc_frac']).copy(); new['cell_number']+=100
        with contextlib.ExitStack() as stack:
            for estimator in FITTERS:
                stack.enter_context(patch.object(estimator,'fit',side_effect=AssertionError(f'{estimator.__name__} must never fit')))
            result=predict_frame(new,bundles)
        self.assertEqual(len(result),8)
        self.assertFalse(result[[c for c in result if c.endswith('_seen_in_training')]].any().any())

    def test_predicted_values_and_decisions_come_from_the_saved_models(self):
        cfg,clean,features,bundles=self.prepared()
        new=clean.drop(columns=['cap','cc_frac']).copy(); new['cell_number']+=100
        X=new[features]
        result=predict_frame(new,bundles)
        capacity=bundles['capacity']['pipeline'].predict(X)
        np.testing.assert_array_equal(result['predicted_capacity'].to_numpy(),capacity)
        np.testing.assert_array_equal(result['capacity_predicted_defective'].to_numpy(),
                                      (capacity<=cfg.threshold_ah).astype(int))
        np.testing.assert_array_equal(result['predicted_cc_fraction'].to_numpy(),
                                      bundles['cc_fraction']['pipeline'].predict(X))
        model=bundles['logistic']['pipeline']
        score=model.predict_proba(X)[:,list(model.named_steps['model'].classes_).index(1)]
        np.testing.assert_array_equal(result['logistic_score'].to_numpy(),score)
        np.testing.assert_array_equal(result['logistic_predicted_defective'].to_numpy(),
                                      (score>=cfg.decision_threshold).astype(int))
        # Both decisions must agree with the labels the same threshold gives the copied cells.
        np.testing.assert_array_equal(result['capacity_predicted_defective'].to_numpy(),
                                      (clean['cap'].to_numpy()<=cfg.threshold_ah).astype(int))
        np.testing.assert_array_equal(result['logistic_predicted_defective'].to_numpy(),
                                      (clean['cap'].to_numpy()<=cfg.threshold_ah).astype(int))

    def test_identical_features_need_no_review_and_shifted_ones_do(self):
        cfg,clean,features,bundles=self.prepared()
        copied=clean.drop(columns=['cap','cc_frac']).copy(); copied['cell_number']+=100
        result=predict_frame(copied,bundles)
        self.assertFalse(result['review_required'].any())
        self.assertFalse(result[[c for c in result if c.endswith('_outside_training_range')]].any().any())
        column=bundles['capacity']['pipeline'].named_steps['select'].columns[0]
        shifted=copied.copy()
        shifted.loc[0,column]=float(bundles['capacity']['training_max'][column])*1.5+1.
        flagged=predict_frame(shifted,bundles)
        self.assertTrue(bool(flagged.loc[0,'capacity_outside_training_range']))
        self.assertTrue(bool(flagged.loc[0,'review_required']))
        self.assertFalse(flagged.loc[1:,'capacity_outside_training_range'].any())

    def test_predict_cli_refuses_incomplete_runs_and_existing_output(self):
        cfg,clean,features,bundles=self.prepared()
        new=clean.drop(columns=['cap','cc_frac']).copy(); new['cell_number']+=100
        run_folder=self.folder/'run'; (run_folder/'models').mkdir(parents=True)
        for name,bundle in bundles.items():
            joblib.dump(bundle,run_folder/'models'/f'{name}.joblib')
        features_csv=self.folder/'new.csv'; new.to_csv(features_csv,index=False,encoding='utf-8-sig')
        out=self.folder/'predictions.csv'
        arguments=['--run',str(run_folder),'--features',str(features_csv),'--output',str(out)]
        write_json(run_folder/'run.json',{'status':'failed','data_kind':'synthetic_demo'})
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit) as raised:
            predict_main(arguments)
        self.assertEqual(raised.exception.code,2)
        self.assertFalse(out.exists())
        write_json(run_folder/'run.json',{'status':'completed','data_kind':'synthetic_demo'})
        write_json(run_folder/'artifact_hashes.json',
                   {p.relative_to(run_folder).as_posix():digest(p) for p in sorted(run_folder.rglob('*')) if p.is_file()})
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(predict_main(arguments),0)
        self.assertEqual(pd.read_csv(out)['cell_number'].tolist(),clean['cell_number'].add(100).tolist())
        provenance=json.loads(out.with_suffix('.provenance.json').read_text(encoding='utf-8'))
        self.assertEqual(provenance['data_kind'],'synthetic_demo')
        self.assertEqual(len(provenance['model_sha256']),3)
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit) as again:
            predict_main(arguments)
        self.assertEqual(again.exception.code,2)


if __name__=='__main__':
    unittest.main(verbosity=2)
