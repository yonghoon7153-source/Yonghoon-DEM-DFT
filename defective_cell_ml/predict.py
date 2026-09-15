"""Apply a locally trained run to new prepared features; never fits on new data."""
from pathlib import Path
import argparse
import joblib
import numpy as np
import pandas as pd
from config import Config,DataError,VERSION,digest,write_json
from extract_capacity import validate_frame

def predict_frame(frame,bundles):
    if not bundles:
        raise DataError('No models found')
    result=None
    for name,bundle in bundles.items():
        if bundle.get('version')!=VERSION:
            raise DataError('Model package version mismatch')
        cfg=Config(**bundle['config']).validate()
        df,_=validate_frame(frame,cfg,[],training=False)
        columns=bundle['input_features']
        if set(columns)-set(df):
            raise DataError(f'{name}: missing training input columns {sorted(set(columns)-set(df))}')
        if result is None:
            result=pd.DataFrame({'cell_number':df['cell_number']})
            result['review_required']=False
        X=df[columns]
        if not np.isfinite(X).all().all():
            raise DataError('Nonfinite prediction inputs')
        model=bundle['pipeline']
        outside=((X<pd.Series(bundle['training_min']))|(X>pd.Series(bundle['training_max']))).any(axis=1)
        result[f'{name}_outside_training_range']=outside.to_numpy()
        result[f'{name}_seen_in_training']=df['cell_number'].isin(bundle['training_cells']).to_numpy()
        result['review_required']|=outside.to_numpy()
        if name=='logistic':
            scores=model.predict_proba(X)[:,list(model.named_steps['model'].classes_).index(1)]
            result['logistic_score']=scores
            result['logistic_predicted_defective']=(scores>=cfg.decision_threshold).astype(int)
        else:
            scores=model.predict(X)
            result['predicted_'+name]=scores
            if name=='capacity':
                result['capacity_predicted_defective']=(scores<=cfg.threshold_ah).astype(int)
                result['review_required']|=scores<=0
            elif name=='cc_fraction':
                result['review_required']|=(scores<0)|(scores>1)
    return result

def main(argv=None):
    parser=argparse.ArgumentParser(description='Predict using a trusted local run; no retraining')
    parser.add_argument('--run',required=True,help='Completed training output directory')
    parser.add_argument('--features',required=True,help='New features CSV; capacity labels not required')
    parser.add_argument('--output',required=True,help='New predictions CSV')
    args=parser.parse_args(argv)
    output=Path(args.output)
    if output.exists() or output.with_suffix('.provenance.json').exists():
        parser.error('Output exists; choose a new path')
    import json
    run_path=Path(args.run)
    try:
        status=json.loads((run_path/'run.json').read_text(encoding='utf-8'))
        if status.get('status') not in ['completed','partial']:
            raise DataError('Training run is not complete')
        paths=sorted((run_path/'models').glob('*.joblib'))
        bundles={p.stem:joblib.load(p) for p in paths}
        frame=pd.read_csv(args.features)
        result=predict_frame(frame,bundles)
        output.parent.mkdir(parents=True,exist_ok=True)
        result.to_csv(output,index=False,encoding='utf-8-sig')
        write_json(output.with_suffix('.provenance.json'),{'features_sha256':digest(args.features),
            'model_sha256':{p.name:digest(p) for p in paths},'data_kind':status['data_kind'],
            'note':'Model estimates; no external performance or probability calibration guarantee'})
    except (DataError,ValueError,OSError,KeyError) as exc:
        parser.exit(2,f'Prediction error: {exc}\n')
    print(f'Predicted {len(result)} cells: {output}')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
