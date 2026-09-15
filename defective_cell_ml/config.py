"""Configuration and shared validation. Importing this module writes nothing."""
from dataclasses import asdict, dataclass, field
from pathlib import Path
import hashlib
import codecs
import json
import math

VERSION = '2.0.0'

class DataError(ValueError):
    pass

class EvaluationError(ValueError):
    pass

@dataclass
class Config:
    threshold_ah: float = 0.01802088
    design_capacity_ah: float = 0.0200232
    area_cm2: float = 3.24
    cell_min: int = 34
    cell_max: int = 98
    exclude_cells: dict = field(default_factory=dict)
    frequency_grid_hz: list = field(default_factory=lambda: [0.01,0.1,1.,10.,100.,1000.,10000.,100000.,1000000.])
    boundary_policy: str = 'error'
    max_boundary_fraction: float = 0.05
    duplicate_frequency_policy: str = 'error'
    target_cycle: int = 1
    target_step_i: int = 1
    target_raw_step: int | None = None
    expected_current_sign: str = 'positive'
    cv_relative_drop: float = 0.01
    use_ocv: bool = True
    outer_cv: str = 'leave_one_cell_out'
    group_column: str = 'batch_id'
    inner_splits: int = 3
    seed: int = 2026
    ridge_alphas: list = field(default_factory=lambda: [0.001,0.01,0.1,1.,10.,100.,1000.])
    logistic_cs: list = field(default_factory=lambda: [0.001,0.01,0.1,1.,10.])
    logistic_class_weight: str | None = 'balanced'
    decision_threshold: float = 0.5
    feature_sets: list = field(default_factory=lambda: ['single_1e3','band_1e3_1e5','band_low','full'])
    encodings: list = field(default_factory=lambda: ['utf-8-sig','cp949'])

    def validate(self):
        for name in ['cell_min','cell_max','target_cycle','target_step_i','inner_splits','seed']:
            if type(getattr(self,name)) is not int or getattr(self,name)<0:
                raise DataError(f'{name} must be a nonnegative integer')
        if self.target_raw_step is not None and (type(self.target_raw_step) is not int or self.target_raw_step<0):
            raise DataError('target_raw_step must be a nonnegative integer or null')
        if self.seed>2**32-1 or type(self.use_ocv) is not bool:
            raise DataError('seed must fit uint32 and use_ocv must be a JSON boolean')
        if not isinstance(self.group_column,str) or not self.group_column.strip():
            raise DataError('group_column must be a nonempty name')
        if not isinstance(self.exclude_cells,dict):
            raise DataError('exclude_cells must map cell IDs to exclusion reasons')
        if not isinstance(self.encodings,list) or not self.encodings:
            raise DataError('encodings must be a nonempty list')
        try:
            for encoding in self.encodings:
                codecs.lookup(encoding)
        except (LookupError,TypeError) as exc:
            raise DataError('Unknown text encoding') from exc
        for name in ['threshold_ah','design_capacity_ah','area_cm2']:
            v=getattr(self,name)
            if type(v) not in (int,float) or not math.isfinite(v) or v<=0:
                raise DataError(f'{name} must be finite and positive')
        if not self.threshold_ah < self.design_capacity_ah:
            raise DataError('threshold_ah must be below design_capacity_ah')
        if self.cell_min>self.cell_max or self.inner_splits<2:
            raise DataError('Invalid cell range or inner_splits')
        if self.boundary_policy not in ['error','clamp'] or self.duplicate_frequency_policy not in ['error','mean']:
            raise DataError('Invalid frequency policy')
        if not 0<=self.max_boundary_fraction<=.1 or not 0<self.cv_relative_drop<1:
            raise DataError('Invalid tolerance')
        if not 0<self.decision_threshold<1:
            raise DataError('decision_threshold must be between 0 and 1')
        if self.outer_cv not in ['leave_one_cell_out','leave_one_group_out']:
            raise DataError('Invalid outer_cv')
        if self.expected_current_sign not in ['positive','negative']:
            raise DataError('expected_current_sign must be positive or negative')
        if self.logistic_class_weight not in [None,'balanced']:
            raise DataError('logistic_class_weight must be null or balanced')
        if not self.feature_sets or set(self.feature_sets)-{'single_1e3','band_1e3_1e5','band_low','full'}:
            raise DataError('Invalid feature_sets')
        for name in ['frequency_grid_hz','ridge_alphas','logistic_cs']:
            seq=getattr(self,name)
            if not seq or any(not isinstance(v,(int,float)) or not math.isfinite(v) or v<=0 for v in seq):
                raise DataError(f'{name} must contain positive finite numbers')
            if len(set(seq))!=len(seq):
                raise DataError(f'{name} has duplicates')
        if self.frequency_grid_hz!=sorted(self.frequency_grid_hz):
            raise DataError('frequency_grid_hz must increase')
        for cell,reason in self.exclude_cells.items():
            if str(int(cell))!=str(cell) or not isinstance(reason,str) or not reason.strip():
                raise DataError('exclude_cells requires integer IDs and nonempty reasons')
        return self

def load_config(path=None):
    if path is None:
        return Config().validate()
    data=json.loads(Path(path).read_text(encoding='utf-8-sig'))
    if not isinstance(data,dict):
        raise DataError('Configuration must be a JSON object')
    unknown=set(data)-set(Config.__dataclass_fields__)
    if unknown:
        raise DataError(f'Unknown config fields: {sorted(unknown)}')
    return Config(**data).validate()

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def jsonable(value):
    if hasattr(value,'item'):
        value=value.item()
    if isinstance(value,float) and not math.isfinite(value):
        return None
    if isinstance(value,Path):
        return str(value)
    if isinstance(value,dict):
        return {str(k):jsonable(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [jsonable(v) for v in value]
    return value

def write_json(path,data):
    Path(path).write_text(json.dumps(jsonable(data),ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')

def config_dict(cfg):
    return asdict(cfg)
