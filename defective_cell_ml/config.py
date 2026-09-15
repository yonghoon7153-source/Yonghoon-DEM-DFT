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
    cap_plausibility_factor: float = 10.
    area_cm2: float = 3.24
    cell_min: int = 34
    cell_max: int = 98
    exclude_cells: dict = field(default_factory=dict)
    frequency_grid_hz: list = field(default_factory=lambda: [0.01,0.1,1.,10.,100.,1000.,10000.,100000.,1000000.])
    boundary_policy: str = 'error'
    max_boundary_fraction: float = 0.05
    duplicate_frequency_policy: str = 'error'
    mean_max_ewe_spread_v: float | None = None
    eis_sweep: str | int = 'all'
    target_cycle: int = 1
    target_step_i: int = 1
    target_raw_step: int | None = None
    expected_current_sign: str = 'positive'
    cv_relative_drop: float = 0.01
    cc_reference_rows: int = 5
    cc_sustained_rows: int = 3
    trim_zero_current_boundary_rows: bool = False
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
    encodings: list = field(default_factory=lambda: ['utf-8-sig','cp949','cp1252'])

    def validate(self):
        for name in ['cell_min','cell_max','target_cycle','target_step_i','inner_splits','seed',
                     'cc_reference_rows','cc_sustained_rows']:
            value=getattr(self,name)
            if type(value) is not int or value<0:
                raise DataError(f'{name}={value!r} must be a nonnegative integer')
        if self.target_raw_step is not None and (type(self.target_raw_step) is not int or self.target_raw_step<0):
            raise DataError(f'target_raw_step={self.target_raw_step!r} must be a nonnegative integer or null')
        if self.seed>2**32-1:
            raise DataError(f'seed={self.seed} must fit in uint32')
        for name in ['use_ocv','trim_zero_current_boundary_rows']:
            if type(getattr(self,name)) is not bool:
                raise DataError(f'{name}={getattr(self,name)!r} must be a JSON boolean (true/false, unquoted)')
        if not isinstance(self.group_column,str) or not self.group_column.strip():
            raise DataError(f'group_column={self.group_column!r} must be a nonempty name')
        if not isinstance(self.exclude_cells,dict):
            raise DataError('exclude_cells must map cell IDs to exclusion reasons')
        if not isinstance(self.encodings,list) or not self.encodings:
            raise DataError('encodings must be a nonempty list of text codecs')
        for encoding in self.encodings:
            try:
                codec=codecs.lookup(encoding)
            except (LookupError,TypeError) as exc:
                raise DataError(f'Unknown text encoding: {encoding!r}') from exc
            # bytes<->bytes codecs (zlib, base64) pass codecs.lookup but cannot decode a file.
            if not getattr(codec,'_is_text_encoding',True):
                raise DataError(f'encodings entry {encoding!r} is not a text encoding; '
                                'use a text codec such as "utf-8-sig", "cp949" or "cp1252"')
        for name in ['threshold_ah','design_capacity_ah','area_cm2','max_boundary_fraction','cv_relative_drop',
                     'decision_threshold','cap_plausibility_factor']:
            value=getattr(self,name)
            if type(value) not in (int,float) or not math.isfinite(value):
                raise DataError(f'{name}={value!r} must be a finite number')
        for name in ['threshold_ah','design_capacity_ah','area_cm2']:
            if getattr(self,name)<=0:
                raise DataError(f'{name}={getattr(self,name)!r} must be positive')
        if not self.threshold_ah < self.design_capacity_ah:
            raise DataError(f'threshold_ah={self.threshold_ah!r} must be below design_capacity_ah={self.design_capacity_ah!r}')
        if self.cap_plausibility_factor<=1:
            raise DataError(f'cap_plausibility_factor={self.cap_plausibility_factor!r} must be greater than 1')
        if self.cell_min>self.cell_max:
            raise DataError(f'cell_min={self.cell_min} must not exceed cell_max={self.cell_max}')
        if self.inner_splits<2:
            raise DataError(f'inner_splits={self.inner_splits} must be at least 2')
        if self.cc_reference_rows<1 or self.cc_sustained_rows<1:
            raise DataError(f'cc_reference_rows={self.cc_reference_rows} and '
                            f'cc_sustained_rows={self.cc_sustained_rows} must be at least 1')
        if self.boundary_policy not in ['error','clamp']:
            raise DataError(f'boundary_policy={self.boundary_policy!r} must be "error" or "clamp"')
        if self.duplicate_frequency_policy not in ['error','mean']:
            raise DataError(f'duplicate_frequency_policy={self.duplicate_frequency_policy!r} must be "error" or "mean"')
        if self.mean_max_ewe_spread_v is not None and (type(self.mean_max_ewe_spread_v) not in (int,float)
                or not math.isfinite(self.mean_max_ewe_spread_v) or self.mean_max_ewe_spread_v<0):
            raise DataError(f'mean_max_ewe_spread_v={self.mean_max_ewe_spread_v!r} must be null or '
                            'a nonnegative number of volts')
        if self.eis_sweep not in ['all','first','last'] and not (type(self.eis_sweep) is int and self.eis_sweep>=0):
            raise DataError(f'eis_sweep={self.eis_sweep!r} must be "all", "first", "last" or a nonnegative sweep index')
        if not 0<=self.max_boundary_fraction<=.1:
            raise DataError(f'max_boundary_fraction={self.max_boundary_fraction!r} must be within [0, 0.1]')
        if not 0<self.cv_relative_drop<1:
            raise DataError(f'cv_relative_drop={self.cv_relative_drop!r} must be within (0, 1)')
        if not 0<self.decision_threshold<1:
            raise DataError(f'decision_threshold={self.decision_threshold!r} must be within (0, 1)')
        if self.outer_cv not in ['leave_one_cell_out','leave_one_group_out']:
            raise DataError(f'outer_cv={self.outer_cv!r} must be leave_one_cell_out or leave_one_group_out')
        if self.expected_current_sign not in ['positive','negative']:
            raise DataError(f'expected_current_sign={self.expected_current_sign!r} must be positive or negative')
        if self.logistic_class_weight not in [None,'balanced']:
            raise DataError(f'logistic_class_weight={self.logistic_class_weight!r} must be null or "balanced"')
        if not self.feature_sets or set(self.feature_sets)-{'single_1e3','band_1e3_1e5','band_low','full'}:
            raise DataError(f'feature_sets={self.feature_sets!r} must be a nonempty subset of '
                            '["single_1e3", "band_1e3_1e5", "band_low", "full"]')
        for name in ['frequency_grid_hz','ridge_alphas','logistic_cs']:
            seq=getattr(self,name)
            if not isinstance(seq,list) or not seq or any(type(v) not in (int,float) or not math.isfinite(v) or v<=0 for v in seq):
                raise DataError(f'{name}={seq!r} must be a nonempty list of positive finite numbers')
            if len(set(seq))!=len(seq):
                raise DataError(f'{name}={seq!r} has duplicates')
        if self.frequency_grid_hz!=sorted(self.frequency_grid_hz):
            raise DataError(f'frequency_grid_hz={self.frequency_grid_hz!r} must increase')
        for cell,reason in self.exclude_cells.items():
            key=str(cell)
            if not (key.isascii() and key.isdigit()) or key!=str(int(key)) or not isinstance(reason,str) or not reason.strip():
                raise DataError(f'exclude_cells[{cell!r}]={reason!r} requires an integer cell ID '
                                'without leading zeros and a nonempty reason')
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
