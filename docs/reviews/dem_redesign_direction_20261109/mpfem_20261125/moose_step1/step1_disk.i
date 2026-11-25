# MPFEM step 1 (MOOSE) - one disk pressed by two rigid frictionless plates. DEVELOPMENT DATA.
# 2D plane strain, finite-strain J2 (same objects as moose_wsl/rot_test.i).
# Design = mpfem_plan/step1_kratos_onedisk.md arm A3-J2; only the tool changed (Kratos -> MOOSE).
# NOT VALIDATED until the first WSL smoke run.  Mesh disk.msh from make_disk_msh.py.
# Mesh tags: quads 1 disk, 2 bottom plate, 3 top plate; edges 11/12 disk upper/lower half,
# 20/30 bottom/top plate contact face; nodes 13/14 disk boundary y>0 / y<0,
# 22/32 all bottom/top plate nodes, 41 x=0 line, 42 y=0 line (disk).
# Checks fixed before any run (C, P1, P2, P4, step1 doc section 4): check_step1.py.
E = 1e7          # disk Young's modulus [Pa]
nu = 0.45
sy = 4e5         # disk uniaxial yield [Pa], no hardening
E_plate = 1e10   # plates are elastic, but every plate node is prescribed (rigid)
nu_plate = 0.3
v = 2.5e-5       # each plate moves v per unit time toward the disk (Delta u / 2 per step)
penalty = 1e8    # node-face kinematic contact: scales only the gap row of the residual

[GlobalParams]
  displacements = 'disp_x disp_y'
  volumetric_locking_correction = true
[]

[Mesh]
  [file]
    type = FileMeshGenerator
    file = disk.msh
  []
  patch_update_strategy = auto
[]

[Variables]
  [disp_x]
    block = '1 2 3'
  []
  [disp_y]
    block = '1 2 3'
  []
[]

[AuxVariables]
  [force_x]
    block = '1 2 3'
  []
  [force_y]
    block = '1 2 3'
  []
  [sxx]
    order = CONSTANT
    family = MONOMIAL
    block = 1
  []
  [syy]
    order = CONSTANT
    family = MONOMIAL
    block = 1
  []
  [szz]
    order = CONSTANT
    family = MONOMIAL
    block = 1
  []
  [sxy]
    order = CONSTANT
    family = MONOMIAL
    block = 1
  []
  [svm]
    order = CONSTANT
    family = MONOMIAL
    block = 1
  []
[]

[Kernels]
  [sdx]
    type = StressDivergenceTensors
    variable = disp_x
    component = 0
    block = '1 2 3'
    use_displaced_mesh = true
    save_in = force_x
  []
  [sdy]
    type = StressDivergenceTensors
    variable = disp_y
    component = 1
    block = '1 2 3'
    use_displaced_mesh = true
    save_in = force_y
  []
[]

[AuxKernels]
  [sxx]
    type = RankTwoAux
    rank_two_tensor = stress
    variable = sxx
    index_i = 0
    index_j = 0
    block = 1
  []
  [syy]
    type = RankTwoAux
    rank_two_tensor = stress
    variable = syy
    index_i = 1
    index_j = 1
    block = 1
  []
  [szz]
    type = RankTwoAux
    rank_two_tensor = stress
    variable = szz
    index_i = 2
    index_j = 2
    block = 1
  []
  [sxy]
    type = RankTwoAux
    rank_two_tensor = stress
    variable = sxy
    index_i = 0
    index_j = 1
    block = 1
  []
  [svm]
    type = RankTwoScalarAux
    rank_two_tensor = stress
    variable = svm
    scalar_type = VonMisesStress
    block = 1
  []
[]

[Functions]
  [down]
    type = ParsedFunction
    expression = '-${v}*t'
  []
  [up]
    type = ParsedFunction
    expression = '${v}*t'
  []
[]

[BCs]
  [symx]
    type = DirichletBC
    variable = disp_x
    boundary = 41
    value = 0
  []
  [symy]
    type = DirichletBC
    variable = disp_y
    boundary = 42
    value = 0
  []
  [top_x]
    type = DirichletBC
    variable = disp_x
    boundary = 32
    value = 0
  []
  [top_y]
    type = FunctionDirichletBC
    variable = disp_y
    boundary = 32
    function = down
  []
  [bottom_x]
    type = DirichletBC
    variable = disp_x
    boundary = 22
    value = 0
  []
  [bottom_y]
    type = FunctionDirichletBC
    variable = disp_y
    boundary = 22
    function = up
  []
[]

[Contact]
  [top]
    primary = 30
    secondary = 11
    model = frictionless
    formulation = kinematic
    penalty = ${penalty}
  []
  [bottom]
    primary = 20
    secondary = 12
    model = frictionless
    formulation = kinematic
    penalty = ${penalty}
  []
[]

[Materials]
  [strain]
    type = ComputeFiniteStrain
    block = '1 2 3'
  []
  [elasticity_disk]
    type = ComputeIsotropicElasticityTensor
    youngs_modulus = ${E}
    poissons_ratio = ${nu}
    block = 1
  []
  [j2]
    type = IsotropicPlasticityStressUpdate
    yield_stress = ${sy}
    hardening_constant = 0
    block = 1
  []
  [stress_disk]
    type = ComputeMultipleInelasticStress
    inelastic_models = 'j2'
    block = 1
  []
  [elasticity_plate]
    type = ComputeIsotropicElasticityTensor
    youngs_modulus = ${E_plate}
    poissons_ratio = ${nu_plate}
    block = '2 3'
  []
  [stress_plate]
    type = ComputeFiniteStrainElasticStress
    block = '2 3'
  []
[]

[Preconditioning]
  [smp]
    type = SMP
    full = true
  []
[]

[Executioner]
  type = Transient
  solve_type = PJFNK
  petsc_options = '-snes_converged_reason'
  petsc_options_iname = '-pc_type -pc_factor_shift_type -pc_factor_shift_amount -mat_mffd_err'
  petsc_options_value = 'lu       NONZERO               1e-15                  1e-5'
  line_search = none
  nl_rel_tol = 1e-6
  nl_abs_tol = 2e-7
  nl_max_its = 30
  l_max_its = 100
  dt = 1
  dtmin = 1
  end_time = 407
  abort_on_solve_fail = true
[]

[Postprocessors]
  [F_top_y]
    type = NodalSum
    variable = force_y
    boundary = 13
  []
  [F_bot_y]
    type = NodalSum
    variable = force_y
    boundary = 14
  []
  [F_top_x]
    type = NodalSum
    variable = force_x
    boundary = 13
  []
  [F_bot_x]
    type = NodalSum
    variable = force_x
    boundary = 14
  []
  [R_symy_y]
    type = NodalSum
    variable = force_y
    boundary = 42
  []
  [R_symx_x]
    type = NodalSum
    variable = force_x
    boundary = 41
  []
  [u_top]
    type = AverageNodalVariableValue
    variable = disp_y
    boundary = 30
  []
  [u_bot]
    type = AverageNodalVariableValue
    variable = disp_y
    boundary = 20
  []
  [area]
    type = VolumePostprocessor
    block = 1
    use_displaced_mesh = true
  []
  [area_ref]
    type = VolumePostprocessor
    block = 1
  []
  [int_sxx]
    type = ElementIntegralVariablePostprocessor
    variable = sxx
    block = 1
    use_displaced_mesh = true
  []
  [int_syy]
    type = ElementIntegralVariablePostprocessor
    variable = syy
    block = 1
    use_displaced_mesh = true
  []
  [int_szz]
    type = ElementIntegralVariablePostprocessor
    variable = szz
    block = 1
    use_displaced_mesh = true
  []
  [int_sxy]
    type = ElementIntegralVariablePostprocessor
    variable = sxy
    block = 1
    use_displaced_mesh = true
  []
  [svm_max]
    type = ElementExtremeValue
    variable = svm
    block = 1
  []
  [nl_its]
    type = NumNonlinearIterations
  []
[]

[Outputs]
  file_base = out
  csv = true
  exodus = true
  print_linear_residuals = false
[]

[Debug]
  show_var_residual_norms = true
[]
