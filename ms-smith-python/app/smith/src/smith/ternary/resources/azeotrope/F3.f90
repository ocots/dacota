!!------------------------------------------------------------------------------------------------------
!! PROJET ALCOS 2017
!>  \ problemDefinition
!!  \brief Shooting function. (EDA System characterizes the azeotrope ternary)
!!  \param[in] ny       Shooting variable dimension (in our case ny=3)
!!  \param[in] y        Shooting variable (in our case y = [x1 x2 T])
!!  \param[in] npar     Number of optional parameters
!!  \param[in] par      Optional parameters
!!
!!  \param[out] s       Shooting value, same dimension as y (EDA system)

Subroutine f3(x, modelname_p, modelpars_p_dim, modelpars_p, modelname_g, modelpars_g_dim, modelpars_g, y)

    use models
    implicit none

	  integer,                            		       intent(in)  :: modelpars_p_dim, modelpars_g_dim
    character(len=20),                   	         intent(in)  :: modelName_p, modelName_g
	  double precision,  dimension(3),     	   	     intent(in)  :: x
    double precision,  dimension(modelpars_p_dim), intent(in)  :: modelpars_p
    double precision,  dimension(modelpars_g_dim), intent(in)  :: modelpars_g
    double precision,  dimension(3),     		       intent(out) :: y

    ! local variables
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

    ! x = (x1, x2, T)

    concentrations(1) = x(1)
    concentrations(2) = x(2)
    concentrations(3) = 1d0 - x(1) - x(2)
    temperature       = x(3)

    call getK(concentrations, temperature,modelname_p, modelpars_p_dim, modelpars_p,&
							modelname_g, modelpars_g_dim, modelpars_g, P0, K)

    y(1) = (1d0 - K(1))*concentrations(1)
    y(2) = (1d0 - K(2))*concentrations(2)
    y(3) = (1d0 - K(3))*concentrations(3)

end subroutine f3
