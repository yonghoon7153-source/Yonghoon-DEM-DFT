"""Pure synthetic geometry/control preparation. No file readers or run authority.

These functions are reference exercises, not registered T5/T11 qualification,
not a live DEM observer, and not a P2-to-ULPR adapter.
"""
import math
import random
from fractions import Fraction


def number(value, *, positive=False, nonnegative=False):
    try:
        finite = type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        finite = False
    if not finite:
        raise ValueError('finite built-in number required')
    if positive and value <= 0 or nonnegative and value < 0:
        raise ValueError('number outside required range')
    return value


def integer(value, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError('integer outside required range')
    return value


def sphere_lens(r, s, distance):
    """Intersection volume, including containment; no pair-sum union shortcut."""
    r, s = number(r, positive=True), number(s, positive=True)
    d = number(distance, nonnegative=True)
    if d <= abs(r-s):
        small = min(r, s)
        return number((4*math.pi/3)*small*small*small, nonnegative=True)
    scale = max(r, s, d)
    r, s, d = r/scale, s/scale, d/scale
    if d >= r + s:
        return 0.
    if d <= abs(r - s):
        coefficient = 4 * math.pi * min(r, s)**3 / 3
    else:
        coefficient = math.pi*(r+s-d)**2*(d*d+2*d*(r+s)-3*(r-s)**2)/(12*d)
    # Multiply by the scale only after the dimensionless lens expression.
    return number(coefficient*scale*scale*scale, nonnegative=True)


def contact_area(r, s, distance):
    """Geometric intersection-circle area, NOT force-law or electrical area.

Containment has no unique intersecting surface circle and is refused. The
provided built-in numbers are treated exactly; no physical contact tolerance is
introduced. A positive area outside finite, nonzero float range is refused.
"""
    r, s = number(r, positive=True), number(s, positive=True)
    d = number(distance, nonnegative=True)
    r, s, d = Fraction(r), Fraction(s), Fraction(d)
    if d >= r + s:
        return 0.
    if d <= abs(r - s):
        raise ValueError('contained/coincident surfaces have no contact circle')
    # Symmetric Heron product: 4*triangle_area^2/d^2 is circle_radius^2.
    # Exact products preserve small positive factors near either tangency and
    # across large radius ratios; subtracting two rounded squared radii does not.
    radius_squared = ((r+s+d)*(r+s-d)*(d+r-s)*(d-r+s))/(4*d*d)
    try:
        area = float(Fraction(math.pi)*radius_squared)
    except OverflowError as exc:
        raise ValueError('contact area outside representable float range') from exc
    return number(area, positive=True)


def sphere_below_plane(radius, plane_minus_center):
    r = number(radius, positive=True)
    z = number(plane_minus_center)
    h = min(2., max(0., z/r+1))
    return number(math.pi*h*h*(1-h/3)*r*r*r, nonnegative=True)


def wilson(hits, n, z):
    integer(n, 1)
    integer(hits)
    number(z, positive=True)
    number(z*z)
    if hits > n:
        raise ValueError('hits exceed planned samples')
    p = hits/n
    den = 1+z*z/n
    mid = (p+z*z/(2*n))/den
    half = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return (max(0., mid-half), min(1., mid+half))


def union_mc(spheres, box, n, seed):
    """IID box sampling of the union (every overlap order), clipped to box.

Reports plug-in standard error; this is not a deterministic 1-sigma gate.
Confidence level and coverage target belong to a separate registration.
"""
    integer(n, 2)
    integer(seed)
    if len(box) != 6 or not spheres:
        raise ValueError('nonempty sphere list and 3D box required')
    bounds = [number(v) for v in box]
    widths = [bounds[i+1]-bounds[i] for i in (0, 2, 4)]
    if min(widths) <= 0:
        raise ValueError('positive box extents required')
    volume = number(math.prod(widths), positive=True)
    clean = []
    for sphere in spheres:
        if len(sphere) != 4:
            raise ValueError('sphere must contain x,y,z,r')
        clean.append(tuple(number(v, positive=(i == 3)) for i, v in enumerate(sphere)))
    rng = random.Random(seed)
    hits = 0
    for _ in range(n):
        p = [bounds[2*i]+widths[i]*rng.random() for i in range(3)]
        hits += any(math.dist(p, s[:3]) <= s[3] for s in clean)
    fraction = hits/n
    return dict(hits=hits, planned=n, seed=seed, volume=volume*fraction,
                standard_error=volume*math.sqrt(fraction*(1-fraction)/n),
                estimator='IID_UNION_INDICATOR', qualification='NOT_RUN')


def coverage(intervals, truth):
    """Missing intervals count in the planned denominator, never discarded."""
    number(truth)
    if not intervals:
        raise ValueError('planned repetitions required')
    covered, missing = 0, 0
    for interval in intervals:
        if interval is None:
            missing += 1
            continue
        if len(interval) != 2:
            raise ValueError('two interval bounds required')
        lo, hi = map(number, interval)
        if lo > hi:
            raise ValueError('reversed interval')
        covered += lo <= truth <= hi
    return dict(covered=covered, planned=len(intervals), missing=missing,
                coverage=covered/len(intervals))


def target_force(pressure_mpa, area_deck_m2):
    # Physical MPa -> physical Pa -> deck pressure (stress scale 0.001).
    return number(number(pressure_mpa, positive=True)*number(area_deck_m2, positive=True)*1000,
                  positive=True)


def servo_velocity(force, target, kp, vmax):
    number(force, nonnegative=True)
    number(target, positive=True)
    number(kp, positive=True)
    number(vmax, positive=True)
    error = (target-force)/target
    if error == 0:
        return 0.
    # Saturate the dimensionless gain before multiplying by vmax: zero error
    # must never become inf*0 -> NaN -> a spurious full-speed command.
    fraction = min(1., kp*abs(error))
    return -math.copysign(vmax*fraction, error)


def servo_probe(a, *, delay=0, saturation=10., budget=100,
                tolerance=1e-6, divergence=10., consecutive=4):
    """Dimensionless toy plant e[n+1]=e[n]-a*clip(e[n-delay]).

Positive error -> downward command -> increasing compressive force.
Initial error=1 is synthetic. No mapping to actual bed stiffness is inferred.
The first tolerance-window hit is diagnostic only. Observe the whole declared
budget unless its divergence bound is crossed. At budget end, both the final
window and all errors awaiting delayed consumption must be within tolerance.
This is finite-budget observation, not permanent/asymptotic stability proof.
"""
    number(a, positive=True)
    integer(delay)
    integer(budget, 1)
    integer(consecutive, 1)
    number(saturation, positive=True)
    number(tolerance, positive=True)
    number(divergence, positive=True)
    if divergence <= 1 or tolerance >= 1:
        raise ValueError('synthetic bounds must surround initial error')
    errors, stable, first_window_hit = [1.], 0, None

    def report(status):
        observed_steps = len(errors)-1
        pending = errors[max(0, observed_steps-delay):]
        tail_stable = len(errors) >= consecutive and all(abs(e) <= tolerance for e in errors[-consecutive:])
        return dict(status=status, errors=errors, first_window_hit=first_window_hit,
                    declared_budget=budget, steps_observed=observed_steps,
                    complete_budget=observed_steps == budget,
                    delay_queue_within_tolerance=all(abs(e) <= tolerance for e in pending),
                    tail_within_tolerance=tail_stable,
                    stability_scope='DECLARED_SYNTHETIC_BUDGET_ONLY', physical_ready=False)

    for n in range(budget):
        observed = errors[max(0, n-delay)]
        action = max(-saturation, min(saturation, observed))
        error = errors[-1]-a*action
        errors.append(error)
        if not math.isfinite(error) or abs(error) > divergence:
            return report('UNSTABLE')
        stable = stable+1 if abs(error) <= tolerance else 0
        if first_window_hit is None and stable >= consecutive:
            first_window_hit = n+1
    result = report('NOT_CONVERGED')
    if result['tail_within_tolerance'] and result['delay_queue_within_tolerance']:
        result['status'] = 'SYNTHETIC_CONVERGED'
    return result


def static_guard(rows, target, rules):
    """Two complete adjacent synthetic windows; never grants physical readiness.

Scalar force/residual/KE fields must eventually be supplied by a qualified
observer; inventory label is a synthetic fixture token, NOT identity evidence.
This does not assess torque, epsilon/height drift, cut-plane balance or S1-S4.
"""
    number(target, positive=True)
    n = integer(rules['samples_per_window'], 2)
    stride = integer(rules['sample_stride'], 1)
    max_ke = number(rules['max_ke'], positive=True)
    drift = number(rules['max_drift_fraction'], nonnegative=True)
    token = rules['expected_inventory']
    if type(token) is not str or not token:
        raise ValueError('explicit synthetic inventory token required')
    if len(rows) != 2*n:
        return dict(status='INCOMPLETE', physical_ready=False)
    forces = []
    previous = None
    for row in rows:
        try:
            step = integer(row['step'], 1)
            if previous is not None and step != previous+stride:
                raise ValueError('nonadjacent samples')
            previous = step
            force = number(row['force'], nonnegative=True)
            ke = number(row['ke'], nonnegative=True)
            residual = abs(number(row['residual']))
            damping = abs(number(row['damping']))
            inertia = abs(number(row['inertia']))
            escaped = integer(row['escaped'])
            if (row['inventory'] != token or row['contacts_complete'] is not True or escaped or
                    abs(force/target-1) > .01 or ke > max_ke or
                    residual/target > .01 or damping/target > .001 or inertia/target > .001):
                raise ValueError('static predicate failed')
            forces.append(force)
        except (KeyError, ValueError, TypeError):
            return dict(status='REJECTED', physical_ready=False)
    means = [sum(forces[i:i+n])/n for i in (0, n)]
    if any(abs(m/target-1) > .005 for m in means) or abs(means[1]-means[0])/target > drift:
        return dict(status='NOT_CONVERGED', physical_ready=False)
    return dict(status='SYNTHETIC_STATIC', physical_ready=False)


def inventory_guard(particles, expected, bottom, top, max_surface_penetration):
    """Synthetic horizontal-plane check; no STL/PBC/path-history qualification.

The full expected ID/type/radius/mass map must be explicit. Center crossing is
always refused; surface cuts are counted separately and require an explicit
penetration bound (no default scientific threshold). Relative clearances and
penetration use the exact stored int/float values, with no origin-dependent
epsilon. Precision already lost before the call cannot be reconstructed; this
does not certify an intended physical geometry from rounded coordinates.
"""
    number(bottom)
    number(top)
    number(max_surface_penetration, nonnegative=True)
    if top <= bottom or type(expected) is not dict or not expected:
        raise ValueError('bounded plane geometry and fixed inventory required')
    lower, upper, limit = Fraction(bottom), Fraction(top), Fraction(max_surface_penetration)
    for ident, identity in expected.items():
        integer(ident, 1)
        if type(identity) is not dict or set(identity) != {'type', 'radius', 'mass'}:
            raise ValueError('complete expected identity required')
        integer(identity['type'], 1)
        number(identity['radius'], positive=True)
        number(identity['mass'], positive=True)
    seen, cuts = set(), 0
    try:
        for particle in particles:
            if type(particle) is not dict or set(particle) != {'id', 'type', 'radius', 'mass', 'x', 'y', 'z'}:
                raise ValueError('complete synthetic particle required')
            ident = integer(particle['id'], 1)
            if ident in seen or ident not in expected:
                raise ValueError('duplicate or unexpected ID')
            seen.add(ident)
            integer(particle['type'], 1)
            radius = number(particle['radius'], positive=True)
            number(particle['mass'], positive=True)
            for axis in ('x', 'y', 'z'):
                number(particle[axis])
            if any(particle[k] != v for k, v in expected[ident].items()):
                raise ValueError('type/radius/mass identity mismatch')
            z, exact_radius = Fraction(particle['z']), Fraction(radius)
            lower_clearance, upper_clearance = z-lower, upper-z
            penetration = max(exact_radius-lower_clearance, exact_radius-upper_clearance, 0)
            if not lower <= z <= upper or penetration > limit:
                raise ValueError('center crossing or excessive surface penetration')
            cuts += penetration > 0
        if seen != set(expected):
            raise ValueError('missing ID')
    except (TypeError, ValueError, KeyError):
        return dict(status='REJECTED', physical_ready=False)
    return dict(status='SYNTHETIC_CONSERVED', surface_cut_count=cuts, physical_ready=False)
