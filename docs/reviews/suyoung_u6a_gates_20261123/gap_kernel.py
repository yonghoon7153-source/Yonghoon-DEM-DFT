"""Setting 2: permit existing shared-node pairs to close their current normal gap in a step."""
import ast
import hashlib
from pathlib import Path
from types import ModuleType

import numpy as np


BASE_KERNEL = "acf5c061032672adb8301fc6b45750c188f8fdc2892350cb7956b64c433f2645"
PAIR_MATERIAL = "6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4"
VERTICES = 256


def _source(path, expected):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError("gap operator source identity: " + path.name)
    return raw.decode("utf8")


def _replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError("pinned source anchor changed: " + old)
    return text.replace(old, new, 1)


def _pair_function(text):
    # The Coulomb bound uses the shifted normal impulse, while the slip
    # vector uses the physical relative velocity, including its normal part.
    func = next(n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == "pair_impulse")
    source = ast.get_source_segment(text, func)
    source = _replace_once(source, "normal,friction):", "normal,friction,allowance):")
    source = _replace_once(source, "np.maximum(closing,0)", "np.maximum(closing-allowance,0)")
    env = {"np": np}
    exec(compile(source, "<gap_corrected_isolated_pair>", "exec"), env)
    return env["pair_impulse"]


def _derived_kernel(path):
    """Change only the nonpenetration speed offset in the pinned solver.

    Both the iterative complementarity residual and every fallback active
    face must use the same offset, including the final nonlinear face check.
    The shared-node list, normal, friction law, face search, tolerances,
    energy guard and deferred updates are taken from the original source.
    """
    source = _source(path, BASE_KERNEL)
    material = _source(path.with_name("dem_suyoung_sf2d_dev.py"), PAIR_MATERIAL)
    changes = (
        ("_pair_impulse = _load_pair_impulse()", "# isolated-pair function supplied from the checked material source"),
        ("mu, jn, jt, guess_n, guess_t_raw, speed_tol):", "mu, jn, jt, guess_n, guess_t_raw, speed_tol, allowance):"),
        ("initial_closing = -(jacobian @ incoming.ravel())",
         "initial_closing = -(jacobian @ incoming.ravel())\n    initial_closing[::2] -= allowance"),
        ("closing, slip = (-(jacobian @ v.ravel())).reshape(-1, 2).T",
         "closing, slip = (-(jacobian @ v.ravel())).reshape(-1, 2).T\n        closing = closing - allowance"),
        ("def _simultaneous(incoming, mass, left, right, normal, mu):",
         "def _simultaneous(incoming, mass, left, right, normal, mu, allowance):"),
        ('closing = np.einsum("npi,npi->np", relative, normal)',
         'closing = np.einsum("npi,npi->np", relative, normal) - allowance'),
        ("jt[idx] + slip[idx], speed_tol[idx])", "jt[idx] + slip[idx], speed_tol[idx], allowance[idx])"),
        ("def project_contacts(ids, nodes, mass, grad, vel, centers, friction):",
         "def project_contacts(ids, nodes, mass, grad, vel, centers, friction, pair_limits):"),
        ("normal = _normals(rows, left, right, ids, mass, grad, centers)",
         "normal = _normals(rows, left, right, ids, mass, grad, centers)\n"
         "        allowance = pair_limits(ids[rows[:, left]], ids[rows[:, right]], normal)"),
        ("vel[a], vel[b], normal[:, 0], friction)", "vel[a], vel[b], normal[:, 0], friction, allowance[:, 0])"),
        ("result = _simultaneous(vel[rows], mass[rows], left, right, normal, friction)",
         "result = _simultaneous(vel[rows], mass[rows], left, right, normal, friction, allowance)"),
    )
    for old, new in changes:
        source = _replace_once(source, old, new)
    module = ModuleType("setting_two_shared_node_contact")
    module.__file__ = str(path)
    module._pair_impulse = _pair_function(material)
    exec(compile(source, str(path), "exec"), module.__dict__)
    return module


class GapProjector:
    def __init__(self, kernel):
        self.derived = _derived_kernel(Path(kernel.__file__).resolve())
        self.calls = 0

    def metadata(self):
        return dict(setting=2, cell_size_gap_correction=True, distance_based_contact_detection=False,
                    gap_law="positive_projected_support_gap_over_dt", boundary_vertices_per_body=VERTICES,
                    normal="pinned_field_mass_gradient_b_minus_a_with_center_fallback",
                    base_kernel_sha256=BASE_KERNEL, pair_material_sha256=PAIR_MATERIAL, calls=self.calls)

    def project(self, boundary, dt, ids, nodes, mass, grad, vel, centers, friction):
        if not np.isfinite(dt) or dt <= 0.:
            raise ValueError("invalid contact time step")
        groups = np.asarray(boundary.groups)
        positions = np.asarray(boundary.positions)
        n = len(centers)
        if (not n or groups.dtype.kind not in "iu" or groups.shape != (n*VERTICES,)
                or positions.shape != (n*VERTICES, 2) or not np.isfinite(positions).all()
                or not np.array_equal(groups, np.repeat(np.arange(n), VERTICES))):
            raise ValueError("expected 256 transported, body-ordered boundary vertices per field")
        if np.any(ids < 0) or np.any(ids >= n):
            raise ValueError("field not bound to material surface")
        vertices = positions.reshape(n, VERTICES, 2)

        def pair_limits(left, right, normals):
            # Every node/pair remains eligible. Projection of the two entire
            # polygons gives a conservative separating-plane gap along n.
            shape = left.shape
            a, b, direction = left.ravel(), right.ravel(), normals.reshape(-1, 2)
            result = np.empty(len(a), dtype=float)
            # Batching only bounds scratch memory; no surface vertex is sampled out.
            for start in range(0, len(a), 128):
                chunk = slice(start, start+128)
                v_a = np.einsum("nvd,nd->nv", vertices[a[chunk]], direction[chunk])
                v_b = np.einsum("nvd,nd->nv", vertices[b[chunk]], direction[chunk])
                gap = v_b.min(axis=1) - v_a.max(axis=1)
                result[chunk] = np.maximum(gap, 0.)/dt
            if not np.isfinite(result).all():
                raise ArithmeticError("nonfinite gap allowance")
            return result.reshape(shape)

        self.derived.project_contacts(ids, nodes, mass, grad, vel, centers, friction, pair_limits)
        self.calls += 1
