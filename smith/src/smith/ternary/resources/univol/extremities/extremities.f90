!!------------------------------------------------------------------------------------------------------
!! PROJET ALCOS 2017
!>  \ problemDefinition
!!  \brief Shooting function. (EDA System characterizes the azeotrope or the univolatility curve)
!!  \param[in] ny       Shooting variable dimension (in our case ny=3 or ny=2)
!!  \param[in] y        Shooting variable (in our case y = [x1 x2 T] ot y = [x1 x2])
!!  \param[in] npar     Number of optional parameters
!!  \param[in] par      Optional parameters
!!
!!  \param[out] s       Shooting value, same dimension as y (EDA system)

Subroutine phi(temperature, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, edge, alpha, y)

    use models
    implicit none

    integer,                                  intent(in)  :: npars_p, npars_g, edge
    character(len=20),                        intent(in)  :: modelName_p, modelName_g
    double precision,                         intent(in)  :: temperature, alpha
    double precision,  dimension(npars_p),    intent(in)  :: pars_p
    double precision,  dimension(npars_g),    intent(in)  :: pars_g
    double precision,                         intent(out) :: y

!!------------------------------------------------------------------------------------------------------
!! DEFINITION OF THE LOCAL VARIABLES AND INITIALISATION
!!------------------------------------------------------------------------------------------------------

    !! Local variables
    double precision :: concentrations(3),  K(3)
    integer          :: P0

		select case (trim(modelname_p))

			case('Antoine', 'antoine')
				P0 = 760

			case('DIPPR', 'dippr')
				P0 = 101325

			case default
				write(*,*) 'Wrong choice of model.'
				stop
		end select

    ! x = T
    select case (edge)
        case(1)
            concentrations(1) = 0d0
            concentrations(2) = alpha
            concentrations(3) = 1d0 - concentrations(2)
        case(2)
            concentrations(2) = 0d0
            concentrations(3) = alpha
            concentrations(1) = 1d0 - concentrations(3)
        case(3)
            concentrations(3) = 0d0
            concentrations(1) = alpha
            concentrations(2) = 1d0 - concentrations(1)
        case default
            write(*,*) 'Wrong choice of edge.'
            stop
    end select

    call getK(concentrations, temperature, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, P0, K)

    y = K(1)*concentrations(1) + K(2)*concentrations(2) + K(3)*concentrations(3) - 1d0

end subroutine phi


Subroutine psi(temperature, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, edge, alpha, indi, indj,  y)

    use models
    implicit none

    integer,                             	intent(in)  :: npars_p, npars_g, edge, indi, indj
    character(len=20),                     	intent(in)  :: modelName_p, modelName_g
    double precision,                    	intent(in)  :: temperature, alpha
    double precision,  dimension(npars_p),   	intent(in)  :: pars_p
    double precision,  dimension(npars_g),   	intent(in)  :: pars_g
    double precision,                    	intent(out) :: y

!!------------------------------------------------------------------------------------------------------
!! DEFINITION OF THE LOCAL VARIABLES AND INITIALISATION
!!------------------------------------------------------------------------------------------------------

    !! Local variables
    double precision :: concentrations(3), K(3)
    integer          :: P0

		select case (trim(modelname_p))

			case('Antoine', 'antoine')
				P0 = 760

			case('DIPPR', 'dippr')
				P0 = 101325

			case default
				write(*,*) 'Wrong choice of model.'
				stop
		end select

    ! x = T
    select case (edge)
        case(1)
            concentrations(1) = 0d0
            concentrations(2) = alpha
            concentrations(3) = 1d0 - concentrations(2)
        case(2)
            concentrations(2) = 0d0
            concentrations(3) = alpha
            concentrations(1) = 1d0 - concentrations(3)
        case(3)
            concentrations(3) = 0d0
            concentrations(1) = alpha
            concentrations(2) = 1d0 - concentrations(1)
        case default
            write(*,*) 'Wrong choice of edge.'
            stop
    end select

    call getK(concentrations, temperature, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, P0, K)

    y = K(indi) - K(indj)

end subroutine psi


Subroutine extremity(x, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, edge, indi, indj, y)

    use models
    implicit none

    integer,                             	intent(in)  :: npars_p, npars_g, edge, indi, indj
    character(len=20),                     	intent(in)  :: modelName_p, modelName_g
    double precision,  dimension(2),     	intent(in)  :: x
    double precision,  dimension(npars_p),   	intent(in)  :: pars_p
    double precision,  dimension(npars_g),   	intent(in)  :: pars_g
    double precision,  dimension(2),     	intent(out) :: y

!!------------------------------------------------------------------------------------------------------
!! DEFINITION OF THE LOCAL VARIABLES AND INITIALISATION
!!------------------------------------------------------------------------------------------------------

    !! Local variables
    double precision :: concentrations(3), temperature, K(3)
    integer          :: P0

		select case (trim(modelname_p))

			case('Antoine', 'antoine')
				P0 = 760

			case('DIPPR', 'dippr')
				P0 = 101325

			case default
				write(*,*) 'Wrong choice of model.'
				stop
		end select

    ! x = (x1, T)
    temperature = x(2)

    select case (edge)
        case(1)
            concentrations(1) = 0d0
            concentrations(2) = x(1)
            concentrations(3) = 1d0 - concentrations(2)
        case(2)
            concentrations(2) = 0d0
            concentrations(3) = x(1)
            concentrations(1) = 1d0 - concentrations(3)
        case(3)
            concentrations(3) = 0d0
            concentrations(1) = x(1)
            concentrations(2) = 1d0 - concentrations(1)
        case default
            write(*,*) 'Wrong choice of edge.'
            stop
    end select

    call getK(concentrations, temperature, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, P0, K)

    y(1) = K(1)*concentrations(1) + K(2)*concentrations(2) + K(3)*concentrations(3) - 1d0
    y(2) = K(indi) - K(indj)

end subroutine extremity
