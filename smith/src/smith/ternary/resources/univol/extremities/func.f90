
SUBROUTINE PHI(temperature, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, edge, alpha, y)

	  USE MOD_EXTREM
	  IMPLICIT NONE

	  INTEGER, INTENT(IN) :: npars_p, npars_g, edge
	  CHARACTER(len=20), INTENT(IN) :: modelname_p, modelname_g
	  DOUBLE PRECISION, INTENT(IN) :: temperature, alpha
	  DOUBLE PRECISION, DIMENSION(npars_p), INTENT(IN) :: pars_p
	  DOUBLE PRECISION, DIMENSION(npars_g), INTENT(IN) :: pars_g
	  DOUBLE PRECISION, INTENT(OUT) :: y

	  CALL PHI_C(temperature, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, edge, alpha, y)

END SUBROUTINE PHI

SUBROUTINE PSI(temperature, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, edge, alpha, indi, indj, y)

	  USE MOD_EXTREM
	  IMPLICIT NONE

	  INTEGER, INTENT(IN) :: npars_p, npars_g, edge, indi, indj
	  CHARACTER(len=20), INTENT(IN) :: modelname_p, modelname_g
	  DOUBLE PRECISION, INTENT(IN) :: temperature, alpha
	  DOUBLE PRECISION, DIMENSION(npars_p), INTENT(IN) :: pars_p
	  DOUBLE PRECISION, DIMENSION(npars_g), INTENT(IN) :: pars_g
	  DOUBLE PRECISION, INTENT(OUT) :: y

	  CALL PSI_C(temperature, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, edge, alpha, indi, indj, y)

END SUBROUTINE PSI

SUBROUTINE EXTREMITY(x, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, edge, indi, indj, y)

	USE MOD_EXTREM
	IMPLICIT NONE
	INTEGER, INTENT(IN) :: npars_p, npars_g, edge, indi, indj
	CHARACTER(len=20), INTENT(IN) :: modelname_p, modelname_g
	DOUBLE PRECISION, DIMENSION(2), INTENT(IN) :: x
	DOUBLE PRECISION, DIMENSION(npars_p), INTENT(IN) :: pars_p
	DOUBLE PRECISION, DIMENSION(npars_g), INTENT(IN) :: pars_g
	DOUBLE PRECISION, DIMENSION(2), INTENT(OUT) :: y

	CALL EXTREMITY_C(x, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, edge, indi, indj, y)

END SUBROUTINE EXTREMITY

SUBROUTINE PHI_JAC(temperature, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, edge, alpha, jac)
	USE MOD_EXTREM
	IMPLICIT NONE

	INTEGER, INTENT(IN) :: npars_p, npars_g, edge
	CHARACTER(len=20), INTENT(IN) :: modelname_p, modelname_g
	DOUBLE PRECISION, INTENT(IN) :: temperature, alpha
	DOUBLE PRECISION, DIMENSION(npars_p), INTENT(IN) :: pars_p
	DOUBLE PRECISION, DIMENSION(npars_g), INTENT(IN) :: pars_g
	DOUBLE PRECISION, INTENT(OUT) :: jac

	! local variables
	double precision :: y, temperatured, alphad

	temperatured = 1d0
	alphad = 0d0
	call PHI_D(temperature, temperatured, modelname_p, npars_p, pars_p&
	& , modelname_g, npars_g, pars_g, edge, alpha, alphad, y, jac)

END SUBROUTINE PHI_JAC


SUBROUTINE PSI_JAC(temperature, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, edge, alpha, indi, indj, jac)

	USE MOD_EXTREM
	IMPLICIT NONE

	INTEGER, INTENT(IN) :: npars_p, npars_g, edge, indi, indj
	CHARACTER(len=20), INTENT(IN) :: modelname_p, modelname_g
	DOUBLE PRECISION, INTENT(IN) :: temperature, alpha
	DOUBLE PRECISION, DIMENSION(npars_p), INTENT(IN) :: pars_p
	DOUBLE PRECISION, DIMENSION(npars_g), INTENT(IN) :: pars_g
	DOUBLE PRECISION, INTENT(OUT) :: jac

	! local variables

	double precision :: y, temperatured, alphad

	temperatured = 1d0
	alphad = 0d0
	call PSI_D(temperature, temperatured, modelname_p, npars_p, pars_p, &
	& modelname_g, npars_g, pars_g, edge, alpha, alphad, indi, indj, y, jac)

END SUBROUTINE PSI_JAC


SUBROUTINE EXTREMITY_JAC(x, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, edge, indi, indj, jac)
	USE MOD_EXTREM
	IMPLICIT NONE

	INTEGER, INTENT(IN) :: npars_p, npars_g, edge, indi, indj
	CHARACTER(len=20), INTENT(IN) :: modelname_p, modelname_g
	DOUBLE PRECISION, DIMENSION(2), INTENT(IN) :: x
	DOUBLE PRECISION, DIMENSION(npars_p), INTENT(IN) :: pars_p
	DOUBLE PRECISION, DIMENSION(npars_g), INTENT(IN) :: pars_g
	DOUBLE PRECISION, DIMENSION(2,2), INTENT(OUT) :: jac

	! local variable
	INTEGER :: n
	INTEGER :: i
	double precision :: y(2), xd(2)

	n = 2

	xd = 0d0
	DO i=1,n,1
		xd(i) = 1d0
		call EXTREMITY_D(x, xd, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, edge, indi, indj, y, jac(:,i))
		xd(i) = 0d0
	END DO

END SUBROUTINE EXTREMITY_JAC
