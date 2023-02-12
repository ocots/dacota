SUBROUTINE FCURVE(x, beta, modelname_p, npars_p, pars_p&
	& , modelname_g, npars_g, pars_g, indi, indj, y)
  USE MOD_CURVE
  IMPLICIT NONE
  INTEGER, INTENT(IN) :: npars_p, npars_g, indi, indj
  CHARACTER(len=20), INTENT(IN) :: modelname_p, modelname_g
  DOUBLE PRECISION, DIMENSION(2), INTENT(IN) :: x
  DOUBLE PRECISION, INTENT(IN) :: beta
  DOUBLE PRECISION, DIMENSION(npars_p), INTENT(IN) :: pars_p
  DOUBLE PRECISION, DIMENSION(npars_g), INTENT(IN) :: pars_g
  DOUBLE PRECISION, DIMENSION(2), INTENT(OUT) :: y

  CALL FCURVE_C(x, beta, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, indi, indj, y)

END SUBROUTINE FCURVE


SUBROUTINE FCURVE_JAC(x, beta, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, indi, indj, dfdx, dfdb)
  USE MOD_CURVE
  IMPLICIT NONE

  INTEGER, INTENT(IN) :: npars_p, npars_g, indi, indj
  CHARACTER(len=20), INTENT(IN) :: modelname_p, modelname_g
  DOUBLE PRECISION, DIMENSION(2), INTENT(IN) :: x
  DOUBLE PRECISION, INTENT(IN) :: beta
  DOUBLE PRECISION, DIMENSION(npars_p), INTENT(IN) :: pars_p
  DOUBLE PRECISION, DIMENSION(npars_g), INTENT(IN) :: pars_g
  DOUBLE PRECISION, DIMENSION(2,2), INTENT(OUT) :: dfdx
  DOUBLE PRECISION, DIMENSION(2,1), INTENT(OUT) :: dfdb

  ! local variable
  INTEGER :: n
  INTEGER :: i
  double precision :: y(2), xd(2), betad

 ! Calcul df_curve/dx

  n = 2
  xd = 0d0
  betad = 0d0
  DO i=1,n,1
    xd(i) = 1d0
    call FCURVE_D(x, xd, beta, betad, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, indi, indj, y, dfdx(:,i))
    xd(i) = 0d0
  END DO

  ! Calcul df_curve/dbeta
  xd = 0d0
  betad = 1d0
  call FCURVE_D(x, xd, beta, betad, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, indi, indj, y, dfdb)

END SUBROUTINE FCURVE_JAC
