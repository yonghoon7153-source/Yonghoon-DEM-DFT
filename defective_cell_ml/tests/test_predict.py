"""Prediction CLI regressions: range tolerance, artifact/version checks, output form."""
from pathlib import Path
from tempfile import TemporaryDirectory
import contextlib
import io
import json
import shutil
import sys
import unittest

PACKAGE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PACKAGE))
import joblib
import numpy as np
import pandas as pd
from config import Config,DataError,VERSION,config_dict,digest,write_json
from demo import make_demo
from extract_capacity import validate_frame
from ridge_capacity import select_model
import predict

def small_config(**changes):
    values=dict(frequency_grid_hz=[.1,1.,10.,1000.,10000.,100000.],
                feature_sets=['single_1e3'],ridge_alphas=[.1,10.],logistic_cs=[.1,1.],
                inner_splits=2,use_ocv=False)
    values.update(changes)
    return Config(**values).validate()

def training_frame(cfg,cells=8):
    clean,features=validate_frame(make_demo(cfg,cells),cfg,[])
    return clean,features

def make_bundle(cfg,clean,features,name='capacity',**extra):
    X=clean[features]; ids=clean['cell_number'].to_numpy()
    y=(clean['cap'].to_numpy()<=cfg.threshold_ah).astype(int) if name=='logistic' else clean['cap'].to_numpy()
    model,_=select_model(X,y,ids,cfg,'classification' if name=='logistic' else 'regression')
    return {'pipeline':model,'config':config_dict(cfg),'version':VERSION,'model_name':name,
            'input_features':list(X.columns),'training_cells':list(map(int,ids)),
            'training_min':X.min().to_dict(),'training_max':X.max().to_dict(),
            'data_kind':'synthetic_demo',**extra}

def new_frame(clean,shift=100):
    frame=clean.drop(columns=[c for c in ('cap','cc_frac') if c in clean]).copy()
    frame['cell_number']+=shift
    return frame

def stamp_hashes(folder):
    """Mirror the training CLI: record every file present, then the listing itself is written last."""
    listing=folder/'artifact_hashes.json'
    listing.unlink(missing_ok=True)
    write_json(listing,{str(p.relative_to(folder)).replace('\\','/'):digest(p)
                        for p in sorted(folder.rglob('*')) if p.is_file()})

def build_run(folder,cfg,clean,features,names=('capacity',),status='completed',data_kind='synthetic_demo',**extra):
    (folder/'models').mkdir(parents=True)
    for name in names:
        bundle=make_bundle(cfg,clean,features,name,**extra)
        bundle['data_kind']=data_kind
        joblib.dump(bundle,folder/'models'/f'{name}.joblib')
    write_json(folder/'config.json',config_dict(cfg))
    meta={'version':VERSION,'status':status,'data_kind':data_kind,'versions':predict.versions()}
    if status=='partial':
        meta['unavailable']={'logistic':'Too few minority cells for inner classification validation'}
    write_json(folder/'run.json',meta)
    stamp_hashes(folder)

def run_cli(argv):
    out=io.StringIO(); err=io.StringIO()
    with contextlib.redirect_stdout(out),contextlib.redirect_stderr(err):
        try:
            code=predict.main(argv)
        except SystemExit as exc:
            code=exc.code
    return code,out.getvalue(),err.getvalue()

class RangeAndColumnTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg=small_config()
        cls.clean,cls.features=training_frame(cls.cfg)
        cls.bundle=make_bundle(cls.cfg,cls.clean,cls.features)

    def test_one_ulp_above_training_max_is_not_an_excursion(self):
        frame=new_frame(self.clean); column=self.features[0]
        high=self.bundle['training_max'][column]
        frame.loc[frame.index[0],column]=np.nextafter(high,np.inf)
        result=predict.predict_frame(frame,{'capacity':self.bundle})
        self.assertEqual(int(result['capacity_outside_training_range'].sum()),0)
        self.assertEqual(int(result['review_required'].sum()),0)
        self.assertEqual(list(result['review_reason'].unique()),[''])

    def test_real_excursion_is_flagged_with_feature_names_and_reason(self):
        frame=new_frame(self.clean); first,second=self.features[0],self.features[1]
        high=self.bundle['training_max'][first]; low=self.bundle['training_min'][second]
        frame.loc[frame.index[0],first]=high+abs(high)*.01+1e-6
        frame.loc[frame.index[0],second]=low-abs(low)*.01-1e-6
        result=predict.predict_frame(frame,{'capacity':self.bundle}).set_index('cell_number')
        row=result.loc[int(frame['cell_number'].iloc[0])]
        self.assertEqual(int(row['capacity_outside_training_range']),1)
        self.assertEqual(int(row['review_required']),1)
        self.assertEqual(set(row['capacity_outside_features'].split(';')),{first,second})
        self.assertTrue(row['review_reason'].startswith('capacity:outside['),row['review_reason'])
        self.assertEqual(int(result['capacity_outside_training_range'].sum()),1)

    def test_missing_ocv_message_names_the_prediction_context(self):
        cfg=small_config(use_ocv=True)
        clean,features=training_frame(cfg)
        bundle=make_bundle(cfg,clean,features)
        frame=new_frame(clean).drop(columns=['ocv'])
        with self.assertRaises(DataError) as caught:
            predict.predict_frame(frame,{'capacity':bundle})
        self.assertIn('trained with ocv',str(caught.exception))
        self.assertNotIn('use_ocv=false',str(caught.exception))

    def test_object_without_bundle_keys_is_reported_before_the_version_gate(self):
        with self.assertRaises(DataError) as caught:
            predict.predict_frame(new_frame(self.clean),{'capacity':{'foo':1}})
        self.assertIn('not a model bundle',str(caught.exception))
        with self.assertRaises(DataError) as caught:
            predict.predict_frame(new_frame(self.clean),{'capacity':dict(self.bundle,version='1.0.0')})
        self.assertIn('version mismatch',str(caught.exception))
        stale=dict(self.bundle,config=dict(self.bundle['config'],unknown_option=1))
        with self.assertRaises(DataError) as caught:
            predict.predict_frame(new_frame(self.clean),{'capacity':stale})
        self.assertIn('not readable',str(caught.exception))

    def test_flags_are_integers_units_are_explicit_and_input_order_is_kept(self):
        frame=new_frame(self.clean).iloc[::-1].reset_index(drop=True)
        result=predict.predict_frame(frame,{'capacity':self.bundle})
        self.assertEqual(result['cell_number'].tolist(),frame['cell_number'].tolist())
        for column in ['review_required','capacity_outside_training_range','capacity_seen_in_training',
                       'capacity_predicted_defective']:
            self.assertTrue(pd.api.types.is_integer_dtype(result[column]),column)
        np.testing.assert_allclose(result['predicted_capacity_mAh_cm2'],
                                   result['predicted_capacity']*1000/self.cfg.area_cm2)
        self.assertIn('batch_id',result)
        self.assertEqual(result['batch_id'].tolist(),frame['batch_id'].tolist())
        self.assertNotIn('cap',result)

    def test_selected_features_read_from_bundle_or_pipeline(self):
        chosen=list(self.bundle['pipeline'].named_steps['select'].columns)
        self.assertEqual(predict.selected_features(self.bundle),chosen)
        self.assertLess(len(chosen),len(self.bundle['input_features']))
        stated=dict(self.bundle,selected_features=['ocv'])
        self.assertEqual(predict.selected_features(stated),['ocv'])

class PredictCommandTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg=small_config()
        cls.clean,cls.features=training_frame(cls.cfg)
        cls.store=TemporaryDirectory(prefix='predict_template_')
        cls.template=Path(cls.store.name)/'run'
        build_run(cls.template,cls.cfg,cls.clean,cls.features)
        cls.csv=Path(cls.store.name)/'new_features.csv'
        new_frame(cls.clean,0).to_csv(cls.csv,index=False,encoding='utf-8-sig')

    @classmethod
    def tearDownClass(cls):
        cls.store.cleanup()

    def setUp(self):
        self.tmp=TemporaryDirectory(prefix='predict_case_')
        self.folder=Path(self.tmp.name)
        self.run=self.folder/'run'
        shutil.copytree(self.template,self.run)
        self.output=self.folder/'out.csv'
        self.provenance=self.output.with_suffix('.provenance.json')
        self.addCleanup(self.tmp.cleanup)

    def argv(self,*extra):
        return ['--run',str(self.run),'--features',str(self.csv),'--output',str(self.output),*extra]

    def edit_run_json(self,**changes):
        meta=json.loads((self.run/'run.json').read_text(encoding='utf-8'))
        for key,value in changes.items():
            if value is None:
                meta.pop(key,None)
            else:
                meta[key]=value
        write_json(self.run/'run.json',meta)
        stamp_hashes(self.run)

    def test_training_features_reused_are_never_flagged_for_review(self):
        code,out,_=run_cli(self.argv())
        self.assertEqual(code,0,out)
        result=pd.read_csv(self.output)
        self.assertEqual(int(result['review_required'].sum()),0)
        self.assertEqual(int(result['capacity_outside_training_range'].sum()),0)
        self.assertEqual(int(result['capacity_seen_in_training'].sum()),len(result))
        self.assertEqual(result['cell_number'].tolist(),pd.read_csv(self.csv)['cell_number'].tolist())
        provenance=json.loads(self.provenance.read_text(encoding='utf-8'))
        self.assertTrue(provenance['artifact_hashes_verified'])
        self.assertEqual(provenance['n_review_required'],0)
        self.assertEqual(provenance['thresholds']['threshold_ah'],self.cfg.threshold_ah)
        self.assertEqual(provenance['column_units']['predicted_capacity'],'Ah')
        self.assertEqual(provenance['models']['capacity']['n_training_cells'],len(self.clean))
        self.assertTrue(provenance['models']['capacity']['selected_features'])
        self.assertEqual(provenance['prediction_versions']['scikit-learn'],
                         provenance['training_versions']['scikit-learn'])

    def test_modified_model_file_is_refused_against_artifact_hashes(self):
        path=self.run/'models'/'capacity.joblib'
        bundle=joblib.load(path)
        bundle['training_min']={k:-1e9 for k in bundle['training_min']}
        joblib.dump(bundle,path)
        code,_,err=run_cli(self.argv())
        self.assertEqual(code,2)
        self.assertIn('hash mismatch',err)
        self.assertFalse(self.output.exists())

    def test_renamed_or_foreign_model_file_is_refused(self):
        shutil.copy(self.run/'models'/'capacity.joblib',self.run/'models'/'capacity_demo.joblib')
        stamp_hashes(self.run)
        code,_,err=run_cli(self.argv())
        self.assertEqual(code,2)
        self.assertIn('unexpected model file',err)
        self.assertFalse(self.output.exists())

    def test_damaged_bundle_exits_two_with_context(self):
        path=self.run/'models'/'capacity.joblib'
        path.write_bytes(path.read_bytes()[:800])
        stamp_hashes(self.run)
        code,_,err=run_cli(self.argv())
        self.assertEqual(code,2)
        self.assertIn('cannot load model bundle',err)
        self.assertFalse(self.output.exists())

    def test_scikit_learn_mismatch_blocks_unless_explicitly_allowed(self):
        versions=dict(predict.versions(),**{'scikit-learn':'1.0.0'})
        self.edit_run_json(versions=versions)
        code,_,err=run_cli(self.argv())
        self.assertEqual(code,2)
        self.assertIn('scikit-learn 1.0.0',err)
        self.assertFalse(self.output.exists())
        code,_,err=run_cli(self.argv('--allow-version-mismatch'))
        self.assertEqual(code,0)
        provenance=json.loads(self.provenance.read_text(encoding='utf-8'))
        self.assertEqual(provenance['version_mismatch']['scikit-learn']['training'],'1.0.0')
        self.assertTrue(provenance['warnings'])
        self.assertIn('Dependency versions differ',err)

    def test_bundle_recorded_versions_take_precedence(self):
        path=self.run/'models'/'capacity.joblib'
        bundle=joblib.load(path)
        bundle['versions']=dict(predict.versions(),**{'scikit-learn':'0.24.0'})
        joblib.dump(bundle,path)
        stamp_hashes(self.run)
        code,_,err=run_cli(self.argv())
        self.assertEqual(code,2)
        self.assertIn('scikit-learn 0.24.0',err)

    def test_partial_run_states_what_is_missing_and_that_data_is_synthetic(self):
        self.edit_run_json(status='partial',
                           unavailable={'logistic':'Too few minority cells for inner classification validation'})
        code,out,_=run_cli(self.argv())
        self.assertEqual(code,0,out)
        self.assertIn('partial',out)
        self.assertIn('Too few minority cells',out)
        self.assertIn('cc_fraction, logistic',out)
        self.assertIn('synthetic demo data',out)
        provenance=json.loads(self.provenance.read_text(encoding='utf-8'))
        self.assertEqual(provenance['run_status'],'partial')
        self.assertIn('logistic',provenance['unavailable'])
        self.assertEqual(provenance['missing_models'],['cc_fraction','logistic'])
        self.assertEqual(provenance['run_dir'],str(self.run.resolve()))
        self.assertEqual(provenance['package_version'],VERSION)
        self.assertTrue(provenance['predicted_utc'])

    def test_failure_leaves_no_partial_output_and_the_path_stays_usable(self):
        self.edit_run_json(data_kind=None)
        code,_,err=run_cli(self.argv())
        self.assertEqual(code,2)
        self.assertIn('data_kind',err)
        self.assertFalse(self.output.exists())
        self.assertFalse(self.provenance.exists())
        self.assertEqual(list(self.folder.glob('out*')),[])
        self.edit_run_json(data_kind='synthetic_demo')
        code,out,_=run_cli(self.argv())
        self.assertEqual(code,0,out)
        self.assertTrue(self.output.exists() and self.provenance.exists())

    def test_run_directory_mistakes_are_explained(self):
        code,_,err=run_cli(['--run',str(self.run/'models'),'--features',str(self.csv),
                            '--output',str(self.output)])
        self.assertEqual(code,2)
        self.assertIn('run.json not found',err)
        self.assertIn('parent of models/',err)
        self.assertFalse(self.output.exists())

if __name__=='__main__':
    unittest.main(verbosity=2)
