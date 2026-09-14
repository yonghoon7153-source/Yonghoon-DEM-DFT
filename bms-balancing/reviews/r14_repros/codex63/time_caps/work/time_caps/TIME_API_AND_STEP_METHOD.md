# Supported expression cap and actual-step verification

Source checked on 2026-09-13: [COMSOL 6.3 Time API](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_solver.51.50.html).

The Time API supports `maxstepconstraintbdf=expr` with `maxstepexpressionbdf` evaluated during solving. `maxstepbdf` controls the constant mode and is an inactive slot in these new cases. The unchanged `strict` mode includes requested tlist times; `tout=tsteps`, `tstepsstore=1` stores each accepted step.

The four Java sources set either `if(t<0.1[s],0.001[s],0.1[s])` or `if(t<0.1[s],0.0005[s],0.1[s])`. At t=0.1 the expression's relaxed branch is selected. The existing 187-point tlist includes exactly 0.1 s. The API does not document the internal point at which t is evaluated when a prospective step is selected; the audit does not infer that point.

The actual-step audit uses differences of consecutive native stored times, checks corresponding native step row counts and rounded log times, and excludes the CDI/consistent-initialization t=0 state from interval counts. It separates steps before 0.1, the interval arriving at 0.1, and intervals starting at/after 0.1. Early intervals including arrival must meet the smaller cap; later intervals must meet 0.1 s. A missing stored boundary with a crossing interval is flagged separately. A 1e-12 s tolerance allows printed floating-point roundoff only. Actual early cap-binding counts, growth after relaxation, and the interval arriving at 0.04 are retained.

An accepted-step size bound does not prove the nonlinear trial history satisfies a concentration guard. OCP input and solid-surface bounds are unchanged runtime StopConditions; electrolyte positivity remains postprocessing only.

The numerical comparison uses only the four fresh cases and exact common requested times. Spatial profiles remain COMSOL FE interpolations at 241 prescribed coordinates/electrode with no temporal interpolation. All internal accepted steps are retained for the time-control audit, even though extra adaptive times are not used as unmatched comparison points.
