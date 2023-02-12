Subroutine fcurve(x, beta, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, indi, indj, y)

    use models
    implicit none

    integer,                             intent(in)  :: npars_p, npars_g, indi, indj
    character(len=20),                   intent(in)  :: modelname_p, modelName_g
    double precision,  dimension(2),     intent(in)  :: x
    double precision,                    intent(in)  :: beta
    double precision,  dimension(npars_p), intent(in)  :: pars_p
    double precision,  dimension(npars_g), intent(in)  :: pars_g
    double precision,  dimension(2),     intent(out) :: y

!!------------------------------------------------------------------------------------------------------
!! DEFINITION OF THE LOCAL VARIABLES AND INITIALISATION
!!------------------------------------------------------------------------------------------------------

    ! x(1) = alpha = x2
    ! x(2) = temperature
    ! beta = x1

    !! Local variables
    double precision :: concentrations(3), temperature, K(3)
    integer 	     :: P0

		select case (trim(modelname_p))

			case('Antoine', 'antoine')
				P0 = 760

			case('DIPPR', 'dippr')
				P0 = 101325

			case default
				write(*,*) 'Wrong choice of model.'
				stop
		end select

    temperature       = x(2)
    concentrations(1) = beta
    concentrations(2) = x(1)
    concentrations(3) = 1d0 - concentrations(1) - concentrations(2)

    call getK(concentrations, temperature, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, P0, K)

    y(1) = K(1)*concentrations(1) + K(2)*concentrations(2) + K(3)*concentrations(3) - 1d0
    y(2) = K(indi) - K(indj)

end subroutine fcurve
