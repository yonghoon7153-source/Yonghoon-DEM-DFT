"""Exercise the distributable package using artificial data in a new directory."""
from pathlib import Path
import argparse
import json
import subprocess
import sys
from datetime import datetime,timezone
import numpy as np
import pandas as pd
from openpyxl import load_workbook

PACKAGE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PACKAGE))
from config import digest,load_config,write_json
from export_for_origin import versions

# A .venv/results/__pycache__ inside the package folder is local user state, not released code.
SKIPPED_DIRECTORIES={'.venv','venv','env','results','__pycache__'}
# Recomputed independently of export_for_origin.outcome so a swapped label is detectable.
OUTCOME_LABELS={(1,1):'TP',(1,0):'FN',(0,1):'FP',(0,0):'TN'}
CLASSIFIERS=[('capacity_threshold','pred_capacity_threshold','score_capacity_threshold','outcome_capacity_threshold'),
             ('logistic_nested_selection','pred_logistic','score_logistic','outcome_logistic')]


def package_sources(folder=None,prefix=()):
    """Released Python sources only, keyed by POSIX path so records stay comparable across systems."""
    for entry in sorted((folder or PACKAGE).iterdir()):
        if entry.is_dir():
            if entry.name not in SKIPPED_DIRECTORIES and not entry.name.startswith('.'):
                yield from package_sources(entry,prefix+(entry.name,))
        elif entry.suffix=='.py':
            yield '/'.join(prefix+(entry.name,)),entry


def require(condition,name):
    """Explicit check; unlike assert it survives python -O and PYTHONOPTIMIZE."""
    if not condition:
        raise RuntimeError(f'Release check failed: {name}')
    return True


def artifact_path(folder,recorded):
    # Hash keys are POSIX; tolerate backslash keys written by older Windows runs.
    return folder.joinpath(*recorded.replace('\\','/').split('/'))


def main():
    parser=argparse.ArgumentParser(description='Synthetic release checks; requires a new output directory')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    if sys.flags.optimize:
        parser.error('Run without -O/PYTHONOPTIMIZE so every release check is evaluated')
    out=Path(args.output).resolve()
    if out.exists():
        parser.error('Output exists; choose a new directory')
    out.mkdir(parents=True)
    report={'started_utc':datetime.now(timezone.utc).isoformat(),'status':'running',
            'data_kind':'synthetic_only','versions':versions(),'commands':[],'checks':[],
            'code_sha256':{key:digest(path) for key,path in sorted(package_sources())}}
    # Published fixture values are the ground truth every value-level check below compares against.
    # config.json and examples/config_group.json differ only in outer_cv, so one threshold labels all three runs.
    cfg=load_config(PACKAGE/'config.json')
    truth=pd.read_csv(PACKAGE/'examples'/'demo_features.csv').sort_values('cell_number').reset_index(drop=True)
    labels=(truth['cap']<=cfg.threshold_ah).astype(int)

    def execute(name,arguments):
        command=[sys.executable,'-X','utf8','-B',*map(str,arguments)]
        result=subprocess.run(command,cwd=PACKAGE,encoding='utf-8',errors='replace',capture_output=True,timeout=600)
        # Saved evidence stays portable and omits machine-specific filesystem roots.
        def portable(text):
            return text.replace(str(out),'{validation_output}').replace(str(PACKAGE),'{package}')
        (out/f'{name}.log').write_text(portable(result.stdout+'\n'+result.stderr),encoding='utf-8')
        report['commands'].append({'name':name,'arguments':[portable(str(v)) for v in arguments],
                                    'returncode':result.returncode,'log':f'{name}.log'})
        if result.returncode:
            raise RuntimeError(f'{name} failed; see {out/name}.log')
        print(f'PASS {name}',flush=True)

    def check(name):
        report['checks'].append({'name':name,'status':'passed'})
        print(f'PASS {name}',flush=True)

    try:
        execute('01_unit_tests',['-m','unittest','discover','-s','tests','-v'])
        execute('02_full_default_demo',['export_for_origin.py','--demo','--output',out/'demo'])
        raw=['--cycle-dir','examples/raw/cycle','--eis-dir','examples/raw/eis',
             '--selection-manifest','examples/selection_manifest.csv','--config','examples/config_group.json']
        execute('03_prepare_raw',['extract_capacity.py',*raw,'--output',out/'prepared.csv'])
        prepared=pd.read_csv(out/'prepared.csv').sort_values('cell_number').reset_index(drop=True)
        # The raw fixtures were written from demo_features.csv, so the readers must restore those values.
        pd.testing.assert_frame_equal(prepared[truth.columns],truth,check_exact=False,rtol=1e-9,atol=1e-12)
        check('raw_readers_restore_the_published_example_features')
        execute('04_train_raw_group',['export_for_origin.py',*raw,'--synthetic-data','--output',out/'raw_group'])
        execute('05_train_csv_group',['export_for_origin.py','--features',out/'prepared.csv',
                '--config','examples/config_group.json','--synthetic-data','--output',out/'csv_group'])
        left=pd.read_csv(out/'raw_group'/'oof_predictions.csv')
        right=pd.read_csv(out/'csv_group'/'oof_predictions.csv')
        pd.testing.assert_frame_equal(left,right,check_exact=False,rtol=1e-8,atol=1e-12)
        check('raw_and_prepared_csv_reproduce_same_OOF')
        for run_name in ['demo','raw_group','csv_group']:
            folder=out/run_name
            state=json.loads((folder/'run.json').read_text(encoding='utf-8'))
            require(state['status']=='completed' and state['data_kind']=='synthetic_demo',f'{run_name}_completed_as_synthetic')
            metrics=json.loads((folder/'metrics.json').read_text(encoding='utf-8'),
                               parse_constant=lambda value:(_ for _ in ()).throw(ValueError(value)))
            for row in metrics['classification']:
                require(sum(row[k] for k in ['TP','FN','FP','TN'])==row['n_samples']==12,f'{run_name}_confusion_matrix_covers_12_cells')
            preds=pd.read_csv(folder/'oof_predictions.csv')
            require(preds['cell_number'].is_unique and len(preds)==12,f'{run_name}_reports_12_distinct_cells')
            require(np.isfinite(preds[['pred_capacity_Ah','pred_cc_frac','score_logistic']]).all().all(),f'{run_name}_predictions_finite')
            # Value-level oracle: the fixture's own capacities decide labels, outcomes and score direction.
            require(preds['cell_number'].tolist()==truth['cell_number'].tolist(),f'{run_name}_covers_the_fixture_cells')
            np.testing.assert_allclose(preds['measured_cap_Ah'],truth['cap'],rtol=1e-8,atol=1e-12)
            require((preds['true_label'].to_numpy()==labels.to_numpy()).all(),f'{run_name}_labels_follow_the_capacity_threshold')
            reported={row['model']:row for row in metrics['classification']}
            for model,predicted,score,outcome in CLASSIFIERS:
                row=reported.get(model)
                require(row is not None,f'{run_name}_{model}_row_present')
                decided=preds[predicted].to_numpy(dtype=int); actual=labels.to_numpy()
                counts={key:int(((actual==a)&(decided==b)).sum()) for key,(a,b) in
                        {'TP':(1,1),'FN':(1,0),'FP':(0,1),'TN':(0,0)}.items()}
                require(all(row[key]==value for key,value in counts.items()),f'{run_name}_{model}_confusion_matrix_matches_its_own_OOF_rows')
                require(int((decided==actual).sum())>=11,f'{run_name}_{model}_decisions_match_fixture_truth')
                require(row['AUC_pooled_OOF'] is not None and row['AUC_pooled_OOF']>=.9,f'{run_name}_{model}_ranks_the_separable_fixture')
                require(float(np.corrcoef(preds[score],preds['measured_cap_Ah'])[0,1])<-.5,f'{run_name}_{model}_score_rises_as_capacity_falls')
                expected=[OUTCOME_LABELS[(int(a),int(b))] for a,b in zip(preds['true_label'],preds[predicted])]
                require(preds[outcome].tolist()==expected,f'{run_name}_{outcome}_recomputes_from_labels_and_decisions')
            wb=load_workbook(folder/'results_for_origin.xlsx',read_only=True,data_only=False)
            require(len(wb.sheetnames)==11 and wb['07_clf_cellwise'].max_row==13,f'{run_name}_workbook_has_11_sheets_and_12_rows')
            require(not any(cell.data_type=='f' for sheet in wb for row in sheet for cell in row),f'{run_name}_workbook_holds_no_formulas')
            wb.close()
            hashes=json.loads((folder/'artifact_hashes.json').read_text(encoding='utf-8'))
            require(all(digest(artifact_path(folder,path))==expected for path,expected in hashes.items()),f'{run_name}_artifacts_match_recorded_hashes')
        check('all_three_runs_complete_12_cells_11_sheets_finite_metrics_and_valid_hashes')
        check('all_three_runs_reproduce_the_fixture_labels_outcomes_and_score_direction')
        traces=json.loads((out/'raw_group'/'folds.json').read_text(encoding='utf-8'))
        for target,folds in traces.items():
            require(len(folds)==3,f'{target}_has_3_outer_folds')
            for fold in folds:
                test=set(fold['test_cells']); groups=set(fold['test_groups'])
                require(not test & set(fold['training_cells']),f'{target}_outer_cells_disjoint')
                require(np.isfinite(fold['best_inner_score']),f'{target}_inner_score_finite')
                for inner in fold['inner_folds']:
                    require(not groups & (set(inner['train_groups'])|set(inner['validation_groups'])),f'{target}_outer_group_absent_from_inner')
                    require(not set(inner['train_groups']) & set(inner['validation_groups']),f'{target}_inner_groups_disjoint')
        check('all_three_targets_keep_outer_and_inner_groups_separate')
        execute('06_prepare_unlabeled_eis',['extract_capacity.py','--config','config.json',
                '--eis-dir','examples/raw/new_eis','--output',out/'new_features.csv'])
        execute('07_predict_from_saved_models',['predict.py','--run',out/'raw_group',
                '--features',out/'new_features.csv','--output',out/'new_predictions.csv'])
        prediction=pd.read_csv(out/'new_predictions.csv')
        require(prediction['cell_number'].tolist()==list(range(61,73)),'new_predictions_carry_the_relabelled_identifiers')
        require(np.isfinite(prediction[['predicted_capacity','predicted_cc_fraction','logistic_score']]).all().all(),'new_predictions_finite')
        require(not prediction[[c for c in prediction if c.endswith('_seen_in_training')]].any().any(),'new_identifiers_unseen_in_training')
        check('saved_models_predict_12_unlabeled_new_identifiers')
        # The new EIS fixtures are copies of the training cells with identifiers shifted by 20.
        for column in ['capacity_predicted_defective','logistic_predicted_defective']:
            require((prediction[column].to_numpy(dtype=int)==labels.to_numpy()).all(),f'new_{column}_matches_fixture_truth')
        require(float(np.max(np.abs(prediction['predicted_capacity'].to_numpy()-truth['cap'].to_numpy())))<=3e-3,
                'new_predicted_capacity_stays_within_3e-3_Ah_of_fixture_truth')
        check('saved_models_reproduce_the_fixture_capacities_and_defect_decisions')
        report['status']='passed'
    except Exception as exc:
        report.update(status='failed',error_type=type(exc).__name__,error=str(exc))
        raise
    finally:
        report['finished_utc']=datetime.now(timezone.utc).isoformat()
        write_json(out/'release_verification.json',report)
    print(f'All release checks passed: {out}',flush=True)


if __name__=='__main__':
    main()
