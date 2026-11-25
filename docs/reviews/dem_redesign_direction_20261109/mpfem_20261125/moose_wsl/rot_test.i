# MPFEM step 1 (MOOSE) - rotation check after plastic flow (development data, 1저자 11-25 (가-1)).
# Single HEX8 element, all nodes prescribed (homogeneous F = Q(th) diag(1/ly, ly, 1)).
# t 0..100 : isochoric plane-strain compression, ly 1 -> 0.85
# t 100..400: rigid rotation 0 -> 30 deg about z in 300 steps
# Criteria fixed before the run: R1 back-rotated stress diff <= 1e-3 sy ; R2 von Mises at t=100 within 2 % of sy
E = 1e7
nu = 0.45
sy = 4e5

[GlobalParams]
  displacements = 'disp_x disp_y disp_z'
[]

[Mesh]
  [gen]
    type = GeneratedMeshGenerator
    dim = 3
    nx = 1
    ny = 1
    nz = 1
  []
[]

[Variables]
  [disp_x]
  []
  [disp_y]
  []
  [disp_z]
  []
[]

[Kernels]
  [sdx]
    type = StressDivergenceTensors
    variable = disp_x
    component = 0
    use_displaced_mesh = true
  []
  [sdy]
    type = StressDivergenceTensors
    variable = disp_y
    component = 1
    use_displaced_mesh = true
  []
  [sdz]
    type = StressDivergenceTensors
    variable = disp_z
    component = 2
    use_displaced_mesh = true
  []
[]

[Functions]
  [ly]
    type = ParsedFunction
    expression = 'if(t<=100, 1-0.15*t/100, 0.85)'
  []
  [th]
    type = ParsedFunction
    expression = 'if(t<=100, 0, 0.5235987755982988*(t-100)/300)'
  []
  [ux]
    type = ParsedFunction
    expression = 'cos(a)*x/b - sin(a)*b*y - x'
    symbol_names = 'b a'
    symbol_values = 'ly th'
  []
  [uy]
    type = ParsedFunction
    expression = 'sin(a)*x/b + cos(a)*b*y - y'
    symbol_names = 'b a'
    symbol_values = 'ly th'
  []
[]

[BCs]
  [bx]
    type = FunctionDirichletBC
    variable = disp_x
    boundary = 'left right bottom top back front'
    function = ux
  []
  [by]
    type = FunctionDirichletBC
    variable = disp_y
    boundary = 'left right bottom top back front'
    function = uy
  []
  [bz]
    type = DirichletBC
    variable = disp_z
    boundary = 'left right bottom top back front'
    value = 0
  []
[]

[Materials]
  [elasticity]
    type = ComputeIsotropicElasticityTensor
    youngs_modulus = ${E}
    poissons_ratio = ${nu}
  []
  [strain]
    type = ComputeFiniteStrain
  []
  [j2]
    type = IsotropicPlasticityStressUpdate
    yield_stress = ${sy}
    hardening_constant = 0
  []
  [stress]
    type = ComputeMultipleInelasticStress
    inelastic_models = 'j2'
  []
[]

[AuxVariables]
  [sxx]
    order = CONSTANT
    family = MONOMIAL
  []
  [syy]
    order = CONSTANT
    family = MONOMIAL
  []
  [szz]
    order = CONSTANT
    family = MONOMIAL
  []
  [sxy]
    order = CONSTANT
    family = MONOMIAL
  []
  [svm]
    order = CONSTANT
    family = MONOMIAL
  []
[]

[AuxKernels]
  [sxx]
    type = RankTwoAux
    rank_two_tensor = stress
    variable = sxx
    index_i = 0
    index_j = 0
  []
  [syy]
    type = RankTwoAux
    rank_two_tensor = stress
    variable = syy
    index_i = 1
    index_j = 1
  []
  [szz]
    type = RankTwoAux
    rank_two_tensor = stress
    variable = szz
    index_i = 2
    index_j = 2
  []
  [sxy]
    type = RankTwoAux
    rank_two_tensor = stress
    variable = sxy
    index_i = 0
    index_j = 1
  []
  [svm]
    type = RankTwoScalarAux
    rank_two_tensor = stress
    variable = svm
    scalar_type = VonMisesStress
  []
[]

[Postprocessors]
  [sxx]
    type = ElementAverageValue
    variable = sxx
  []
  [syy]
    type = ElementAverageValue
    variable = syy
  []
  [szz]
    type = ElementAverageValue
    variable = szz
  []
  [sxy]
    type = ElementAverageValue
    variable = sxy
  []
  [svm]
    type = ElementAverageValue
    variable = svm
  []
[]

[Executioner]
  type = Transient
  solve_type = NEWTON
  petsc_options_iname = '-pc_type'
  petsc_options_value = 'lu'
  dt = 1
  end_time = 400
  nl_abs_tol = 1e-6
  nl_rel_tol = 1e-10
[]

[Outputs]
  csv = true
[]
