"""Nested selection of features and hyperparameters with explicit cell/group splits."""
import warnings
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin, clone
from sklearn.dummy import DummyRegressor
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import (confusion_matrix, f1_score, matthews_corrcoef, roc_auc_score,
                             log_loss, brier_score_loss)
from sklearn.model_selection import GridSearchCV, GroupKFold, KFold, LeaveOneGroupOut, LeaveOneOut, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from config import EvaluationError
from extract_capacity import FEATURE_RE

class FeatureSelector(TransformerMixin,BaseEstimator):
    def __init__(self,columns=None):
        self.columns=columns

    def fit(self,X,y=None):
        self.feature_names_in_=np.asarray(X.columns,dtype=object)
        self.n_features_in_=X.shape[1]
        if not self.columns or set(self.columns)-set(X.columns):
            raise EvaluationError('Selected features missing')
        return self

    def transform(self,X):
        return X.loc[:,list(self.columns)]

def band_columns(X,cfg):
    z=[c for c in X.columns if FEATURE_RE.fullmatch(c)]
    def frequency(c):
        return float(FEATURE_RE.fullmatch(c).group(2))
    available={
        'full':z,
        'single_1e3':[c for c in z if np.isclose(frequency(c),1000.,rtol=1e-10)],
        'band_1e3_1e5':[c for c in z if 1e3<=frequency(c)<=1e5],
        'band_low':[c for c in z if .1<=frequency(c)<=10.],
    }
    result=[]
    seen=set()
    for name in cfg.feature_sets:
        columns=available[name]
        if not columns:
            continue
        for ocv in [False,True] if cfg.use_ocv else [False]:
            selected=tuple(columns+(['ocv'] if ocv else []))
            if selected not in seen:
                result.append((name+('_ocv' if ocv else ''),selected))
                seen.add(selected)
    if not result:
        raise EvaluationError('No configured feature sets are available')
    return result

def candidate_grid(X,cfg,kind):
    bands=band_columns(X,cfg)
    grid=[]
    if kind=='regression':
        # Baselines also compete only inside inner CV, not on outer results.
        grid.append({'select__columns':[(X.columns[0],)],'model':[DummyRegressor(strategy='mean')]})
        for col in ['mag@1000Hz']+(['ocv'] if cfg.use_ocv else []):
            if col in X:
                grid.append({'select__columns':[(col,)],'model':[LinearRegression()]})
        for _,columns in bands:
            grid.append({'select__columns':[columns],'model':[Ridge()], 'model__alpha':cfg.ridge_alphas})
    else:
        for _,columns in bands:
            grid.append({'select__columns':[columns],
                         'model':[LogisticRegression(max_iter=10000,solver='lbfgs',class_weight=cfg.logistic_class_weight,random_state=cfg.seed)],
                         'model__C':cfg.logistic_cs})
    return grid

def outer_splits(X,y,cfg,groups=None):
    if len(X)<4:
        raise EvaluationError('At least 4 independent cells required; this is an execution minimum, not evidence of adequacy')
    if cfg.outer_cv=='leave_one_group_out':
        if groups is None or len(np.unique(groups))<3:
            raise EvaluationError('Nested group evaluation requires at least 3 groups')
        return list(LeaveOneGroupOut().split(X,y,groups))
    return list(LeaveOneOut().split(X,y))

def inner_splits(X,y,cfg,kind,groups=None):
    if kind=='classification' and len(np.unique(y))!=2:
        raise EvaluationError('Training partition has only one class; classification unavailable')
    if cfg.outer_cv=='leave_one_group_out':
        count=len(np.unique(groups))
        for k in range(min(cfg.inner_splits,count),1,-1):
            folds=list(GroupKFold(n_splits=k).split(X,y,groups))
            if kind=='regression' or all(len(np.unique(y[a]))==2 and len(np.unique(y[b]))==2 for a,b in folds):
                return folds
        raise EvaluationError('No valid inner group split with both classes; groups are not split to force a score')
    if kind=='classification':
        count=int(np.bincount(np.asarray(y,dtype=int),minlength=2).min())
        k=min(cfg.inner_splits,count)
        if k<2:
            raise EvaluationError('Too few minority cells for inner classification validation')
        return list(StratifiedKFold(k,shuffle=True,random_state=cfg.seed).split(X,y))
    if len(X)<2:
        raise EvaluationError('Too few training cells for inner regression validation')
    return list(KFold(min(cfg.inner_splits,len(X)),shuffle=True,random_state=cfg.seed).split(X))

def describe(model):
    estimator=model.named_steps['model']
    return {'estimator':type(estimator).__name__,'features':list(model.named_steps['select'].columns),
            'alpha':getattr(estimator,'alpha',None),'C':getattr(estimator,'C',None)}

def select_model(X,y,ids,cfg,kind,groups=None):
    folds=inner_splits(X,y,cfg,kind,groups)
    pipe=Pipeline([('select',FeatureSelector()),('scale',StandardScaler()),
                   ('model',Ridge() if kind=='regression' else LogisticRegression())])
    search=GridSearchCV(pipe,candidate_grid(X,cfg,kind),
                        scoring='neg_mean_squared_error' if kind=='regression' else 'neg_log_loss',
                        cv=folds,refit=True,error_score='raise',n_jobs=1,return_train_score=False)
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter('always')
        warnings.filterwarnings('error',category=ConvergenceWarning)
        search.fit(X,np.asarray(y))
    scores=np.asarray(search.cv_results_['mean_test_score'])
    if not np.isfinite(scores).all():
        raise EvaluationError('Nonfinite inner validation scores; selection rejected')
    selected=describe(search.best_estimator_)
    trace={'training_cells':list(map(int,ids)),'selected':selected,
           'inner_metric':'negative_MSE' if kind=='regression' else 'negative_log_loss',
           'best_inner_score':float(search.best_score_),'candidate_count':len(scores),
           'warnings':[str(w.message) for w in captured],
           'inner_folds':[{'train_cells':list(map(int,np.asarray(ids)[a])),
                           'validation_cells':list(map(int,np.asarray(ids)[b])),
                           'train_groups':list(map(str,np.unique(np.asarray(groups)[a]))) if groups is not None else [],
                           'validation_groups':list(map(str,np.unique(np.asarray(groups)[b]))) if groups is not None else []}
                          for a,b in folds],
           'scaler_mean':search.best_estimator_.named_steps['scale'].mean_.tolist()}
    return search.best_estimator_,trace

def regression_metrics(y,pred):
    y=np.asarray(y); pred=np.asarray(pred)
    residual=y-pred
    sst=float(np.sum((y-y.mean())**2))
    return {'n_samples':len(y),'Q2':float(1-np.sum(residual**2)/sst) if sst>0 else None,
            'RMSE':float(np.sqrt(np.mean(residual**2))),'MAE':float(np.mean(np.abs(residual))),
            'MAPE_pct':float(np.mean(np.abs(residual[np.abs(y)>=1e-3]/y[np.abs(y)>=1e-3]))*100) if np.any(np.abs(y)>=1e-3) else None}

def classification_metrics(y,pred,score,probabilities=False):
    y=np.asarray(y,dtype=int); pred=np.asarray(pred,dtype=int); score=np.asarray(score)
    tn,fp,fn,tp=map(int,confusion_matrix(y,pred,labels=[0,1]).ravel())
    both=len(np.unique(y))==2
    result={'n_samples':len(y),'TP':tp,'FN':fn,'FP':fp,'TN':tn,
            'sensitivity':tp/(tp+fn) if tp+fn else None,
            'specificity':tn/(tn+fp) if tn+fp else None,
            'precision':tp/(tp+fp) if tp+fp else None,'accuracy':(tp+tn)/len(y),
            'F1':float(f1_score(y,pred,zero_division=0)),
            'MCC':float(matthews_corrcoef(y,pred)) if both else None,
            'AUC_pooled_OOF':float(roc_auc_score(y,score)) if both else None}
    if probabilities:
        result.update(log_loss=float(log_loss(y,score,labels=[0,1])),
                      brier_score=float(brier_score_loss(y,score)))
    return result

def nested_evaluate(X,y,ids,cfg,kind='regression',groups=None):
    y=np.asarray(y)
    ids=np.asarray(ids)
    pred=np.full(len(y),np.nan)
    traces=[]
    for number,(train,test) in enumerate(outer_splits(X,y,cfg,groups),1):
        if set(ids[train])&set(ids[test]):
            raise EvaluationError('Same cell in train and test')
        if groups is not None and cfg.outer_cv=='leave_one_group_out' and set(groups[train])&set(groups[test]):
            raise EvaluationError('Same group in train and test')
        model,trace=select_model(X.iloc[train],y[train],ids[train],cfg,kind,
                                 None if groups is None else np.asarray(groups)[train])
        if kind=='regression':
            pred[test]=model.predict(X.iloc[test])
        else:
            classes=model.named_steps['model'].classes_
            pred[test]=model.predict_proba(X.iloc[test])[:,list(classes).index(1)]
        trace.update(outer_fold=number,test_cells=list(map(int,ids[test])),
                     test_groups=list(map(str,np.unique(np.asarray(groups)[test]))) if groups is not None else [])
        traces.append(trace)
    if not np.isfinite(pred).all():
        raise EvaluationError('Incomplete/nonfinite OOF predictions')
    return pred,traces

def fixed_baselines(X,y,ids,cfg,groups=None):
    candidates=[('mean',DummyRegressor(),[X.columns[0]])]
    for col in ['mag@1000Hz']+(['ocv'] if cfg.use_ocv else []):
        if col in X:
            candidates.append((col,LinearRegression(),[col]))
    results=[]
    for name,estimator,columns in candidates:
        predictions=np.full(len(y),np.nan)
        for train,test in outer_splits(X,y,cfg,groups):
            model=Pipeline([('scale',StandardScaler()),('model',clone(estimator))])
            model.fit(X.iloc[train][columns],np.asarray(y)[train])
            predictions[test]=model.predict(X.iloc[test][columns])
        results.append((name,predictions,regression_metrics(y,predictions)))
    return results

if __name__=='__main__':
    from export_for_origin import main
    raise SystemExit(main())
