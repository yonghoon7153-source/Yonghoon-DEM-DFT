"""Apply a locally trained run to new prepared features; never fits on new data."""
from datetime import datetime,timezone
from pathlib import Path
import argparse
import importlib.metadata
import json
import os
import platform
import sys
import warnings
import joblib
import numpy as np
import pandas as pd
from config import Config,DataError,VERSION,digest,write_json
from extract_capacity import validate_frame

MODEL_NAMES=('capacity','cc_fraction','logistic')
BUNDLE_KEYS=('version','config','pipeline','input_features','training_min','training_max','training_cells')
LIBRARIES=('numpy','pandas','scikit-learn','scipy','joblib','openpyxl','threadpoolctl')
RANGE_RTOL=1e-9
RANGE_ATOL=1e-12
NOTE='Model estimates; no external performance or probability calibration guarantee'
PRIMARY='capacity_predicted_defective (capacity threshold) is the primary call; logistic_predicted_defective is a secondary check'

def versions():
    """Same probe as the training CLI; kept local so predicting stays import-light."""
    found={'python':platform.python_version()}
    for package in LIBRARIES:
        try:
            found[package]=importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            found[package]='missing'
    return found

def minor(value):
    return '.'.join(str(value).split('.')[:2])

def alert(alerts,text):
    alerts.append(text)
    print(f'Warning: {text}',file=sys.stderr)

def check_bundle(name,bundle):
    if not isinstance(bundle,dict) or any(key not in bundle for key in BUNDLE_KEYS):
        raise DataError(f'{name}: not a model bundle written by this package')
    if bundle.get('version')!=VERSION:
        raise DataError(f"{name}: model package version mismatch (bundle {bundle.get('version')!r}, package {VERSION})")
    return bundle

def bundle_config(name,bundle):
    try:
        return Config(**bundle['config']).validate()
    except TypeError as exc:
        raise DataError(f'{name}: bundle configuration is not readable by this package ({exc})') from exc

def selected_features(bundle):
    """Features the saved pipeline actually uses; bundles without the key are read from the pipeline."""
    columns=bundle.get('selected_features')
    if columns is None:
        columns=getattr(getattr(bundle['pipeline'],'named_steps',{}).get('select'),'columns',None)
    return list(columns) if columns else list(bundle['input_features'])

def training_box(name,bundle,columns):
    """Observed training min/max widened by a tiny tolerance so CSV round-trip noise is not an excursion."""
    low=pd.Series(bundle['training_min'],dtype=float).reindex(columns)
    high=pd.Series(bundle['training_max'],dtype=float).reindex(columns)
    if not np.isfinite(low).all() or not np.isfinite(high).all():
        raise DataError(f'{name}: bundle training range does not cover every input feature')
    return low-(RANGE_ATOL+RANGE_RTOL*low.abs()),high+(RANGE_ATOL+RANGE_RTOL*high.abs())

def flag(review,reasons,mask,text):
    review|=mask
    for i in np.flatnonzero(mask):
        reasons[i].append(text)

def predict_frame(frame,bundles):
    if not bundles:
        raise DataError('No models found')
    result=None
    used=set()
    for name,bundle in bundles.items():
        check_bundle(name,bundle)
        cfg=bundle_config(name,bundle)
        if cfg.use_ocv and 'ocv' not in frame:
            raise DataError(f'{name}: this model was trained with ocv; the prediction CSV needs an ocv column '
                            '(a saved bundle keeps its training configuration and cannot be switched to EIS-only here)')
        df,features=validate_frame(frame,cfg,[],training=False)
        columns=list(bundle['input_features'])
        if set(columns)-set(df):
            raise DataError(f'{name}: missing training input columns {sorted(set(columns)-set(df))}')
        used.update(columns,features)
        if result is None:
            source=df
            result=pd.DataFrame({'cell_number':df['cell_number']})
            review=np.zeros(len(df),dtype=bool)
            reasons=[[] for _ in range(len(df))]
        X=df[columns]
        if not np.isfinite(X).all().all():
            raise DataError('Nonfinite prediction inputs')
        model=bundle['pipeline']
        low,high=training_box(name,bundle,columns)
        breach=(X.lt(low,axis=1)|X.gt(high,axis=1)).to_numpy()
        labels=np.asarray(columns,dtype=object)
        outside=breach.any(axis=1)
        result[f'{name}_outside_training_range']=outside.astype(int)
        result[f'{name}_outside_features']=[';'.join(labels[row]) for row in breach]
        result[f'{name}_seen_in_training']=df['cell_number'].isin(bundle['training_cells']).to_numpy().astype(int)
        review|=outside
        for i in np.flatnonzero(outside):
            reasons[i].append(f"{name}:outside[{','.join(labels[breach[i]])}]")
        if name=='logistic':
            scores=model.predict_proba(X)[:,list(model.named_steps['model'].classes_).index(1)]
            result['logistic_score']=scores
            result['logistic_predicted_defective']=(scores>=cfg.decision_threshold).astype(int)
        else:
            scores=model.predict(X)
            result['predicted_'+name]=scores
            if name=='capacity':
                result['predicted_capacity_mAh_cm2']=scores*1000/cfg.area_cm2
                result['capacity_predicted_defective']=(scores<=cfg.threshold_ah).astype(int)
                flag(review,reasons,scores<=0,'capacity:predicted<=0')
            elif name=='cc_fraction':
                flag(review,reasons,(scores<0)|(scores>1),'cc_fraction:predicted outside 0-1')
    result.insert(1,'review_required',review.astype(int))
    result.insert(2,'review_reason',[';'.join(reason) for reason in reasons])
    for column in source.columns:
        if column not in result and column not in used and column not in ('cap','cc_frac'):
            result[column]=source[column].to_numpy()
    order=pd.to_numeric(frame['cell_number'],errors='coerce').astype('int64').to_numpy()
    return result.set_index('cell_number').reindex(order).reset_index()

def verify_hashes(run_path,paths):
    """artifact_hashes.json is written by every run that is not failed; models must still match it."""
    listing=run_path/'artifact_hashes.json'
    if not listing.is_file():
        raise DataError(f'{run_path}: artifact_hashes.json not found; pass a training output directory written by this package')
    hashes={str(key).replace('\\','/'):value for key,value in json.loads(listing.read_text(encoding='utf-8')).items()}
    for path in paths:
        recorded=hashes.get(f'models/{path.name}')
        if recorded is None:
            raise DataError(f'{path.name}: not listed in artifact_hashes.json; the run directory was modified')
        if recorded!=digest(path):
            raise DataError(f'{path.name}: model file hash mismatch; the run directory was modified')

def load_bundles(paths,alerts):
    bundles={}
    for path in paths:
        if path.stem not in MODEL_NAMES:
            raise DataError(f"{path.name}: unexpected model file; expected {', '.join(n+'.joblib' for n in MODEL_NAMES)}")
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            try:
                bundle=joblib.load(path)
            except Exception as exc:
                raise DataError(f'{path.name}: cannot load model bundle ({type(exc).__name__}); '
                                'copy models/ again and use the training dependency versions') from exc
        for item in caught:
            alert(alerts,f'{path.name}: {item.category.__name__}: {item.message}')
        check_bundle(path.stem,bundle)
        if bundle.get('model_name') not in (None,path.stem):
            raise DataError(f"{path.name}: bundle was saved as {bundle.get('model_name')!r}; do not rename model files")
        bundles[path.stem]=bundle
    return bundles

def check_environment(trained,alerts,allow_mismatch):
    current=versions()
    if not trained:
        alert(alerts,'Training run recorded no dependency versions; the prediction environment cannot be compared')
        return {}
    mismatch={k:{'training':v,'prediction':current.get(k)} for k,v in trained.items() if k in current and current[k]!=v}
    learner=str(trained.get('scikit-learn',''))
    if learner and minor(learner)!=minor(current['scikit-learn']) and not allow_mismatch:
        raise DataError(f"scikit-learn {learner} trained these models but {current['scikit-learn']} is installed; "
                        'install requirements.lock.txt or pass --allow-version-mismatch')
    if mismatch:
        alert(alerts,f'Dependency versions differ from the training run: {json.dumps(mismatch,ensure_ascii=False)}')
    return mismatch

def run_notices(status,bundles):
    lines=[]
    if status.get('status')!='completed':
        lines.append(f"Training run status {status.get('status')}; unavailable targets: "
                     f"{json.dumps(status.get('unavailable',{}),ensure_ascii=False)}")
    missing=[name for name in MODEL_NAMES if name not in bundles]
    if missing:
        lines.append(f"No saved model for {', '.join(missing)}; those columns are absent from the output")
    if status.get('data_kind')=='synthetic_demo':
        lines.append('Models were trained on synthetic demo data; these numbers are not measurements of real cells')
    return lines

def model_provenance(bundle):
    estimator=getattr(bundle['pipeline'],'named_steps',{}).get('model')
    return {'estimator':type(estimator if estimator is not None else bundle['pipeline']).__name__,
            'selected_features':selected_features(bundle),'n_input_features':len(bundle['input_features']),
            'n_training_cells':len(bundle['training_cells']),'data_kind':bundle.get('data_kind')}

def main(argv=None):
    parser=argparse.ArgumentParser(description='Predict using a trusted local run; no retraining')
    parser.add_argument('--run',required=True,help='Completed training output directory (the parent of models/)')
    parser.add_argument('--features',required=True,help='New features CSV; capacity labels not required')
    parser.add_argument('--output',required=True,help='New predictions CSV')
    parser.add_argument('--allow-version-mismatch',action='store_true',
                        help='Predict even when installed dependency versions differ from the training run')
    args=parser.parse_args(argv)
    output=Path(args.output)
    provenance_path=output.with_suffix('.provenance.json')
    if output.exists() or provenance_path.exists():
        parser.error('Output exists; choose a new path')
    run_path=Path(args.run)
    alerts=[]
    partial=[output.with_name(output.name+'.tmp'),provenance_path.with_name(provenance_path.name+'.tmp')]
    try:
        if not (run_path/'run.json').is_file():
            raise DataError(f'{run_path}: run.json not found; pass the completed training output directory '
                            '(the parent of models/), not models/ itself')
        status=json.loads((run_path/'run.json').read_text(encoding='utf-8'))
        if status.get('status') not in ['completed','partial']:
            raise DataError('Training run is not complete')
        if not status.get('data_kind'):
            raise DataError('run.json lacks data_kind; repeat the training run with this package version')
        paths=sorted((run_path/'models').glob('*.joblib'))
        verify_hashes(run_path,paths)
        bundles=load_bundles(paths,alerts)
        trained=next((b['versions'] for b in bundles.values() if isinstance(b.get('versions'),dict)),
                     status.get('versions') or {})
        mismatch=check_environment(trained,alerts,args.allow_version_mismatch)
        notices=run_notices(status,bundles)
        frame=pd.read_csv(args.features,float_precision='round_trip')
        result=predict_frame(frame,bundles)
        cfg=bundle_config(*next(iter(bundles.items())))
        provenance={'features_sha256':digest(args.features),'model_sha256':{p.name:digest(p) for p in paths},
            'data_kind':status['data_kind'],'note':NOTE,'package_version':VERSION,
            'predicted_utc':datetime.now(timezone.utc).isoformat(),'run_dir':str(run_path.resolve()),
            'run_json_sha256':digest(run_path/'run.json'),
            'config_json_sha256':digest(run_path/'config.json') if (run_path/'config.json').is_file() else None,
            'artifact_hashes_verified':True,'run_status':status.get('status'),
            'unavailable':status.get('unavailable',{}),'missing_models':[n for n in MODEL_NAMES if n not in bundles],
            'training_versions':trained,'prediction_versions':versions(),'version_mismatch':mismatch,
            'warnings':alerts,'notices':notices,
            'models':{name:model_provenance(bundle) for name,bundle in bundles.items()},
            'thresholds':{'threshold_ah':cfg.threshold_ah,'decision_threshold':cfg.decision_threshold,
                          'area_cm2':cfg.area_cm2},
            'primary_decision':PRIMARY,'range_tolerance':{'relative':RANGE_RTOL,'absolute':RANGE_ATOL},
            'column_units':{'predicted_capacity':'Ah','predicted_capacity_mAh_cm2':'mAh/cm2',
                            'predicted_cc_fraction':'fraction 0-1','logistic_score':'probability'},
            'n_cells':int(len(result)),'n_review_required':int(result['review_required'].sum()),
            'n_outside_training_range':{n:int(result[f'{n}_outside_training_range'].sum()) for n in bundles}}
        output.parent.mkdir(parents=True,exist_ok=True)
        result.to_csv(partial[0],index=False,encoding='utf-8-sig')
        write_json(partial[1],provenance)
        os.replace(partial[0],output)
        os.replace(partial[1],provenance_path)
    except (DataError,ValueError,OSError,KeyError) as exc:
        for path in partial+[output,provenance_path]:
            Path(path).unlink(missing_ok=True)
        parser.exit(2,f'Prediction error: {exc}\n')
    for line in notices:
        print(line)
    print(f'Predicted {len(result)} cells: {output}')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
