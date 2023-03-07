module models

	implicit none

	contains

	! split data
	subroutine getDataActivity_nrtl(modelname, nparData, parData, A, alpha, R)

		implicit none
		character(len=20), intent(in) 			:: modelname
		integer, intent(in)                             :: nparData
		double precision, intent(in)                    :: parData(nparData)
		double precision, intent(out),  dimension(3,3)  :: A, alpha
		double precision, intent(out)                   :: R

		!! Matrix A of binary interaction
		A(1,:)      = parData(1:3)
		A(2,:)      = parData(4:6)
		A(3,:)      = parData(7:9)

		!! Symetric matrix Alpha
		alpha(1,:)  = parData(10:12)
		alpha(2,:)  = parData(13:15)
		alpha(3,:)  = parData(16:18)

		!! The constant R
		R           = parData(19)

	end subroutine getDataActivity_nrtl

	subroutine getDataActivity_uniquac(modelname, nparData, parData, A, rp, q, Qp, z, R)

		implicit none
		character(len=20), intent(in) 			:: modelname
		integer, intent(in)                             :: nparData
		double precision, intent(in)                    :: parData(nparData)
		double precision, intent(out),  dimension(3,3)  :: A
		double precision, intent(out),  dimension(3)    :: rp, q, Qp
		double precision, intent(out)                   :: z, R

		!! Matrix A of binary interaction
		A(1,:)      = parData(1:3)
		A(2,:)      = parData(4:6)
		A(3,:)      = parData(7:9)

		!! Coefficient r, q, Qp
		rp  = parData(10:12)
		q   = parData(13:15)
		Qp  = parData(16:18)

		!! The constant z
		z       = parData(19)
		!! The constant R
		R           = parData(20)

	end subroutine getDataActivity_uniquac


	subroutine getDataPressure_antoine(modelname, nparData, parData, antoineA, antoineB, antoineC)
		implicit none
		character(len=20), intent(in) 			:: modelname
		integer, intent(in)                             :: nparData
		double precision, intent(in)                    :: parData(nparData)
		double precision, intent(out),  dimension(3)    :: antoineA, antoineB, antoineC

		!! Antoine's Equation constants
		antoineA    = parData(1:3)
		antoineB    = parData(4:6)
		antoineC    = parData(7:9)

	end subroutine getDataPressure_antoine


	subroutine getDataPressure_dippr(modelname, nparData, parData, dipprA, dipprB, dipprC, dipprD, dipprE)
		implicit none
		character(len=20), intent(in) 			:: modelname
		integer, intent(in)                             :: nparData
		double precision, intent(in)                    :: parData(nparData)
		double precision, intent(out),  dimension(3)    :: dipprA, dipprB, dipprC, dipprD, dipprE

		!! Dippr's Equation constants
		dipprA    = parData(1:3)
		dipprB    = parData(4:6)
		dipprC    = parData(7:9)
		dipprD	  = parData(10:12)
		dipprE	  = parData(13:15)

	end subroutine getDataPressure_dippr


	subroutine getPressure(temperature, modelname, modelpars_dim, modelpars, pression)
		implicit none
		double precision, intent(in) 		:: temperature
		character(len=20), intent(in) 		:: modelname
		integer, intent(in) 			:: modelpars_dim
		double precision, intent(in) 		:: modelpars(modelpars_dim)
		double precision, intent(out) 		:: pression(3)

		! on calcule p en fonction du modèle
		! attention, la taille du vecteur de paramètres modelpars dépend de modelname
		! modelname = 'antoine', 'dippr'

		! Local variables
		double precision,  dimension(3) 	:: antoineA, antoineB, antoineC
		double precision,  dimension(3) 	:: dipprA, dipprB, dipprC, dipprD, dipprE
		integer 				:: n
		double precision 			:: T
		integer 				:: i 				!! Loop indice

		T = temperature
		n = 3

		select case (trim(modelname))

			case('ANTOINE', 'antoine') !! Antoine model
				! get data
				call getDataPressure_antoine(modelname, modelpars_dim, modelpars, antoineA, antoineB, antoineC)

				!! Calcul des pressions partielles Pi en utilisant l'equation d'antoine
				Do i=1,n,1
					pression(i) = 10d0**(antoineA(i)-antoineB(i)/(T + antoineC(i)))
				Enddo

			case('DIPPR', 'dippr')
				! get Data
				call getDataPressure_dippr(modelname, modelpars_dim, modelpars, dipprA, dipprB, dipprC, dipprD, dipprE)

				!! Calcul des pressions partielles Pi en utilisant l'equation DIPPR
				Do i=1,n,1
					pression(i) = (T**dipprC(i))*exp(dipprA(i) + dipprB(i)/T + dipprD(i)*(T**dipprE(i)))
				Enddo

			case default
				write(*,*) 'Wrong choice of model.'
				stop
		end select
	end subroutine getPressure

	subroutine getKaux(concentrations, temperature, modelname_p, modelpars_p_dim, modelpars_p,&
			modelname_g, modelpars_g_dim, modelpars_g, P0, Kaux)
		implicit none

		double precision, dimension(3),		intent(in) 	:: concentrations
		double precision, 			intent(in) 	:: temperature
		character(len=20), 			intent(in) 	:: modelname_p, modelname_g
		integer, 				intent(in) 	:: modelpars_p_dim, modelpars_g_dim
		double precision, 			intent(in) 	:: modelpars_p(modelpars_p_dim), modelpars_g(modelpars_g_dim)
		integer, intent(in) 					:: P0
		double precision, intent(out) 				:: Kaux(2)

		! Local variables
		double precision,  dimension(3,3) 	:: A, alpha
		double precision,  dimension(3)     ::  rp, q, Qp
		double precision 			:: R, z
		integer 				:: n
		double precision 			:: x(3), T
		integer 				:: i,j 				!! Loop indice
		double precision 			::  fr1,fr2,fr3,fr4,fr5,fr6
		double precision,  dimension(3,3) 	::  tho,G
		double precision,  dimension(3) 	::  pression
		double precision,  dimension(3)   ::  partie1, partie2, partie3, partie4, partie5              !! intermediaire variables
		double precision,  dimension(3,2) ::  fraction1, fraction2                                        !! intermediaire variables
		double precision                  ::  denom1, denom2, denom3, som1
		double precision,  dimension(3)   ::  phi, theta, theta_prim, l

		x = concentrations
		T = temperature

		!! Initialisation of the local variables at zero
		partie1 = 0d0
		partie2 = 0d0
		partie3 = 0d0
		partie4 = 0d0
		partie5 = 0d0
		fraction1 = 0d0
		fraction2 = 0d0
		denom1 = 0d0
		denom2 = 0d0
		denom3 = 0d0
		fr1 = 0d0
		fr2 = 0d0

		n = 3

		call getPressure(temperature, modelname_p, modelpars_p_dim, modelpars_p, pression)

		select case (trim(modelname_g))

			case('NRTL', 'nrtl') !! nrtl model

				! get data
				call getDataActivity_nrtl(modelname_g, modelpars_g_dim, modelpars_g, A, alpha, R)

				!!*****************************************************************************************************************
				!!!!!!!!!!!!!!!!!!!!!!!!!!CALCULATION OF ALL PARAMETERS NEEDED TO COSNTRUCT THE EDA SYSTEM!!!!!!!!!!!!!!!!!!!!!!!!!
				!!*****************************************************************************************************************

				!! Construction of tho(i,j)
				Do i=1,n,1
					Do j=1,n,1
						tho(i,j) = A(i,j)/(R*(T+273.15))
					Enddo
				Enddo

				!! Construction of G(i,j)
				Do i=1,n,1
					Do j=1,n,1
						G(i,j) = exp(-alpha(i,j)*tho(i,j))
					Enddo
				Enddo

				!!*****************************************************************************************************************
				!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!CONSTRUCTION OF THE EDA SYSTEM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
				!!*****************************************************************************************************************

				!! Calculation of the equilibrium constants in the case of a binary mixture (getAzeotropeBinary)
				!! The binary case when substance 3 is absent
				fr1 = ((1 - x(1)) + x(1)*G(1,2))**2
				fr2 = (x(1) + (1 - x(1))*G(2,1))**2
				Kaux(1) = pression(1)*exp(((1 - x(1))**2)*(tho(2,1)*(G(2,1)/fr2**(0.5d0))**2 + tho(1,2)*G(1,2)/fr1))/P0
				Kaux(2) = pression(2)*exp((x(1)**2)*(tho(1,2)*(G(1,2)/fr1**(0.5d0))**2 + tho(2,1)*G(2,1)/fr2))/P0

			case('UNIQUAC', 'uniquac')

				! get data
				call getDataActivity_uniquac(modelname, modelpars_dim, modelpars, A, rp, q, Qp, z, R)

				!! Construction of l(i)
				Do i=1,n,1
					l(i) = (z/2)*(rp(i)-q(i)) - (rp(i)-1)
				Enddo

				!! Construction of phi(i)
				do i=1,n,1
					denom1 = denom1 + rp(i)*x(i)
				enddo
				Do i=1,n,1
					phi(i) = (rp(i)*x(i))/denom1
				Enddo

				!! Construction of theta(i)
				Do i=1,n,1
					denom2 = denom2 + q(i)*x(i)
				Enddo
				Do i=1,n,1
					theta(i) = (q(i)*x(i))/denom2
				Enddo

				!! Construction of theta_prim(i)
				Do i=1,n,1
					denom3 = denom3 + Qp(i)*x(i)
				Enddo
				Do i=1,n,1
					theta_prim(i) = (Qp(i)*x(i))/denom3
				Enddo

				!! Construction of tho(i,j) et tho(j, i)
				Do i=1,n,1
					Do j=1,n,1
						tho(i,j) = exp(-A(i,j)/(T*R))
					Enddo
				Enddo

				!! Construction de la partie 1
				Do i=1,n,1
					partie1(i) = log(phi(i)/x(i))
				Enddo

				!! Construction de la partie 2
				Do i=1,n,1
					partie2(i) = (z/2)*q(i)*log(theta(i)/phi(i))
				Enddo

				!! Construction de la partie 3
				Do i=1,n,1
					som1 = som1 + x(i)*l(i)
				Enddo
				Do i=1,n,1
					partie3(i) = l(i) - (phi(i)/x(i))*som1
				Enddo

				!! Construction de la partie 4
				Do i=1,n,1
					Do j=1,n,1
						fraction1(i,1) = fraction1(i,1) + theta_prim(j)*tho(j,i)
					enddo
					partie4(i) = -Qp(i)*log(fraction1(i,1))
				enddo

				!! Construction de la partie 5
				Do i=1,n,1
					Do j=1,n,1
						!! the fraction
			    		fraction2(i,1) = fraction2(i,1) + (theta_prim(j)*tho(i,j))/fraction1(j,1)
					Enddo
					partie5(i) = Qp(i)*(1 - fraction2(i,1))
				Enddo

				Do i=1,n,1
					Kaux(i) = (pression(i)*exp(partie1(i)+partie2(i)+partie3(i)+partie4(i)+partie5(i)))/P0
				Enddo

			case default
				write(*,*) 'Wrong choice of model.'
				stop
		end select

	end subroutine

end module models


!		!! The binary case or substance 1 is absent
!		fr3 = ((1 - x(2)) + x(2)*G(2,3))**2
!		fr4 = (x(2) + (1 - x(2))*G(3,2))**2
!		Kaux(3) = pression(2)*exp((1 - x(2))**2*(tho(3,2)*(G(3,2)/fr4**(0.5d0))**2 + tho(2,3)*G(2,3)/fr3))/P0
!		Kaux(4) = pression(3)*exp(x(2)**2*(tho(2,3)*(G(2,3)/fr3**(0.5d0))**2 + tho(3,2)*G(3,2)/fr4))/P0
!		!! The binary case or substance 2 is absent
!		fr5 = ((1 - x(1)) + x(1)*G(1,3))**2
!		fr6 = (x(1) + (1 - x(1))*G(3,1))**2
!		Kaux(5) = pression(1)*exp((1 - x(1))**2*(tho(3,1)*(G(3,1)/fr6**(0.5d0))**2 + tho(1,3)*G(1,3)/fr5))/P0
!		Kaux(6) = pression(3)*exp(x(1)**2*(tho(1,3)*(G(1,3)/fr5**(0.5d0))**2 + tho(3,1)*G(3,1)/fr6))/P0
