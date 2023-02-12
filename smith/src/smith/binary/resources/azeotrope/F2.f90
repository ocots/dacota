Subroutine f2(x, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, y)

    use models
    implicit none

	  integer,                            		   		 intent(in)  :: npars_p, npars_g
    character(len=20),                   	         intent(in)  :: modelName_p, modelName_g
	  double precision,  dimension(2),     	   	     intent(in)  :: x
    double precision,  dimension(npars_p), 				 intent(in)  :: pars_p
    double precision,  dimension(npars_g), 				 intent(in)  :: pars_g
    double precision,  dimension(2),     		   		 intent(out) :: y

    ! local variables
    double precision :: concentrations(3), temperature, Kaux(2)
	  integer          :: P0

		P0 = 760

    ! x = (x1, T)
    concentrations(3) = 0d0
    concentrations(1) = x(1)
    concentrations(2) = 1d0 - concentrations(1)
    temperature    = x(2)

    call getKaux(concentrations, temperature, modelname_p, npars_p, pars_p, modelname_g, npars_g, pars_g, P0, Kaux)

    y(1) = 1d0 - Kaux(1)
    y(2) = 1d0 - Kaux(2)

end subroutine f2
