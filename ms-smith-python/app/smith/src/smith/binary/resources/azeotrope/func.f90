SUBROUTINE F2(x, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, y)
	USE mod_F2d
  IMPLICIT NONE

  INTEGER, INTENT(IN) :: npars_p, npars_g
  CHARACTER(len=20), INTENT(IN) :: modelname_p, modelname_g
  DOUBLE PRECISION, DIMENSION(2), INTENT(IN) :: x
  DOUBLE PRECISION, DIMENSION(npars_p), INTENT(IN) :: pars_p
  DOUBLE PRECISION, DIMENSION(npars_g), INTENT(IN) :: pars_g
  DOUBLE PRECISION, DIMENSION(2), INTENT(OUT) :: y

	call F2_C(x, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, y)

END SUBROUTINE F2

SUBROUTINE F2_JAC(x, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, jac)
	USE mod_F2d
  IMPLICIT NONE

  INTEGER, INTENT(IN) :: npars_p, npars_g
  CHARACTER(len=20), INTENT(IN) :: modelname_p, modelname_g
  DOUBLE PRECISION, DIMENSION(2), INTENT(IN) :: x
  DOUBLE PRECISION, DIMENSION(npars_p), INTENT(IN) :: pars_p
  DOUBLE PRECISION, DIMENSION(npars_g), INTENT(IN) :: pars_g
  DOUBLE PRECISION, DIMENSION(2,2), INTENT(OUT) :: jac

  ! local variables
  INTEGER :: n
  INTEGER :: i
  double precision :: y(2), xd(2)

  n = 2

  xd = 0d0
  DO i=1,n,1
    xd(i) = 1d0
    call F2_D(x, xd, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, y, jac(:,i))
    xd(i) = 0d0
  END DO

END SUBROUTINE F2_JAC
